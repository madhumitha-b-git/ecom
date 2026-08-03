import os
import time
import secrets
import hashlib
from database import get_db
from config import settings
from exceptions import (
    UserExistsError,
    InvalidCredentialsError,
    UserNotVerifiedError,
    VerificationCodeInvalidError
)
from logger import get_logger

logger = get_logger(__name__)
JWT_SECRET = "super-secret-ecom-key-12345"

def base64url_encode(data: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def sign_jwt(payload: dict) -> str:
    import json
    import hmac
    header = {"alg": "HS256", "typ": "JWT"}
    header_enc = base64url_encode(json.dumps(header).encode('utf-8'))
    payload_enc = base64url_encode(json.dumps(payload).encode('utf-8'))
    signing_input = f"{header_enc}.{payload_enc}".encode('utf-8')
    signature = hmac.new(JWT_SECRET.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_enc = base64url_encode(signature)
    return f"{header_enc}.{payload_enc}.{sig_enc}"

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed, salt

def register_user(name: str, email: str, password_raw: str) -> dict:
    import re
    if len(password_raw) < 8:
        raise Exception("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', password_raw):
        raise Exception("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', password_raw):
        raise Exception("Password must contain at least one lowercase letter")
    if not re.search(r'[0-9]', password_raw):
        raise Exception("Password must contain at least one number")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password_raw):
        raise Exception("Password must contain at least one special character (!@#$%^&* etc.)")

    db = get_db()
    existing = db.get_item(Key={"email": email})
    if "Item" in existing:
        raise UserExistsError()

    code = str(secrets.randbelow(900000) + 100000) # 6 digit code
    expires_at = int(time.time()) + 600 # 10 minutes from now
    password_hash, salt = hash_password(password_raw)

    user_item = {
        "email": email,
        "name": name,
        "password_hash": password_hash,
        "salt": salt,
        "status": "VERIFICATION_PENDING",
        "verification_code": code,
        "code_expires_at": expires_at
    }

    db.put_item(Item=user_item)
    
    email_sent = _send_otp_email(email, name, code)

    return {
        "message": "Verification code sent to your email. Please check your inbox."
                    if email_sent else
                    "Account created, but we couldn't send the email right now. Please use 'Resend code' shortly.",
        "email": email,
        "email_sent": email_sent
    }
    
def _send_otp_email(email: str, name: str, code: str) -> bool:
    """Send OTP verification email via SMTP. Returns True if sent successfully."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    SENDER = settings.SMTP_SENDER
    SUBJECT = "Your E-Shop Verification Code"
    BODY_HTML = f"""
    <html><body>
    <h2>Welcome to E-Shop, {name}!</h2>
    <p>Your verification code is:</p>
    <h1 style="letter-spacing: 8px; color: #10b981;">{code}</h1>
    <p>This code expires in <strong>10 minutes</strong>.</p>
    <p>If you did not register, please ignore this email.</p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = email
    msg.attach(MIMEText(BODY_HTML, "html"))

    if not settings.SMTP_PASSWORD:
        logger.warning("SMTP_PASSWORD not configured. Printing code to console:")
        logger.info("FALLBACK | Verification Code for %s: %s", email, code)
        return False

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, settings.SMTP_PASSWORD)
            server.sendmail(SENDER, email, msg.as_string())
        logger.info("SMTP | OTP email sent to: %s", email)
        return True
    except Exception as e:
        logger.error("SMTP | Unexpected error: %s", e)
        logger.info("FALLBACK | Verification Code for %s: %s", email, code)
        return False


def verify_code(email: str, code: str) -> dict:
    db = get_db()
    existing = db.get_item(Key={"email": email})
    if "Item" not in existing:
        raise VerificationCodeInvalidError()
    
    user = existing["Item"]
    if user.get("verification_code") != code or int(user.get("code_expires_at", 0)) < time.time():
        raise VerificationCodeInvalidError()

    db.update_item(
        Key={"email": email},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "VERIFIED"}
    )

    token = sign_jwt({"username": email, "role": "user", "exp": int(time.time()) + 86400})
    return {
        "message": "Account verified successfully",
        "token": token,
        "username": email,
        "name": user.get("name", "")
    }

def login_user(email: str, password_raw: str) -> dict:
    db = get_db()
    existing = db.get_item(Key={"email": email})
    if "Item" not in existing:
        raise InvalidCredentialsError()

    user = existing["Item"]
    password_hash, _ = hash_password(password_raw, user.get("salt"))
    if user.get("password_hash") != password_hash:
        raise InvalidCredentialsError()

    if user.get("status") != "VERIFIED":
        raise UserNotVerifiedError()

    token = sign_jwt({"username": email, "role": "user", "exp": int(time.time()) + 86400})
    return {
        "message": "Login successful",
        "token": token,
        "username": email,
        "name": user.get("name", "")
    }

def get_all_users() -> list[dict]:
    db = get_db()
    users = []
    if type(db).__name__ == "LocalUserDB":
        data = db._read()
        for email, info in data.items():
            users.append({
                "name": info.get("name"),
                "email": email,
                "status": info.get("status"),
                "code_expires_at": info.get("code_expires_at")
            })
    else:
        try:
            response = db.scan()
            items = response.get("Items", [])
            for item in items:
                users.append({
                    "name": item.get("name"),
                    "email": item.get("email"),
                    "status": item.get("status"),
                    "code_expires_at": int(item.get("code_expires_at", 0))
                })
        except Exception as e:
            logger.error("DB | Failed to scan user table: %s", e)
    return users


def send_order_confirmation(req) -> dict:
    """Send order confirmation email via SMTP."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    SENDER = "madhumithamalu6@gmail.com"
    SUBJECT = f"Order Confirmed #{req.order_id} - E-Shop"

    items_html = "".join([
        f'<tr><td style="padding:8px 12px;border-bottom:1px solid #eee;">'
        f'{item.name}{" (" + item.size + ")" if item.size else ""}</td>'
        f'<td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;">{item.quantity}</td>'
        f'<td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right;">&#8377;{item.amount:.2f}</td></tr>'
        for item in req.items
    ])

    phone_row = f'<p style="margin:4px 0;font-size:14px;color:#555;"><strong>Phone:</strong> {req.phone}</p>' if req.phone else ''

    body_html = f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#ffffff;">
        <div style="background:linear-gradient(135deg,#0a0f1d,#1b2641);padding:30px;text-align:center;">
            <h1 style="color:#f0c14b;margin:0;font-size:24px;">&#128722; E-Shop Order Confirmed!</h1>
        </div>
        <div style="padding:30px;">
            <p style="font-size:16px;color:#333;">Hi <strong>{req.user_name}</strong>,</p>
            <p style="font-size:14px;color:#555;">Your order has been placed successfully.</p>
            <div style="background:#f8f9fa;border-radius:12px;padding:20px;margin:20px 0;border:1px solid #e9ecef;">
                <h3 style="margin:0 0 10px 0;color:#0a0f1d;">Order Details</h3>
                <p style="margin:4px 0;font-size:14px;color:#555;"><strong>Order ID:</strong> {req.order_id}</p>
                <p style="margin:4px 0;font-size:14px;color:#555;"><strong>Date:</strong> {req.order_date}</p>
                <p style="margin:4px 0;font-size:14px;color:#555;"><strong>Payment:</strong> {req.payment_method.upper()}</p>
                <p style="margin:4px 0;font-size:14px;color:#555;"><strong>Ship To:</strong> {req.shipping_name}, {req.shipping_address}</p>
                {phone_row}
            </div>
            <table style="width:100%;border-collapse:collapse;margin:20px 0;">
                <thead><tr style="background:#0a0f1d;color:#fff;">
                    <th style="padding:10px 12px;text-align:left;">Item</th>
                    <th style="padding:10px 12px;text-align:center;">Qty</th>
                    <th style="padding:10px 12px;text-align:right;">Amount</th>
                </tr></thead>
                <tbody>{items_html}</tbody>
                <tfoot><tr>
                    <td colspan="2" style="padding:12px;font-weight:bold;text-align:right;border-top:2px solid #0a0f1d;">Total Paid:</td>
                    <td style="padding:12px;font-weight:bold;text-align:right;color:#10b981;font-size:18px;border-top:2px solid #0a0f1d;">&#8377;{req.total_paid:.2f}</td>
                </tr></tfoot>
            </table>
            <div style="background:#e8f5e9;border-radius:8px;padding:15px;border-left:4px solid #10b981;">
                <p style="margin:0;font-size:14px;color:#2e7d32;"><strong>&#128230; Shipping Status:</strong> Your order is being processed. Tracking details will follow once shipped.</p>
            </div>
        </div>
    </div>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = req.to
    msg.attach(MIMEText(body_html, "html"))

    try:
        if not settings.SMTP_PASSWORD:
            logger.warning("SMTP_PASSWORD not configured. Cannot send email.")
            return {"message": "Email delivery skipped (no password)", "order_id": req.order_id}

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, settings.SMTP_PASSWORD)
            server.sendmail(SENDER, req.to, msg.as_string())
        logger.info("SMTP | Order confirmation email sent to: %s for order: %s", req.to, req.order_id)
        return {"message": "Order confirmation email sent", "order_id": req.order_id}
    except Exception as e:
        logger.error("SMTP | Unexpected error sending order email: %s", e)
        return {"message": "Email delivery failed", "order_id": req.order_id}
