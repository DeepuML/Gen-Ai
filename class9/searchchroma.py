import os
import requests
import numpy as np
from chromadb import HttpClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EURI_API_KEY = os.getenv("EURI_API_KEY")

# Initialize ChromaDB client
client = HttpClient(host="localhost", port=8000)
clibrary = client.get_or_create_collection("library")

# Function to generate embeddings from EURI API
def generate_embeddings(text_list):
    url = "https://api.euron.one/api/v1/euri/alpha/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EURI_API_KEY}"
    }
    payload = {
        "input": text_list,
        "model": "text-embedding-3-small"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    embeddings = [item['embedding'] for item in data['data']]

    return embeddings

# Function to search in ChromaDB
def search_chroma(query_text):
    query_embeddings = generate_embeddings([query_text])
    results = clibrary.query(
        query_embeddings=query_embeddings,
        n_results=5,
        include=["documents", "metadatas"]
    )

    print(f"\n🔍 Search results for: '{query_text}'")
    if results["documents"] and results["documents"][0]:
        print(f"Top {len(results['documents'][0])} results:\n")
        for i, doc in enumerate(results["documents"][0]):
            print(f"{i+1}. {doc}")
    else:
        print("No matching documents found.")
    
    return results

# Run search
search_chroma("I am deepu interested in machine learning, artificial intelligence, web development, and blockchain technology.")
