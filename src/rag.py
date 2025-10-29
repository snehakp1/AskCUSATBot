import os
from loguru import logger
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from src.vector_db import load_vector_db

load_dotenv()  
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
logger.info("Loaded GOOGLE_API_KEY from .env")

if not GOOGLE_API_KEY:
    raise ValueError("Please set your GOOGLE_API_KEY in a .env file!")

vectorstore = load_vector_db()

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    verbose=True,
    google_api_key=GOOGLE_API_KEY
)



def gemini_answer(query: str) -> str:

    logger.info("retrieving information from vectorstore")
    results = vectorstore.similarity_search(query, k=5)
    retrieved_text = "\n\n".join([doc.page_content for doc in results])

    combined_prompt = f"""
    You are a helpful assistant for university information.
    Use the following context to answer the question clearly and concisely.

    Context:
    {retrieved_text}

    Question:
    {query}

    Answer:
    """

    logger.info("Generating Gemini LLM response using retrieved context")
    response = gemini_llm.invoke(combined_prompt)
    

    print("\n🤖 Gemini Answer:\n")
    return response.text


