from typing import List
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from llm import llm
from datasource import vectorstore

llm = llm()
vectorstore = vectorstore()
retriever = vectorstore.retriever


# Retrieval Grader
def check_relevant(question: str, doc: Document) -> bool:
    system = """You are a grader assessing relevance
        of a retrieved document to a user question. If the document contains keywords related to the user question,
        grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
        Provide the binary score as a JSON with a single key 'score' and no premable or explanation.
        """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "question: {question}\n\n document: {document} "),
        ]
    )
    retrieval_grader = prompt | llm | JsonOutputParser()
    doc_txt = doc.page_content
    result = retrieval_grader.invoke({"question": question, "document": doc_txt})
    return result["score"] == "yes"


# Hallucination Grader
def check_hallucination(docs: List[Document], generation: str) -> bool:
    system = """You are a grader assessing whether
        an answer is grounded in / supported by a set of facts. Give a binary 'yes' or 'no' score to indicate
        whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a
        single key 'score' and no preamble or explanation."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "documents: {documents}\n\n answer: {generation} "),
        ]
    )

    hallucination_grader = prompt | llm | JsonOutputParser()
    result = hallucination_grader.invoke({"documents": docs, "generation": generation})
    return result["score"] == "yes"


# Answer Grader
def check_answer(question: str, generation: str) -> bool:
    system = """You are a grader assessing whether an
        answer is useful to resolve a question. Give a binary score 'yes' or 'no' to indicate whether the answer is
        useful to resolve a question. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "question: {question}\n\n answer: {generation} "),
        ]
    )

    answer_grader = prompt | llm | JsonOutputParser()
    result = answer_grader.invoke({"question": question, "generation": generation})
    return result["score"] == "yes"
