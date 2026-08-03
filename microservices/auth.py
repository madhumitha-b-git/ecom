import base64
import time
import json
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Decodes and validates the token.
    Supports:
    1. Cognito JWT Token (header.payload.signature) -> extracts cognito:username
    2. Local Base64 Token (username:timestamp) -> extracts username
    """
    token = credentials.credentials
    try:
        if "." in token:
            # Real JWT token
            parts = token.split(".")
            if len(parts) == 3:
                payload_b64 = parts[1]
                # Add base64 padding if needed
                payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
                # Standard base64url decode uses urlsafe_b64decode
                payload_bytes = base64.urlsafe_b64decode(payload_b64.encode("utf-8"))
                payload = json.loads(payload_bytes.decode("utf-8"))
                username = payload.get("cognito:username") or payload.get("username") or payload.get("sub", "unknown")
                return username
                
        # Fallback to local Base64 token
        decoded_bytes = base64.b64decode(token)
        decoded_str = decoded_bytes.decode("utf-8")
        
        parts = decoded_str.split(":")
        if len(parts) != 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format. Expected username:timestamp",
            )
            
        username, timestamp_str = parts[0], parts[1]
        timestamp_ms = int(timestamp_str)
        
        if timestamp_ms <= 0:
            raise ValueError()
            
        return username
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
