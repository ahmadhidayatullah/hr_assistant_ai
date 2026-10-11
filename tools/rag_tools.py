"""
RAG Tools for HR Assistant AI.
Handles document loading, embedding, vector storage, and semantic search
for company policy documents.
"""
import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import (
    KNOWLEDGE_BASE_DIR, UPLOAD_DIR, VECTORSTORE_DIR,
    EMBEDDING_MODEL, FALLBACK_EMBEDDING_MODELS, CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVAL_TOP_K
)

from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)

try:
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
except ImportError:
    UnstructuredMarkdownLoader = None

import streamlit as st

_vectorstore: Optional[FAISS] = None
_embeddings = None
_last_embeddings_key = None
_current_embedding_model = None


def get_embeddings(api_key: str, model_name: Optional[str] = None) -> GoogleGenerativeAIEmbeddings:
    global _embeddings, _last_embeddings_key, _current_embedding_model
    target_model = model_name or EMBEDDING_MODEL
    if _embeddings is None or _last_embeddings_key != api_key or _current_embedding_model != target_model:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model=target_model,
            google_api_key=api_key
        )
        _last_embeddings_key = api_key
        _current_embedding_model = target_model
    return _embeddings


def load_documents() -> List[Document]:
    documents = []
    dirs_to_scan = [KNOWLEDGE_BASE_DIR, UPLOAD_DIR]
    
    for directory in dirs_to_scan:
        if not os.path.exists(directory):
            continue
            
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                try:
                    loader = None
                    if ext == '.pdf':
                        loader = PyPDFLoader(file_path)
                    elif ext in ('.md', '.txt'):
                        loader = TextLoader(file_path, encoding='utf-8')
                    else:
                        continue
                        
                    if loader:
                        docs = loader.load()
                        for doc in docs:
                            doc.metadata['source_filename'] = file
                            doc.metadata['file_type'] = ext
                        documents.extend(docs)
                        print(f"Loaded: {file_path}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    
    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""]
    )
    raw_chunks = splitter.split_documents(documents)
    # Filter out empty or trivial divider chunks (e.g. '---')
    return [c for c in raw_chunks if len(c.page_content.strip()) > 10]


def init_vectorstore(api_key: str, force_rebuild: bool = False) -> FAISS:
    global _vectorstore
    
    if _vectorstore is not None and not force_rebuild:
        return _vectorstore

    documents = load_documents()
    chunks = split_documents(documents)

    # Candidate models to try in order of priority
    models_to_try = [EMBEDDING_MODEL] + [m for m in FALLBACK_EMBEDDING_MODELS if m != EMBEDDING_MODEL]
    last_error = None

    for model_name in models_to_try:
        try:
            embeddings = get_embeddings(api_key, model_name=model_name)
            
            if os.path.exists(VECTORSTORE_DIR) and not force_rebuild:
                try:
                    # allow_dangerous_deserialization is required for newer FAISS versions
                    _vectorstore = FAISS.load_local(
                        VECTORSTORE_DIR, 
                        embeddings, 
                        allow_dangerous_deserialization=True
                    )
                    return _vectorstore
                except Exception as e:
                    print(f"Error loading vector store from disk with {model_name}: {e}")

            if not chunks:
                _vectorstore = FAISS.from_texts(["No documents loaded."], embeddings)
                return _vectorstore

            _vectorstore = FAISS.from_documents(chunks, embeddings)
            os.makedirs(VECTORSTORE_DIR, exist_ok=True)
            _vectorstore.save_local(VECTORSTORE_DIR)
            print(f"Successfully initialized vector store with model: {model_name}")
            return _vectorstore

        except Exception as e:
            last_error = e
            print(f"Embedding model '{model_name}' failed: {e}. Trying next fallback...")
            continue

    raise RuntimeError(f"Gagal menginisialisasi Vector Store dengan model yang tersedia: {last_error}")


def add_uploaded_document(file_path: str, api_key: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        loader = None
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext in ('.md', '.txt'):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            return f"Unsupported file type: {ext}"
            
        docs = loader.load()
        filename = os.path.basename(file_path)
        for doc in docs:
            doc.metadata['source_filename'] = filename
            doc.metadata['file_type'] = ext
            
        chunks = split_documents(docs)
        
        global _vectorstore
        if _vectorstore is not None:
            _vectorstore.add_documents(chunks)
            os.makedirs(VECTORSTORE_DIR, exist_ok=True)
            _vectorstore.save_local(VECTORSTORE_DIR)
        else:
            init_vectorstore(api_key, force_rebuild=True)
            
        return f"Successfully added {filename} ({len(chunks)} chunks)"
        
    except Exception as e:
        return f"Error adding document: {e}"


@tool
def search_company_policies(query: str) -> str:
    """Search the company policy documents and employee handbook for information about rules, procedures, benefits, and regulations. Use this tool when the user asks about company policies, leave rules, reimbursement procedures, work hours, training programs, or any HR-related rules and guidelines. Args: query: The search query describing what policy information to find."""
    vectorstore = None
    try:
        if hasattr(st, "session_state") and "vectorstore" in st.session_state:
            vectorstore = st.session_state.vectorstore
    except Exception:
        pass

    if vectorstore is None:
        global _vectorstore
        vectorstore = _vectorstore

    if vectorstore is None:
        return "❌ Knowledge base belum diinisialisasi. Silakan pastikan API key sudah dimasukkan."
    
    try:
        docs = vectorstore.similarity_search(query, k=RETRIEVAL_TOP_K)
        
        if not docs:
            return "Tidak ada informasi yang relevan ditemukan di dokumen kebijakan."
            
        results = []
        for doc in docs:
            source = doc.metadata.get('source_filename', 'Unknown Source')
            results.append(f"Source: {source}\nContent:\n{doc.page_content}")
            
        return "\n\n---\n\n".join(results)
    except Exception as e:
        return f"Error searching documents: {e}"
