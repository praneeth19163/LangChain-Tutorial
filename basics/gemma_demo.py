#
#
# from langchain_community.chat_models import ChatOllama
# llm=ChatOllama(model="gemma:2b")
# question=input("enter the question")
# response=llm.invoke(question)
# print(response.content)
from langchain_ollama import ChatOllama  # Correct import

llm = ChatOllama(model="mistral:latest")

question = input("Enter the question: ")
response = llm.invoke(question)
print(response.content)
