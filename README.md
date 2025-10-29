# 🎓 AskCUSATBot  
### RAG-based AI Chatbot for CUSAT Statistics Department Information  

## 📘 Overview  
**AskCUSATBot** is an intelligent, **Retrieval-Augmented Generation (RAG)** chatbot designed to provide quick and accurate answers about the **Department of Statistics**, Cochin University of Science and Technology (CUSAT).  

It integrates **LangChain**, **Hugging Face embeddings**, and **Google Gemini** to create a powerful conversational agent that retrieves verified departmental information and presents it in a human-like way through a **Streamlit** web interface.

## 🚀 Features  
- 🔍 **Context-aware answers** retrieved from verified departmental sources  
- 🧠 **Re-ranking mechanism** to improve the accuracy and relevance of retrieved information  
- 🤖 **Gemini-powered AI responses** for clear and natural language generation  
- 💾 **Chroma vector database** for efficient semantic search and retrieval  
- 💬 **Streamlit-based chat UI** for an interactive, conversational experience  
- ⚡ **Cached embeddings** to optimize speed and performance  
- 🔐 **Environment-based API key management** for secure configuration  

## 🏗️ Repository Structure  

```
AskCUSATBot/
│
├── src/
│   ├── rag.py              # Handles RAG logic using Gemini model
│   ├── vector_db.py        # Embedding creation and Chroma vector store
│
├── main.py                 # Streamlit web app
├── requirements.txt        # Required dependencies
├── README.md               # Project documentation
├── .gitignore              # Ignored files and folders
└── data/                   # Persisted Chroma vector database
```

## ⚙️ Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/snehakp1/AskCUSATBot.git
cd AskCUSATBot
```

### 2️⃣ Create a Virtual Environment  
```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables  
Rename the `.envexample` file to `.env` file and add your Google API key:  
```
GOOGLE_API_KEY=your_google_api_key_here
```

### 5️⃣ Run the Streamlit App  
```bash
streamlit run main.py
```

## 🧩 How It Works  

1. **Data Loading:**  
   The chatbot loads data from official CUSAT Statistics Department webpages (About, Courses, Faculty, etc.).  

2. **Embeddings Creation:**  
   Text is split into chunks and embedded using the **sentence-transformers/all-mpnet-base-v2** model.  

3. **Storage:**  
   Embeddings are stored in **ChromaDB** (`/data/chroma_db/`) for persistent retrieval.  

4. **Question Processing:**  
   When a user submits a query, the app retrieves the most relevant text chunks using **semantic similarity search**.  

5. **Response Generation:**  
   Retrieved context is passed to **Google Gemini 2.5 Flash** to generate a natural and precise answer.  

6. **Display:**  
   The Streamlit app shows the conversation in a chat-style interface.  


## 🧠 Tech Stack  

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Language Model** | Google Gemini 2.5 Flash |
| **Vector Store** | ChromaDB |
| **Embeddings** | Hugging Face (`sentence-transformers/all-mpnet-base-v2`) |
| **Framework** | LangChain |
| **Language** | Python 3.10+ |
| **Logging** | Loguru |
| **Environment Handling** | python-dotenv |


## 🌐 Data Sources  
AskCUSATBot currently retrieves and processes information from department websites and documents.  

## 💬 Example Queries  
- “Who is the Head of the Department?”  
- “What courses does the Statistics Department offer?”  
- “What are the eligibility criteria for M.Sc. Statistics?”  
- “Where is the department located?”  

## 🧰 Future Improvements  
- 🗂️ Support for departmental PDFs and circulars  
- 🗣️ Voice or multilingual support  
- 🧑‍🎓 Integration with student services (exam, timetable queries)  
- ☁️ Cloud deployment on Streamlit Cloud or Hugging Face Spaces  

## 👨‍💻 Authors  
Developed by **Sneha KP**  
Department of Statistics, CUSAT  
