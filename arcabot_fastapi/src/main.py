import os
import aiofiles
import openai

from fastapi import (
    FastAPI,
    Depends,
    File,
    Form,
    UploadFile,
    HTTPException,
    )

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from chains.custom_pdfquery_chain import PDFQueryChainCustom
from models.query import PDFQueryInput, PDFQueryOutput

from utils.auth_utils import my_auth
from utils.async_utils import async_retry



app = FastAPI(
    title="ARCA-BOT",
    description="ARCA24 HR TECH FACTORY BOT",
)



@async_retry(max_retries=1, delay=1)
async def invoke_agent_with_retry(query: PDFQueryInput) -> dict:
    """
    Retry the agent if a tool fails to run.
    This can help when there are intermittent connection issues
    to external APIs.
    """
    my_chain = await PDFQueryChainCustom(query).get_pdfquery_vector_chain()
    return await my_chain.ainvoke({"query": query.text})


@app.get("/")
async def get_status():
    """Health root."""
    return {"status": "running"}


@app.post("/arcabot")
async def pdfquery_agent(
    query: PDFQueryInput,
    auth=Depends(my_auth)
) -> PDFQueryOutput:
    """Invoke the agent with the input query."""
    query_response = await invoke_agent_with_retry(query)
    return query_response


@app.post("/update-db")
async def upload_file(
    file: UploadFile = File(...),
    software: str = Form(...),
    openai_token: str = Form(...),
    auth=Depends(my_auth)
) -> dict:

    upload_dir = '/tmp/uploads'
    os.makedirs(upload_dir, exist_ok=True)

    content = await file.read()
    async with aiofiles.open(f"{upload_dir}/{file.filename}", "wb") as f:
        await f.write(content)

    loader = PyPDFLoader(f"{upload_dir}/{file.filename}")
    pages = loader.load_and_split()

    embedding = OpenAIEmbeddings(openai_api_key=openai_token)

    try:
        _ = Chroma.from_documents(
            pages,
            embedding,
            collection_name=software,
            persist_directory='chroma_data',
            )
    except openai.AuthenticationError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
            )

    return {"message": "DB updated successfully"}