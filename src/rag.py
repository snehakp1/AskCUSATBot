import os
from loguru import logger
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from src.vector_db import load_vector_db
from sentence_transformers import CrossEncoder  # for reranking


load_dotenv()
logger.info("Environment variables loaded.")

# Load vectorstore
vectorstore = load_vector_db()

# Initialize Cross-Encoder for reranking
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_documents(query, docs, top_n=3):
    """Rerank retrieved documents using a cross-encoder model."""
    if not docs:
        return []

    logger.info("Reranking retrieved documents...")
    pairs = [[query, doc.page_content] for doc in docs]
    scores = reranker.predict(pairs)

    for i, doc in enumerate(docs):
        doc.metadata["score"] = float(scores[i])
    reranked = sorted(docs, key=lambda x: x.metadata["score"], reverse=True)

    return reranked[:top_n]


def gemini_answer(query: str, api_key: str) -> str:
    """
    Generate an answer using the Gemini model.
    Args:
        query (str): The user query.
        api_key (str): Google Gemini API key entered by the user.
    """
    if not api_key:
        raise ValueError("Please provide a valid Google Gemini API key!")

    # Initialize Gemini model with the user’s API key
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        verbose=True,
        google_api_key=api_key
    )

    logger.info("Retrieving top documents from vectorstore...")
    retrieved_docs = vectorstore.similarity_search(query, k=10)

    # Rerank top documents
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
