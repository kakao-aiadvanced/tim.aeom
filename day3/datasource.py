from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever, VectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from tavily import TavilyClient
from llm import llm


class ChromaVectorStore:
    vectorstore: VectorStore
    retriever: VectorStoreRetriever

    def __init__(self, urls: List[str]):
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )
        doc_splits = text_splitter.split_documents(docs_list)

        # Add to vectorDB
        self.vectorstore = Chroma.from_documents(
            documents=doc_splits,
            collection_name="rag-chroma",
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )
        self.retriever = self.vectorstore.as_retriever()


_llm = llm()
_travily = TavilyClient(api_key='API_KEY')
_vectorstore = ChromaVectorStore(urls=[
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
])


def vectorstore():
    return _vectorstore


def travily():
    return _travily


def route_datasource(question: str) -> str:
    system = """You are an expert at routing a user question to a vectorstore or web search.
    Use the vectorstore for questions on LLM agents, prompt engineering, and adversarial attacks.
    You do not need to be stringent with the keywords in the question related to these topics.
    Otherwise, use web-search. Give a binary choice 'web_search' or 'vectorstore' based on the question.
    Return the a JSON with a single key 'datasource' and no premable or explanation. Question to route"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "question: {question}"),
        ]
    )

    question_router = prompt | _llm | JsonOutputParser()
    result = question_router.invoke({"question": question})
    return result["datasource"]
