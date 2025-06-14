import os
import requests
from dotenv import load_dotenv
import numpy as np
from chromadb import HttpClient

# Load environment variables from .env file
load_dotenv()
EURI_API_KEY = os.getenv("EURI_API_KEY")

# Initialize ChromaDB client
client = HttpClient(host="localhost", port=8000)
clibrary = client.get_or_create_collection("library")
print(client)

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
    
    embeddings = [item['embedding'] for item in data["data"]]

    print(f"Generated {len(embeddings)} embeddings.")
    print(f"Shape of each embedding: {np.array(embeddings[0]).shape}")
    print(f"First 5 values of first embedding: {embeddings[0][:5]}")
    
    for i, emb in enumerate(embeddings[:3]):
        print(f"Norm of embedding {i}: {np.linalg.norm(emb)}")
    
    return embeddings

documents = [
    "my name is deepu currently persuing btechh in computer science and engineering",
    "I am interested in machine learning and artificial intelligence",
    "I love to play cricket and watch movies",
    "I am currently learning about databases and data structures",
    "I enjoy solving problems and coding challenges",
    "I am passionate about technology and innovation",
    "I like to read books on science fiction and fantasy",
    "I am a member of the college coding club and participate in hackathons",
    "I am looking for internship opportunities in the field of software development",
    "I am a quick learner and adapt to new technologies easily",
    "I have experience in Python, Java, and C++ programming languages",
    "I am working on a project related to natural language processing",
    "I am interested in exploring cloud computing and big data technologies",
    "I am a team player and enjoy collaborating with others",
    "I am also learning Web development and improving my skills",
    "I am excited about the future of technology and its impact on society",
    "I am also intersetd in WEB3 and blockchain technology",
    "I am currently working on a project related to machine learning and data analysis"
]

all_embeddings = generate_embeddings(documents)
# print(all_embeddings)
# print(len(all_embeddings))

enumerate(zip(documents, all_embeddings))

for idx, (doc, emb) in enumerate(zip(documents, all_embeddings)):
    clibrary.add(
        ids=[f"doc_{idx}"],
        documents=[doc],
        embeddings=[emb],
        metadatas=[{"source": "euri"}]
    )

print("Documents and embeddings added to the library collection.")

# Query the collection to verify
query_result = clibrary.query(
    query_embeddings=[all_embeddings[0]],
    n_results=5,
    include=["documents", "embeddings", "metadatas"]
)


print(("Query results:", query_result))

# Print the query results
for i, (doc, emb) in enumerate(zip(query_result['documents'][0], query_result['embeddings'][0])):
    print(f"Result {i+1}:")
    print(f"Document: {doc}")
    print(f"Embedding: {emb[:5]}...")  # Print first 5 values of the embedding
    print(f"Metadata: {query_result['metadatas'][0][i]}")
    print() 
    
# print(f"Printing the doccuments from the ChromaDB")
# print(clibrary.get(include=["documents","embeddings", "metadatas"]))  
 