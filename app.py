"""
HR Assistant AI - Main Application Entry Point
Streamlit web app integrating LangGraph ReAct Agent, SQLite HR Database, and FAISS RAG Knowledge Base.
"""
import os
import sys
import streamlit as st

# Configure page layout and title
st.set_page_config(
    page_title="HR Assistant AI | PT IDELOGI INDONESIA",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure project root in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import APP_TITLE, APP_SUBTITLE, DB_PATH
from database.init_db import init_database
from core.agent import create_hr_agent
from tools.rag_tools import init_vectorstore
from ui.sidebar import render_sidebar
from ui.chat_tab import render_chat_tab
from ui.data_explorer_tab import render_data_explorer_tab
from ui.knowledge_base_tab import render_knowledge_base_tab


def initialize_app_state(api_key: str, model_name: str):
    """
    Ensure database, vector store, and LangGraph agent instances are properly initialized.
    """
    # 1. Ensure SQL DB exists
    if not os.path.exists(DB_PATH):
        init_database()

    # 2. Check if API key provided
    if not api_key:
        return

    # 3. Check if key or model changed
    key_changed = getattr(st.session_state, "_last_api_key", None) != api_key
    model_changed = getattr(st.session_state, "_last_model", None) != model_name

    if key_changed or model_changed or ("agent" not in st.session_state):
        try:
            # Initialize vectorstore if not already loaded
            if "vectorstore" not in st.session_state or st.session_state.vectorstore is None or key_changed:
                try:
                    vs = init_vectorstore(api_key)
                    st.session_state.vectorstore = vs
                except Exception as e:
                    st.sidebar.warning(f"Knowledge base indexing note: {e}")

            # Create agent
            st.session_state.agent = create_hr_agent(
                api_key=api_key,
                model_name=model_name
            )
            st.session_state._last_api_key = api_key
            st.session_state._last_model = model_name

        except Exception as e:
            st.sidebar.error(f"Gagal menginisialisasi Agent: {e}")


def main():
    # Render header
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)

    # Render sidebar and get user settings
    api_key, selected_model, reset_clicked = render_sidebar()

    # Handle reset request
    if reset_clicked:
        st.session_state.pop("messages", None)
        st.session_state.pop("agent", None)
        st.rerun()

    # Initialize agent and resources
    initialize_app_state(api_key, selected_model)

    # Render main tabs
    tab_chat, tab_data, tab_kb = st.tabs([
        "💬 HR Chatbot",
        "📊 HR Data Explorer",
        "📑 Knowledge Base"
    ])

    with tab_chat:
        render_chat_tab()

    with tab_data:
        render_data_explorer_tab()

    with tab_kb:
        render_knowledge_base_tab(api_key)


if __name__ == "__main__":
    main()
