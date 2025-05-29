import chainlit as cl
import os
import pandas as pd
from models.rag_query_engine import generate_rag_answer
from models.embedding_generator import embed_excel_to_faiss

# Caching the model and FAISS/SQLite resources
model_pipeline = None
index = None
documents = None

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

@cl.on_chat_start
async def start():
    load_model_pipeline()
    load_faiss_resources()

    res = await cl.AskActionMessage(
        content="Welcome to RAGEX-RAG Only Chatbot",
        actions=[
            cl.Action(name="upload", label="📁 Upload Excel/CSV File", payload={}),
            cl.Action(name="ask", label="❓ Ask a Question", payload={})
        ]
    ).send()

    if res.get("value") == "upload":
        await cl.Message(content="📁 Please upload your Excel or CSV file.").send()

        file = await cl.AskFileMessage(
            content="Upload your Excel/CSV file 📄",
            accept=[".xlsx", ".csv"],
            max_size_mb=20,
            timeout=180,
        ).send()

        if not file.name.endswith(('.csv', '.xlsx')):
            await cl.Message(content="❌ Unsupported file format.").send()
            return

        save_path = os.path.join("data", "incident_data.csv")
        os.makedirs("data", exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(await file.read())

        await cl.Message(content="✅ File uploaded successfully!").send()

        embed_excel_to_faiss(save_path)
        load_faiss_resources()

        await cl.Message(content="🔍 Data embedded. Ask your questions!").send()

    elif res.get("value") == "ask":
        await cl.Message(content="❓ What would you like to ask about the data?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_query = message.content

    load_model_pipeline()
    load_faiss_resources()

    try:
        result = generate_rag_answer(user_query)
        final = f"📚 **Answer from RAG:**\n{result}"
    except Exception as e:
        final = f"❌ Error generating RAG response:\n{e}"

    await cl.Message(content=final).send()
