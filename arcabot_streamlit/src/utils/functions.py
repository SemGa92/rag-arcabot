import os
import jwt
import requests
import time
import uuid



CHATBOT_URL = os.getenv("CHATBOT_URL")


def _get_token_api() -> str:
    """Get JWT token."""
    now = int(time.time())
    to_encode = {
        "nbf" : now,
        "exp" : now + 1800,
    }
    return jwt.encode(to_encode, os.getenv('JWT_KEY'), algorithm='HS512')


def make_chatbot_request(data: dict) -> tuple[str, bool]:
    headers = {
        'Authorization': f'Bearer {_get_token_api()}',
        'Content-type': 'application/json'
    }
    response = requests.post(
        CHATBOT_URL,
        json=data,
        headers=headers,
        verify=False
        )

    if response.status_code == 200:
        output_text = response.json()["result"]
        error = False
    else:
        output_text = """An error occurred while processing your message.
        Please try again or rephrase your message."""
        error = True

    return output_text, error


def get_sw_dir(software: str) -> str:
    return os.path.join("software", software)
