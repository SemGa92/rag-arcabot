from chains.pdfquery_chain import PDFQueryChain



class PDFQueryChainGeneric(PDFQueryChain):
    """PDFQuery Talentum subclass. Specific attributes."""

    def __init__(self, openai_token: str, software: str):
        super().__init__(
            openai_token=openai_token,
            collection=software,
            template=f"""
            You are a Customer Service Assistant knowledgeable {software}, an HR software developed by Arca24.
            You can help users answering questions only about {software} features and functionalities.
            Use the following context to answer questions. Be as detailed as possible, but don't make up any information that's not from the context.
            If you don't know an answer, say you don't know. You must not answer questions not related to {software}.

            {{context}}
            """
            )