import os
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
prompt_template = ChatPromptTemplate.from_messages(
[
    ("system","You are a python Expert.Answer any questions "
              "related to the Python ,if they ask about any program give the code properly with proper identation and list all the packages in code correctly.if the question is not related to agile return applogy kind of message"),
    ("human", "{input}")
]
)

st.title("Python Guide")

input = st.text_input("Enter the question:")
chain = prompt_template | llm

if input:
    response = chain.invoke({"input":input})
    st.write(response.content)