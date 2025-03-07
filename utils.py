import os
from langchain_chroma import Chroma
import shutil
import tempfile
import streamlit as st

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

from constant import embeddings, PERSIST_DIR, text_splitter


def get_vector_store():
    return Chroma(
        collection_name="uploaded_data",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR
    )


def delete_vector_store():
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)
        st.success("Document database cleared!")


def process_documents(uploaded_files):
    documents = []
    
    for file in uploaded_files:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name[file.name.rfind('.'):]) as tmp_file:
            tmp_file.write(file.getvalue())
            file_path = tmp_file.name
            
        try:
            # Load document based on file type
            if file.name.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif file.name.endswith('.txt'):
                loader = TextLoader(file_path)
                documents.extend(loader.load())
            elif file.name.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
                
        finally:
            # Clean up temporary file
            os.unlink(file_path)
    
    chunks = text_splitter.split_documents(documents)
    
    return chunks