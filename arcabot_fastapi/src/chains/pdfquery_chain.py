import os
import asyncio

from concurrent.futures import ThreadPoolExecutor

from langchain_chroma import Chroma
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_openai import (
    OpenAIEmbeddings,
    ChatOpenAI
    )
from langchain.chains import RetrievalQA
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    )

CHROMA_PATH = os.getenv('CHROMA_PATH', '')



class PDFQueryChain:
    """PDFQuery Superclass. Common functions."""

    _executor = ThreadPoolExecutor()

    def __init__(self, openai_token: str, collection: str, template: str):
        self._openai_token = openai_token
        self._collection = collection
        self._template = template

    def _get_chroma_db(self) -> Chroma:
        """
        Get ChromaDB object.
        Collection depends on input software query.
        """
        return Chroma(
            collection_name=self._collection,
            persist_directory=CHROMA_PATH,
            embedding_function=OpenAIEmbeddings(
                openai_api_key=self._openai_token
                )
        )


    async def _get_chroma_db_asynch(self) -> Chroma:
        """Avoid block using different thread."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, self._get_chroma_db)


    async def _get_chroma_retriever(self) -> VectorStoreRetriever:
        """Get Chroma Vector Retriever."""
        chroma_db = await self._get_chroma_db_asynch()
        return chroma_db.as_retriever(k=10)


    def _get_system_prompt(self) -> SystemMessagePromptTemplate:
        """Get System Prompt Template."""
        return SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["context"],
                template=self._template
            )
        )


    @staticmethod
    def _get_human_prompt() -> HumanMessagePromptTemplate:
        """Get Human Prompt Template."""
        return HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["question"],
                template="{question}"
            )
        )


    def _get_pdfquery_prompt(self) -> ChatPromptTemplate:
        """Get Chat Prompt Template."""
        return ChatPromptTemplate(
            input_variables=["context", "question"],
            messages=[self._get_system_prompt(), self._get_human_prompt()]
        )


    async def _init_vector_chain(self) -> RetrievalQA:
        """Init RetrievalQA."""
        return RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                openai_api_key=self._openai_token,
                model="gpt-4o",
                temperature=0,
                streaming=True,
                ),
            chain_type="stuff",
            retriever=await self._get_chroma_retriever(),
        )


    async def get_pdfquery_vector_chain(self) -> RetrievalQA:
        """Get RetrievalQA."""
        chain = await self._init_vector_chain()
        chain.combine_documents_chain.llm_chain.prompt = self._get_pdfquery_prompt()
        return chain