"""
Generate a demo bearer token matching the frontend's logic:
    const token = btoa(`${username}:${Date.now()}`);

Usage:
    python generate_token.py
    python generate_token.py myusername
"""

import base64
import time
import sys


def generate_demo_token(username: str = "testuser") -> str:
    timestamp_ms = int(time.time() * 1000)
    raw = f"{username}:{timestamp_ms}"
    token = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
    return token


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "testuser"
    token = generate_demo_token(username)

    print(f"Username : {username}")
    print(f"Token    : {token}")
    print(f"\nUse in Postman as:")
    print(f"  Authorization: Bearer {token}")