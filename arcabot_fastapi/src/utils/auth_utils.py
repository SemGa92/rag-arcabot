import os
import jwt

from fastapi import Header, HTTPException


JWT_KEY = os.getenv("JWT_KEY", "")


def _jwt_validation(token: str) -> None:
    """JWT validation"""
    try:
        jwt.decode(token, JWT_KEY, algorithms=['HS512'])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Signature expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token.")


def my_auth(authorization: str = Header(None)) -> None:
    """Auth manager"""
    if not authorization:
        raise HTTPException(status_code=403, detail="Invalid auth method.")

    token = authorization.split()[1] if " " in authorization else None
    if not token:
        raise HTTPException(status_code=403, detail="Invalid auth method.")

    _jwt_validation(token)
