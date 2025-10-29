import os
from loguru import logger
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from src.vector_db import load_vector_db
from sentence_transformers import CrossEncoder  #for reranking

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
logger.info("Loaded GOOGLE_API_KEY from .env")

if not GOOGLE_API_KEY:
    raise ValueError("Please set your GOOGLE_API_KEY in a .env file!")

# load vectorstore
vectorstore = load_vector_db()

# initialize Gemini model
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    verbose=True,
    google_api_key=GOOGLE_API_KEY
)

# initialize Cross-Encoder for reranking
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_documents(query, docs, top_n=3):
    """Rerank retrieved documents using a cross-encoder model.
    Args:
        query (str): The user query.
        docs (list): List of retrieved documents.
        top_n (int): Number of top documents to return after reranking.
    Returns:
        list: Reranked list of top_n documents.
    """
    if not docs:
        return []

    logger.info("Reranking retrieved documents...")
    pairs = [[query, doc.page_content] for doc in docs]
    scores = reranker.predict(pairs)

    # attach scores and sort
    for i, doc in enumerate(docs):
        doc.metadata["score"] = float(scores[i])
    reranked = sorted(docs, key=lambda x: x.metadata["score"], reverse=True)

    return reranked[:top_n]


def gemini_answer(query: str) -> str:
    logger.info("Retrieving top documents from vectorstore...")
    retrieved_docs = vectorstore.similarity_search(query, k=10)

    # add reranking 
    top_docs = rerank_documents(query, retrieved_docs, top_n=5)

    retrieved_text = "\n\n".join([doc.page_content for doc in top_docs])

    combined_prompt = f"""
    You are a helpful assistant for university information.
    Use the following context to answer the question clearly and concisely.

    Context:
    {retrieved_text}

    Question:
    {query}

    Answer:
    """

    logger.info("Generating Gemini LLM response using reranked context...")
    response = gemini_llm.invoke(combined_prompt)

    print("\n🤖 Gemini Answer:\n")
    return response.text
