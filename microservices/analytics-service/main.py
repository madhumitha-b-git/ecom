from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.fastapi.middleware import FastAPIMiddleware
patch_all()

from fastapi import FastAPI, Request, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
from logger import get_logger
import service
import database

logger = get_logger(__name__)
app = FastAPI(title="Analytics Service", version="1.0.0")
app.add_middleware(FastAPIMiddleware, recorder=xray_recorder)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

router = APIRouter()

class EventPublishRequest(BaseModel):
    event_type: str
    data: dict

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("--> %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("<-- %s %s %d", request.method, request.url.path, response.status_code)
    return response

@app.get("/", tags=["Health"])
def health():
    return {"service": "analytics-service", "status": "ok"}

@router.post("/analytics/publish-event", summary="Ingest event into Data Lake and broadcast via Event Broker")
async def publish_event(req: EventPublishRequest):
    # 1. Ingest into S3 Raw directory
    service.ingest_event(req.event_type, req.data)
    # 2. Broadcast via WebSockets to listening clients
    await service.broadcast_event({
        "event_type": req.event_type,
        "data": req.data
    })
    return {"status": "event_published"}

@router.get("/analytics/company/revenue", summary="Get Revenue analytics")
def get_revenue_analytics():
    return database.get_stage_data("revenue_analytics")

@router.get("/analytics/customer/abandoned-carts", summary="Get abandoned carts")
def get_abandoned_carts():
    return database.get_stage_data("cart_abandonment")

@router.get("/analytics/engineer/reliability", summary="Get system TAT and reliability SLA metrics")
def get_reliability_metrics():
    return database.get_stage_data("reliability_metrics")

# WebSocket Endpoint for live visual event monitoring
@router.websocket("/analytics/ws")
async def websocket_endpoint(websocket: WebSocket):
    await service.register_connection(websocket)
    try:
        while True:
            # Keep connection alive by reading message
            data = await websocket.receive_text()
            logger.info("WS | Received message from client: %s", data)
    except WebSocketDisconnect:
        service.unregister_connection(websocket)
    except Exception as e:
        logger.error("WS | Connection error: %s", e)
        service.unregister_connection(websocket)

app.include_router(router, prefix="/v1")

handler = Mangum(app)
