import os
import subprocess
import sys

def deploy():
    build_only = "--build-only" in sys.argv
    deploy_only = "--deploy-only" in sys.argv
    
    target_service = None
    if "--service" in sys.argv:
        idx = sys.argv.index("--service")
        if idx + 1 < len(sys.argv):
            target_service = sys.argv[idx + 1]

    # List of your microservices
    services = [
        "analytics-service",
        "auth-service",
        "cart-service",
        "inventory-service",
        "order-service",
        "payment-service",
        "product-service"
    ]
    
    if target_service:
        if target_service in services:
            services = [target_service]
        else:
            print(f"Error: Unknown service {target_service}")
            sys.exit(1)
            
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "microservices"))
    
    for service in services:
        service_dir = os.path.join(base_dir, service)
        if not os.path.isdir(service_dir):
            continue
            
        print(f"\n{'='*50}\n[*] Processing {service}...\n{'='*50}")
        os.chdir(service_dir)
        
        # 1. Build the zip file if a build script exists
        if not deploy_only:
            if os.path.exists("build_zip.py"):
                print("[1/2] Building zip file...")
                subprocess.run([sys.executable, "build_zip.py"], check=True)
            else:
                print(f"[!] Warning: No build_zip.py found in {service}")
                
        # 2. Deploy to AWS Lambda
        if not build_only:
            if os.path.exists("deploy.zip"):
                print(f"[2/2] Uploading to AWS Lambda ({service}_ecom)...")
                cmd = [
                    "aws", "lambda", "update-function-code",
                    "--function-name", f"{service}_ecom",
                    "--zip-file", "fileb://deploy.zip"
                ]
                
                # Only use the local AWS profile if we are NOT running in a CI/CD environment
                if not os.getenv("CI"):
                    cmd.extend(["--profile", "idp-sbx-trn-lab-01"])
                    
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"[SUCCESS] Successfully deployed {service}!")
                else:
                    print(f"[ERROR] Failed to deploy {service}: {result.stderr}")
            else:
                print(f"[ERROR] Failed: deploy.zip was not generated for {service}")

if __name__ == "__main__":
    deploy()
