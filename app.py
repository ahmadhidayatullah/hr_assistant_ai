"""
PeopleConnect AI - Main Application Entry Point
Streamlit web application integrating LangGraph ReAct Agent, SQLite HR Database, and FAISS RAG Knowledge Base.
Enterprise HR Self-Service Platform for PT IDELOGI INDONESIA.
"""
import os
import sys
import streamlit as st

# Configure page layout, title, and favicon
st.set_page_config(
    page_title="PeopleConnect AI | PT IDELOGI INDONESIA",
    page_icon=":material/corporate_fare:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure project root in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import DB_PATH
from database.init_db import init_database
from core.agent import create_hr_agent
from tools.rag_tools import init_vectorstore
from ui.styles import inject_css, render_brand_header
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
    # Inject centralized custom CSS
    inject_css()

    # Render branded enterprise header
    render_brand_header()

    # Render sidebar and retrieve user configuration
    api_key, selected_model, reset_clicked = render_sidebar()

    # Handle conversation reset request
    if reset_clicked:
        st.session_state.pop("messages", None)
        st.session_state.pop("agent", None)
        st.rerun()

    # Initialize agent, DB, and RAG index
    initialize_app_state(api_key, selected_model)

    # Render main navigation tabs with Material Symbols
    tab_chat, tab_data, tab_kb = st.tabs([
        ":material/chat: Asisten HR",
        ":material/monitoring: Data Explorer",
        ":material/description: Knowledge Base"
    ])

    with tab_chat:
        render_chat_tab()

    with tab_data:
        render_data_explorer_tab()

    with tab_kb:
        render_knowledge_base_tab(api_key)


if __name__ == "__main__":
    main()
