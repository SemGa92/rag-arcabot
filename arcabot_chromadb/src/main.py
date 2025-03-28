import os

from utils import sw_map
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings



def _load_pdf_into_chroma(embedding: OpenAIEmbeddings, software: dict) -> None:
    loader = PyPDFLoader(software['path'])
    pages = loader.load_and_split()

    _ = Chroma.from_documents(
        pages,
        embedding,
        collection_name=software['collection'],
        persist_directory=os.getenv('CHROMA_PATH', ''),
        )



if __name__ == '__main__':
    if os.getenv('UPDATE_POLICY'):
        embedding = OpenAIEmbeddings(
            openai_api_key=os.getenv('OPENAI_API_KEY', '')
            )

        for sw in sw_map:
            _load_pdf_into_chroma(embedding, sw)
