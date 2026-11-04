import hashlib

from app.auth.schemas import AuthPurpose, EmailCodePurpose


def auth_failure_count(email: str, purpose: AuthPurpose) -> str:
    return f"auth:email:{email}:failures:{purpose}"


def email_send_interval(email: str, purpose: EmailCodePurpose) -> str:
    return f"auth:email:{email}:rate_limit:{purpose}"


def email_code(email: str, purpose: EmailCodePurpose) -> str:
    return f"auth:email:{email}:verification:{purpose}"


def session(session_token: str) -> str:
    token_hash = hashlib.sha256(session_token.encode()).hexdigest()

    return f"auth:session:{token_hash}"
