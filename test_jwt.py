import os
import base64
import hmac
import hashlib
import json
import time

JWT_SECRET = "IS2XRMkqOowrmCpBFhs4DAcJ0vul95G1WaH6gViK"

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def sign_jwt(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_enc = base64url_encode(json.dumps(header).encode('utf-8'))
    payload_enc = base64url_encode(json.dumps(payload).encode('utf-8'))
    signing_input = f"{header_enc}.{payload_enc}".encode('utf-8')
    signature = hmac.new(JWT_SECRET.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_enc = base64url_encode(signature)
    return f"{header_enc}.{payload_enc}.{sig_enc}"

def _verify_signature(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT structure")
    header_enc, payload_enc, sig_enc = parts
    signing_input = f"{header_enc}.{payload_enc}".encode("utf-8")
    expected_sig = base64.urlsafe_b64encode(
        hmac.new(JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    ).rstrip(b"=").decode("utf-8")
    if not hmac.compare_digest(expected_sig, sig_enc):
        raise ValueError("Invalid signature")
    payload_b64 = payload_enc + "=" * ((4 - len(payload_enc) % 4) % 4)
    return json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))

try:
    token = sign_jwt({"username": "madhumithamalu6@gmail.com", "role": "admin", "exp": int(time.time()) + 86400})
    print("Token:", token)
    payload = _verify_signature(token)
    print("Payload:", payload)
except Exception as e:
    print("Error:", e)
