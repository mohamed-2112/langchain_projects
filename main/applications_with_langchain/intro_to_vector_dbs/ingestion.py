import os

from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


class VectorDbs(Application):
    @override
    def run(self, **kwargs):
        print("Hello Ingesting!")
        loader = TextLoader("main/resources/mediumblog1.txt")
        document = loader.load()
        print("splitting....")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(document)
        print(f"created {len(texts)} chunks")

        embeddings = OpenAIEmbeddings()
        print("ingesting...")
        PineconeVectorStore.from_documents(texts, embeddings, index_name=os.environ['INDEX_NAME'])
        print("finish")
