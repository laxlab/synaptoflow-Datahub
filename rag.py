import chromadb
import os
from dotenv import load_dotenv
from groq import Groq

# Must run before reading env vars below, because bot.py imports this file
load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("synaptoflow_docs")
ai = Groq(api_key=os.environ["GROQ_API_KEY"])

def get_rag_answer(question, top_k=3, max_distance=1.0):
    # Chroma embeds the question the same way it embedded the docs,
    # then returns the closest chunks
    results = collection.query(query_texts=[question], n_results=top_k)
    docs = results["documents"][0]
    distances = results["distances"][0]  # smaller distance = more relevant

    # If nothing found, or the closest match is still too far off, be honest instead of guessing
    if not docs or min(distances) > max_distance:
        return "I'm not fully sure about that from the docs I have. You might want to check directly with the maintainer."

    context = "\n\n---\n\n".join(docs)
    prompt = f"""You are a helpful assistant answering questions about the SynaptoFlow project, using only the context below. If the context doesn't actually answer the question, say you're not sure rather than guessing.

Context:
{context}

Question: {question}"""

    response = ai.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content