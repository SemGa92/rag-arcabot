from pydantic import BaseModel
from models import SoftwareEnum



class PDFQueryInput(BaseModel):
    """Input Query Pydantic Model"""
    text: str
    software: SoftwareEnum
    openai_token: str
    custom_prompt: str
    uid_chroma_collection: str


class PDFQueryOutput(BaseModel):
    """Output Query Pydantic Model"""
    query: str
    result: str
