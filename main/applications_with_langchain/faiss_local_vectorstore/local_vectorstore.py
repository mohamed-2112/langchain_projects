from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS


class LocalVector(Application):
    @override
    def run(self, **kwargs):
        print("Hello, from the Faiss local vectorstore with pdf application!")
        pdf_path = "main/resources/Selection_of_Features_and_Classifiers.pdf"
        loader = PyPDFLoader(file_path=pdf_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
        docs = text_splitter.split_documents(documents=documents)
        print(len(docs))
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local("main/resources/faiss_index_react")
