import os
import jwt
import requests
import time

from pdf2image import convert_from_bytes



CHATBOT_URL = os.getenv('CHATBOT_URL', '')


def _get_token_api() -> str:
    """Get JWT token."""
    now = int(time.time())
    to_encode = {
        "nbf" : now,
        "exp" : now + 1800,
    }
    return jwt.encode(to_encode, os.getenv('JWT_KEY'), algorithm='HS512')


def get_headers(file: bool = False) -> dict:
    headers =  {
        'Authorization': f'Bearer {_get_token_api()}',
        'Content-type': 'application/json'
    }
    if file:
        del headers['Content-type']

    return headers


def get_pdf_preview(pdf_content: bytes):
    return convert_from_bytes(
        pdf_content,
        first_page=1,
        last_page=1
        )


def chat_request(data: dict) -> tuple[str, bool]:
    response = requests.post(
        f'{CHATBOT_URL}/arcabot',
        json=data,
        headers=get_headers(),
        verify=False
        )

    error = False
    if response.status_code == 200:
        output_text = response.json()["result"]
    elif response.status_code == 401:
        output_text = { 'message': 'Incorrect API key provided.', }
    else:
        output_text = { 'message': 'An error occurred while processing your message. Please try again or rephrase your message.', }
        error = True

    return output_text, error


def file_request(uploaded_file, software: str, openai_token: str) -> tuple[str, bool]:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

    response = requests.post(
        f'{CHATBOT_URL}/update-db',
        files=files,
        headers=get_headers(file=True),
        data={'software': software, 'openai_token': openai_token,},
        verify=False
        )

    error = True
    if response.status_code == 200:
        error = False
        output_text = response.json()
    elif response.status_code == 401:
        output_text = { 'message': 'Incorrect API key provided.', }
    else:
        output_text = { 'message': 'An error occurred while processing your file.', }

    return output_text, error