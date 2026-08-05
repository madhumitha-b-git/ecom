import os
import subprocess
import sys

services = [
    "analytics-service",
    "auth-service",
    "cart-service",
    "inventory-service",
    "order-service",
    "payment-service",
    "product-service"
]

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "microservices"))

for service in services:
    service_dir = os.path.join(base_dir, service)
    if not os.path.isdir(service_dir):
        continue
        
    print(f"Re-compiling ZIP for {service}...")
    os.chdir(service_dir)
    
    if os.path.exists("build_zip.py"):
        subprocess.run([sys.executable, "build_zip.py"], check=True)
        print(f"Generated new deploy.zip for {service}")

print("All zips recompiled successfully!")
