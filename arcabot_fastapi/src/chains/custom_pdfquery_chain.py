from models.query import PDFQueryInput
from chains.pdfquery_chain import PDFQueryChain



class PDFQueryChainCustom(PDFQueryChain):
    """PDFQuery Talentum subclass. Specific attributes."""

    def __init__(self, query: PDFQueryInput):
        super().__init__(
            openai_token=query.openai_token,
            collection=query.uid_chroma_collection,
            template=f"""
            {query.custom_prompt}

            {{context}}
            """
            )