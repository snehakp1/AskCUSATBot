import os
import streamlit as st
from loguru import logger
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


# Data source URLs
urls = [
            "https://www.cusat.ac.in/stats.php",
            "https://stats.cusat.ac.in/index.php/About",
            "https://stats.cusat.ac.in/index.php/Courses",
            "https://stats.cusat.ac.in/index.php/Faculty",
        ]

@st.cache_resource 
def load_embedding():
    embeddings =HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return embeddings

logger.info("Loading embeddings...")
embeddings = load_embedding()


def create_vector_db():
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(documents)
    print(f"Number of documents after splitting: {len(texts)}")

    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="./data/chroma_db"
    )
    
    return vectorstore

def load_vector_db():
    if not os.path.exists("data/chroma_db"):
        logger.info("Creating new vectorstore...")
        create_vector_db()
    return Chroma(persist_directory="./data/chroma_db", embedding_function=embeddings)

    