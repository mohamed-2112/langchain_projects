import os

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override


class RAG(Application):

    @override
    def run(self, **kwargs):
        print("Retrieving...")
        embeddings = OpenAIEmbeddings()
        llm = ChatOpenAI()
        query = "What is Pinecone in machine learning?"
        chain = PromptTemplate.from_template(template=query) | llm
        result = chain.invoke(input={})
        print(result.content)
        vectorstore = PineconeVectorStore(index_name=os.environ["INDEX_NAME"], embedding=embeddings)
        retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
        retrival_chain = create_retrieval_chain(
            retriever=vectorstore.as_retriever(),
            combine_docs_chain=combine_docs_chain
        )
        result = retrival_chain.invoke(input={"input": query})
        print(result)
