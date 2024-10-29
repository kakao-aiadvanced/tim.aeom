from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from typing import List

import bs4


def load(urls: List[str]) -> List[Document]:
    loader = WebBaseLoader(
        web_paths=urls,
        verify_ssl=False,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.aload()

    # log for debug
    # for doc in docs:
    #     print(f"[{doc.metadata}][{doc.page_content}]")

    return docs


def split(docs: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)


def vectorstore() -> VectorStore:
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]
    docs = split(load(urls))
    return Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))


def check_relevance(query: str, retrieved_chunk: Document) -> bool:
    system = """
        당신은 Retrieval Augmented Generation(RAG) 에서 찾아진(Retrieved) 사용자 쿼리(Query) 임베딩 결과와 유사한 정보(Document) 가 실제로 연관도(Relevancy) 를 가지는지 판단하는 봇입니다.
        아래 예시를 참고하여 주어진 query 에 대하여 각각의 retrieved_chunk 가 유사한지 relevancy 를 판단하여 "True" 혹은 "False" 로 나타내세요.
        결과는 Json 형태로 응답합니다.
        
        [예시] 
        # INPUT
        query: "Korean foods"
        retrieved_chunk: "Kimchi"
        
        # OUTPUT 
        "relevancy": true
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "query: {query}\n retrieved_chunk: {retrieved_chunk}")
        ]
    )

    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | JsonOutputParser()
    result = chain.invoke({"query": query, "retrieved_chunk": retrieved_chunk.page_content})

    return result['relevancy']


def check_hallucination(document: Document) -> bool:
    system = """
        당신은 생성된 답안에 Hallucination 이 존재하는지 평가하는 봇입니다.
        아래 예시를 참고하여 주어진 document 에 대하여 할루시네이션(hallucination) 이 존재하는지 판단하여 존재하면 "True" 존재하지 않으면 "False" 로 나타내세요.
        결과는 Json 형태로 응답합니다.

        [예시] 
        # INPUT
        document: Agent memory refers to the short-term memory module that records an agent's experiences in natural language,

        # OUTPUT 
        "hallucination": true
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "document: {document}")
        ]
    )

    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | JsonOutputParser()
    result = chain.invoke({"document": document})

    return result['hallucination']
