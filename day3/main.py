import streamlit as st

from langgraph.constants import END
from langgraph.graph import StateGraph

from graph import GraphState, web_search, retrieve, grade_documents, generate, \
    grade_generation_v_documents_and_question, route_question, decide_to_generate

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("websearch", web_search)  # web search
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae

# Build graph
workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "websearch",
        "vectorstore": "retrieve",
    },
)

workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch",
    },
)

# Compile
app = workflow.compile()

# # Test
# inputs = {"question": "Where does Messi play right now?"}
# for output in app.stream(inputs):
#     for key, value in output.items():
#         print(f"{key}: {value}")

st.set_page_config(
    page_title="Research Assistant",
    page_icon=":orange_heart:",
)
st.title("Research Assistant powered by OpenAI")

input_topic = st.text_input(
    ":female-scientist: Enter a topic",
    value="Superfast Llama 3 inference on Groq Cloud",
)

generate_report = st.button("Generate Report")

if generate_report:
    with st.spinner("Generating Report"):
        inputs = {"question": input_topic}
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"Finished running: {key}:")
        final_report = value["generation"]
        st.markdown(final_report)

st.sidebar.markdown("---")
if st.sidebar.button("Restart"):
    st.session_state.clear()
    st.experimental_rerun()
