# import os
#
# from langchain_openai import ChatOpenAI
#
#
# from dotenv import load_dotenv,find_dotenv
# load_dotenv(find_dotenv(),override=True)
# OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
# print(OPENAI_API_KEY)
# llm=ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
#
# question=input("enter the question")
# response=llm.invoke(question)
# print(response.content)
#
# from langchain_openai import ChatOpenAI
# import os
# from dotenv import load_dotenv, find_dotenv
#
# # Load environment variables
# load_dotenv(find_dotenv(), override=True)
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#
# # Initialize ChatOpenAI with correct response_format
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     api_key=OPENAI_API_KEY,
#     temperature=0.7,
#     max_tokens=500,  # Correct value
# )
#
# question = input("Enter the question: ")
# response = llm.invoke(question)
# print(response.content)
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0.7
)

# Pass messages when invoking
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "What is LangChain?"}
]

response = llm.invoke(messages)
print(response.content)
