
import faiss
import numpy as np
import requests

from llm_service import generate_response

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


def get_embedding(text):
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embedding"]


def split_text(text, chunk_size=1500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def create_rag_index(text):
    chunks = split_text(text)

    if not chunks:
        raise ValueError("No meeting text available.")

    embeddings = [get_embedding(chunk) for chunk in chunks]

    embeddings = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, chunks


def ask_meeting_question(question, index, chunks):

    question_embedding = np.array(
        [get_embedding(question)],
        dtype="float32"
    )

    distances, indices = index.search(question_embedding, k=2)

    context = "\n".join(
        chunks[i] for i in indices[0] if i < len(chunks)
    )

    prompt = f"""
Answer the question using only the meeting context below.

If the answer is not available, say:
Information not found in the meeting.

Meeting Context:
{context}

Question:
{question}

Answer:
"""

    return generate_response(prompt)
