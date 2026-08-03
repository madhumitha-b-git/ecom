import time
import os
import json
from database import write_raw_event, get_raw_events, write_stage_data, get_stage_data
from logger import get_logger

logger = get_logger(__name__)

# In-memory web socket list for active dashboard clients
active_ws_connections = []

async def register_connection(ws):
    await ws.accept()
    active_ws_connections.append(ws)
    logger.info("WS | Client connected. Active: %d", len(active_ws_connections))

def unregister_connection(ws):
    if ws in active_ws_connections:
        active_ws_connections.remove(ws)
        logger.info("WS | Client disconnected. Active: %d", len(active_ws_connections))

async def broadcast_event(event_data: dict):
    for ws in active_ws_connections:
        try:
            await ws.send_json(event_data)
        except Exception as e:
            logger.warn("WS | Failed to broadcast to client: %s", e)

def ingest_event(event_type: str, data: dict):
    # 1. Store as Raw S3 Event
    write_raw_event(event_type, data)
    # 2. Trigger ETL aggregate calculation immediately
    run_etl_job()

def run_etl_job():
    """Simulates AWS Glue ETL job reading from Raw S3 and writing to Stage S3."""
    logger.info("ETL | Running Glue ETL job...")
    raw_events = get_raw_events()

    # --- 1. Company Perspective (Revenue) ---
    latest_orders = {}
    for event in raw_events:
        if event.get("event_type") == "order_status_update":
            payload = event.get("data", {})
            order_id = payload.get("order_id")
            if order_id:
                latest_orders[order_id] = payload

    active_orders = [o for o in latest_orders.values() if o.get("status") in ("SUCCESS", "PENDING", "INVENTORY_RESERVED")]
    
    total_revenue = 0.0
    order_count = len(active_orders)
    product_sales = {}
    
    for order in active_orders:
        amount = float(order.get("amount", 0.0))
        total_revenue += amount
        
        prod_id = order.get("product_id", "unknown")
        product_sales[prod_id] = product_sales.get(prod_id, 0) + int(order.get("quantity", 1))

    average_order_value = total_revenue / order_count if order_count > 0 else 0.0
    
    company_stage = {
        "total_revenue": total_revenue,
        "total_orders": order_count,
        "average_order_value": average_order_value,
        "product_sales": product_sales,
        "last_updated": time.time()
    }
    write_stage_data("revenue_analytics", company_stage)

    # --- 2. Customer Perspective (Cart Abandonment) ---
    # Find all cart add items
    cart_adds = {}  # key: (user_id, product_id) -> timestamp
    for event in raw_events:
        if event.get("event_type") == "cart_action":
            payload = event.get("data", {})
            user_id = payload.get("user_id")
            prod_id = payload.get("product_id")
            action = payload.get("action")
            if user_id and prod_id:
                key = f"{user_id}:{prod_id}"
                if action == "add":
                    cart_adds[key] = event.get("timestamp")
                elif action == "remove" or action == "clear":
                    cart_adds.pop(key, None)

    # Find users who completed an order (to remove from abandonment)
    success_orders = [o for o in latest_orders.values() if o.get("status") in ("SUCCESS", "DELIVERED", "SHIPPED")]
    completed_keys = set()
    for order in success_orders:
        uid = order.get("user_id")
        pid = order.get("product_id")
        if uid and pid:
            completed_keys.add(f"{uid}:{pid}")

    # Carts not ordered within 30 seconds are marked as abandoned (short time for demo)
    abandoned_carts = []
    current_time = time.time()
    for key, timestamp in cart_adds.items():
        if key not in completed_keys:
            # 30 seconds threshold for local demonstration testing
            if current_time - timestamp > 30:
                user_id, prod_id = key.split(":")
                abandoned_carts.append({
                    "user_id": user_id,
                    "product_id": prod_id,
                    "added_at": timestamp,
                    "abandoned_duration": current_time - timestamp
                })

    customer_stage = {
        "abandoned_count": len(abandoned_carts),
        "abandoned_carts": abandoned_carts,
        "last_updated": current_time
    }
    write_stage_data("cart_abandonment", customer_stage)

    # --- 3. Engineer Perspective (Reliability & TAT) ---
    order_creations = {}
    order_resolutions = {}
    
    for event in raw_events:
        event_type = event.get("event_type")
        payload = event.get("data", {})
        o_id = payload.get("order_id")
        
        if o_id:
            if event_type == "order_status_update":
                status = payload.get("status")
                if status == "PENDING":
                    order_creations[o_id] = event.get("timestamp")
                elif status in ["SUCCESS", "FAILED"]:
                    order_resolutions[o_id] = {
                        "status": status,
                        "timestamp": event.get("timestamp")
                    }

    tats = []
    failures = 0
    successes = 0

    for o_id, start_time in order_creations.items():
        res = order_resolutions.get(o_id)
        if res:
            end_time = res["timestamp"]
            tats.append(end_time - start_time)
            if res["status"] == "SUCCESS":
                successes += 1
            else:
                failures += 1

    avg_tat = sum(tats) / len(tats) if tats else 0.0
    sla_percentage = (successes / (successes + failures) * 100.0) if (successes + failures) > 0 else 100.0

    engineer_stage = {
        "average_tat_seconds": avg_tat,
        "success_rate_sla": sla_percentage,
        "total_failures": failures,
        "total_successes": successes,
        "last_updated": current_time
    }
    write_stage_data("reliability_metrics", engineer_stage)
    logger.info("ETL | ETL completed successfully.")
