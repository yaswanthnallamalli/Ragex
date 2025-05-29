import chainlit as cl
import os
import sqlite3
import pandas as pd
from models.hybrid_query_engine import hybrid_query
from models.rag_query_engine import generate_rag_answer
from models.embedding_generator import embed_excel_to_faiss

# Caching the model and FAISS/SQLite resources
model_pipeline = None
index = None
documents = None

def is_structured_query(query):
    keywords = ["total", "count", "list", "sum", "show", "how many", "filter", "greater than"]
    return any(kw in query.lower() for kw in keywords)

def load_model_pipeline():
    global model_pipeline
    if model_pipeline is None:
        from models.load_model import load_mistral_pipeline
        model_pipeline = load_mistral_pipeline()
        print("✅ Mistral model loaded and cached.")

def load_faiss_resources():
    global index, documents
    import faiss
    import pickle

    index_path = "vector_store/faiss_index/index.faiss"
    text_path = "vector_store/faiss_index/texts.pkl"

    if not os.path.exists(index_path) or not os.path.exists(text_path):
        print("⚠️ FAISS index or text data not found.")
        return

    index = faiss.read_index(index_path)
    with open(text_path, "rb") as f:
        documents = pickle.load(f)
    print("✅ FAISS index and documents loaded and cached.")

def save_excel_to_sqlite(file_path: str, db_path: str = "vector_store/excel_db.sqlite"):
    df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("data", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ SQLite DB created at {db_path}")

@cl.on_chat_start
async def start():
    load_model_pipeline()
    load_faiss_resources()

    res = await cl.AskActionMessage(
        content="Welcome to RAGEX - Conversational Chatbot",
        actions=[
            cl.Action(name="upload", label="📁 Upload Excel/CSV File", payload={}),
            cl.Action(name="ask", label="❓ Ask a Question", payload={})
        ]
    ).send()

    if res.get("value") == "upload":
        await cl.Message(content="📁 Please upload your Excel or CSV file to begin.").send()

        file = await cl.AskFileMessage(
            content="Upload your Excel/CSV file 📄",
            accept=[".xlsx", ".csv"],
            max_size_mb=20,
            timeout=180,
        ).send()

        if not file.name.endswith(('.csv', '.xlsx')):
            await cl.Message(content="❌ Unsupported file format. Please upload CSV or Excel.").send()
            return

        save_path = os.path.join("data", "incident_data.csv")
        os.makedirs("data", exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(await file.read())

        await cl.Message(content="✅ File 'incident_data.csv' uploaded and saved!").send()

        # Generate embeddings and update FAISS
        embed_excel_to_faiss(save_path)
        load_faiss_resources()  # Reload new FAISS data

        # Create SQLite DB for hybrid query
        save_excel_to_sqlite(save_path)

        await cl.Message(content="🔍 Data embedded into RAG and SQLite DB created. Ask me anything!").send()

    elif res.get("value") == "ask":
        await cl.Message(content="❓ What would you like to ask about the data?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_query = message.content

    if user_query.lower() == "upload file":
        await cl.Message(content="📁 Please upload your Excel or CSV file to begin.").send()
    else:
        load_model_pipeline()
        load_faiss_resources()

        if is_structured_query(user_query):
            try:
                result = hybrid_query(user_query, "vector_store/excel_db.sqlite")
                final = f"🧮 **Answer from SQL:**\n{result}"
            except Exception as e:
                final = f"❌ Error querying database:\n{e}"
        else:
            result = generate_rag_answer(user_query)
            final = f"📚 **Answer from RAG:**\n{result}"

        await cl.Message(content=final).send()