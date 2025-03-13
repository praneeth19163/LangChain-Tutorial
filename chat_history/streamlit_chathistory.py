import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
prompt_template = ChatPromptTemplate.from_messages(
[
    ("system","You are a python Expert.Answer any questions "
              "related to the Python ,if they ask about any program give the code properly with proper identation and list all the packages in code correctly.if the question is not related to python return applogy kind of message"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
]
)

chain = prompt_template | llm

history_for_chain = StreamlitChatMessageHistory()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id : history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history"
)

st.title("Python Guide")

input = st.text_input("Enter the question:")

if input:
    response = chain_with_history.invoke({"input":input},
                                         {"configurable":{"session_id":"abc123"}})
    st.write(response.content)

st.write("HISTORY")
st.write(history_for_chain)