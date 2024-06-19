from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import pinecone as PineconeLangChain
from langchain_pinecone import Pinecone
from main.applications_with_langchain.documentation_helper_app.constant import INDEX_NAME


def ingest_docs() -> None:
    loader = ReadTheDocsLoader(path="main/resources/langchain-docs/langchain.readthedocs.io/en/latest",
                               encoding="utf-8")
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} documents.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100,
                                                   separators=["\n\n", "\n", " ", ""])
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Splitted into {len(documents)} chunks")

    for doc in documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("main\\resources\\langchain-docs", "https:/")
        new_url = new_url.replace("\\", "/")

        doc.metadata.update({"source": new_url})

    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=INDEX_NAME)
    print("****** Added to Pinecone vectorstore vectors")


def run_ingestion():
    print("ingestion starting...")
    ingest_docs()
