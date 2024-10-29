from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from rag import vectorstore, check_relevance

if __name__ == '__main__':
    query = "agent memory"
    retriever = vectorstore().as_retriever(search_type="similarity", search_kwargs={"k": 6})
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model="gpt-4o-mini")


    def filter_relevancy(docs):
        return list(filter(lambda doc: check_relevance(query, doc), docs))


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
            {"context": retriever | filter_relevancy | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    result = rag_chain.invoke("agent memory")
    print(result)
