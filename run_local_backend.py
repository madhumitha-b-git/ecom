import subprocess
import sys
import os
import time

# Services and port mappings
services = {
    "order-service": {"port": 8000, "dir": "microservices/order-service"},
    "cart-service": {"port": 8001, "dir": "microservices/cart-service"},
    "inventory-service": {"port": 8002, "dir": "microservices/inventory-service"},
    "payment-service": {"port": 8003, "dir": "microservices/payment-service"},
    "product-service": {"port": 8004, "dir": "microservices/product-service"},
    "analytics-service": {"port": 8005, "dir": "microservices/analytics-service"},
    "auth-service": {"port": 8006, "dir": "microservices/auth-service"}
}

processes = []

if __name__ == "__main__":
    # Ensure uvicorn is installed in current Python env
    try:
        import uvicorn
    except ImportError:
        print("Error: 'uvicorn' is not installed in the active environment. Please install it using:")
        print("  pip install uvicorn")
        sys.exit(1)

    print("=" * 60)
    print("      Starting E-Commerce Microservices Locally (Ports 8000-8004)      ")
    print("=" * 60)
    
    try:
        for name, config in services.items():
            port = config["port"]
            directory = config["dir"]
            
            # Start uvicorn process
            print(f"[+] Starting {name} on http://127.0.0.1:{port} ...")
            p = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)],
                cwd=directory
            )
            processes.append((name, p))
            time.sleep(0.5)  # Delay to give processes time to bind ports

        print("\n[!] All backend services are running. Press Ctrl+C to terminate all services.\n")
        
        while True:
            # Monitor processes
            for name, p in processes:
                exit_code = p.poll()
                if exit_code is not None:
                    print(f"\n[-] Process {name} exited with code {exit_code}")
                    processes.remove((name, p))
            time.sleep(1.0)
            
    except KeyboardInterrupt:
        print("\n\n[!] KeyboardInterrupt detected. Terminating all services gracefully...")
        for name, p in processes:
            print(f"[-] Stopping {name}...")
            p.terminate()
            p.wait()
        print("[+] All microservices stopped successfully.")
