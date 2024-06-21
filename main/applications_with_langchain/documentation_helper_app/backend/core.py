from builtins import int
from typing import Any

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeLangChain

from main.applications_with_langchain.application_interface import Application
from main.applications_with_langchain.documentation_helper_app.constant import INDEX_NAME
from main.utils.utils import override


class DocHelper(Application):
    @override
    def run(self, **kwargs):
        res = self.run_llm(query=kwargs["query"], chat_history=kwargs["chat_history"])
        print(res)
        return res

    def run_llm(self, query: str, chat_history: list = []) -> Any:
        embeddings = OpenAIEmbeddings()
        docsearch = PineconeLangChain.from_existing_index(
            index_name=INDEX_NAME, embedding=embeddings
        )
        chat = ChatOpenAI(verbose=True, temperature=0)
        # qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=docsearch.as_retriever(),
        #                                  return_source_documents=True)
        qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True)
        return qa({"question": query, "chat_history": chat_history})
