import os
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

st.title("Chat with OpenAI")

question = st.text_input("Enter your question:")

if question:
    response = llm.invoke(question)
    st.write(response.content)
