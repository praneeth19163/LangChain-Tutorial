import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
prompt_template = ChatPromptTemplate.from_messages(
[
    ("system", "You are a python Expert.Answer any questions "
              "related to the Python ,if they ask about any program give the code properly with proper identation and list all the packages in code correctly.if the question is not related to agile return applogy kind of message"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
]
)

chain = prompt_template | llm

history_for_chain = ChatMessageHistory()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history"
)

print("Python Guide")

while True:
    question = input("Enter the question:")
    if question:
        response = (chain_with_history
                    .invoke({"input": question},
                            {"configurable":{
                                "session_id":"abc123"
                            }}))
        print(response.content)