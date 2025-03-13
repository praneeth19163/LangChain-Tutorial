import os
from langchain_ollama import OllamaEmbeddings


embeddings = OllamaEmbeddings(model="llama3.2:latest")

response = embeddings.embed_documents(
    [
        "I love playing video games",
        "I am going to the movie",
        "I love coding",
        "Hello World!"
    ]
)

print(len(response))
print(response[0])
