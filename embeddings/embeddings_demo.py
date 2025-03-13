import os

from langchain_openai import OpenAIEmbeddings


from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv(),override=True)
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)
llm=OpenAIEmbeddings(api_key=OPENAI_API_KEY)

text=input("enter the question")
response=llm.embed_query(text)
print(response)