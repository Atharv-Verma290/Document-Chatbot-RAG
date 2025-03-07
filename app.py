import streamlit as st

from constant import thread
from utils import get_vector_store, delete_vector_store, process_documents
from graph import create_graph


# vector_store = None
# if not vector_store:
#     vector_store = get_vector_store()

# Set page configuration
st.set_page_config(page_title="Document Chat Assistant", layout="wide")

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'vector_store' not in st.session_state:
    st.session_state.vector_store = get_vector_store()

if 'graph' not in st.session_state:
    graph = create_graph()
    st.session_state.graph = graph



with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    uploaded_files = st.file_uploader(
        "Upload your documents",
        accept_multiple_files=True,
        type=['pdf', 'txt', 'docx']
    )

    # Add a clear database button
    if st.button("Clear Document Database"):
        if st.session_state.vector_store is not None:
            delete_vector_store()
            st.session_state.vector_store = get_vector_store()
        else:
            st.warning("Vector store is not initialized.")


    if uploaded_files and api_key:
        with st.spinner("Processing documents..."):
            # Process documents
            chunks = process_documents(uploaded_files)

            if st.session_state.vector_store is None:
                st.session_state.vector_store = get_vector_store()
            # Add new documents to existing vector store
            st.session_state.vector_store.add_documents(chunks)
            
            st.success(f"Processed {len(chunks)} document chunks")


# Title and description
st.title("📚 Document Chat Assistant")
st.write("Upload your documents and chat with them!")

# Main chat interface
if st.session_state.vector_store is not None and api_key:

    # Chat interface
    st.header("Chat with your documents")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    # Chat input
    if input_message := st.chat_input("Ask a question about your documents"):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": input_message})

        with st.chat_message("user"):
            st.write(input_message)


        # Get response from chain
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.graph.invoke(
                    {"messages": [{"role": "user", "content": input_message}]}, config=thread
                )
                final_answer = response["messages"][-1].content
                st.write(final_answer)
                
        # Add assistant response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": final_answer
        })

else:
    st.info("Please upload documents and provide an OpenAI API key to start chatting.")

