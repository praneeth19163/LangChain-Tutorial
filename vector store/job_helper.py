import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

import os
from langchain_ollama import OllamaEmbeddings


llm = OllamaEmbeddings(model="gemma:2b")


document = TextLoader("job_listings.txt").load()
text_splitter= RecursiveCharacterTextSplitter(chunk_size=200,
                                              chunk_overlap=10)
chunks=text_splitter.split_documents(document)
db=Chroma.from_documents(chunks,llm)
retriever = db.as_retriever()

text = input("Enter the query")
embeddings_vector=llm.embed_query(text)

docs = db.similarity_search_by_vector(embeddings_vector)
print(docs)
for doc in docs:
    print(doc.page_content)



#     
# import os
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
#
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# llm=OpenAIEmbeddings(api_key=OPENAI_API_KEY)
#
# document = TextLoader("job_listings.txt").load()
# text_splitter= RecursiveCharacterTextSplitter(chunk_size=200,
#                                               chunk_overlap=10)
# chunks=text_splitter.split_documents(document)
# db=Chroma.from_documents(chunks,llm)
# retriever = db.as_retriever()
#
# text = input("Enter the query")
#
# docs = retriever.invoke(text)
#
# for doc in docs:
#     print(doc.page_content)