from fastapi import FastAPI, Depends

from chains.talentum_pdfquery_chain import PDFQueryChainTalentum
from chains.jobarch_pdfquery_chain import PDFQueryChainJobArch
from chains.ngage_pdfquery_chain import PDFQueryChainNgage
from chains.jobcourier_pdfquery_chain import PDFQueryChainJobCourier

from models.query import PDFQueryInput, PDFQueryOutput

from utils.auth_utils import my_auth
from utils.async_utils import async_retry



app = FastAPI(
    title="ARCA-BOT",
    description="ARCA24 HR TECH FACTORY BOT",
)


CHAIN_SELECTOR = {
    'Talentum': PDFQueryChainTalentum(),
    'JobArch': PDFQueryChainJobArch(),
    'Ngage': PDFQueryChainNgage(),
    'JobCourier': PDFQueryChainJobCourier(),
}


@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str, software: str) -> dict:
    """
    Retry the agent if a tool fails to run.
    This can help when there are intermittent connection issues
    to external APIs.
    """
    my_chain = await CHAIN_SELECTOR.get(software).get_pdfquery_vector_chain()
    return await my_chain.ainvoke({"query": query})


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
    query_response = await invoke_agent_with_retry(query.text, query.software)
    return query_response