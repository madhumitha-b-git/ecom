import boto3
import subprocess
import sys
import os

def run_terraform():
    print("Fetching AWS credentials via Boto3...")
    try:
        # Boto3 correctly parses the Windows SSO profile without issues
        session = boto3.Session(profile_name="idp-sbx-trn-lab-01")
        creds = session.get_credentials().get_frozen_credentials()
    except Exception as e:
        print(f"Error getting credentials: {e}")
        print("Please run: aws sso login --profile idp-sbx-trn-lab-01")
        sys.exit(1)

    # Prepare environment variables for Terraform
    env = os.environ.copy()
    env["AWS_ACCESS_KEY_ID"] = creds.access_key
    env["AWS_SECRET_ACCESS_KEY"] = creds.secret_key
    env["AWS_SESSION_TOKEN"] = creds.token
    env["AWS_REGION"] = "ap-southeast-1"

    # Grab the command to run (e.g. "plan" or "apply")
    args = sys.argv[1:]
    if not args:
        args = ["plan"]

    cmd = ["terraform"] + args
    print(f"Running: {' '.join(cmd)}\n")
    
    # Run terraform with the explicit temporary credentials
    subprocess.run(cmd, env=env)

if __name__ == "__main__":
    run_terraform()
