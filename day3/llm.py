from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def llm():
    return _llm


def generate_with_context(question: str, context: List[Document]) -> str:
    system = """You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
        Use three sentences maximum and keep the answer concise"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "question: {question}\n\n context: {context} "),
        ]
    )

    rag_chain = prompt | _llm | StrOutputParser()

    generation = rag_chain.invoke({"context": context, "question": question})

    return generation
