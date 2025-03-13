import os

from langchain_ollama import OllamaEmbeddings


from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv(),override=True)
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)
llm=OllamaEmbeddings(model="llama3.2:latest")

text=input("enter the question")
response=llm.embed_query(text)
print(response)