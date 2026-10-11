"""
Sidebar UI component for HR Assistant AI.
"""
import os
import streamlit as st
from core.config import DEFAULT_LLM_MODEL, AVAILABLE_MODELS, COMPANY_NAME


def render_sidebar():
    """
    Render sidebar controls including API key, model selector, conversation reset, and status.

    Returns:
        tuple: (api_key: str, selected_model: str, reset_clicked: bool)
    """
    with st.sidebar:
        st.header("⚙️ Pengaturan")

        # API Key input
        api_key_from_env = os.environ.get("GOOGLE_API_KEY", "")
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            value=api_key_from_env,
            placeholder="AIzaSy...",
            help="Dapatkan API key gratis di Google AI Studio (aistudio.google.com)"
        )

        # Model selection (including gemini-3.6-flash)
        model_options = AVAILABLE_MODELS
        selected_model = st.selectbox(
            "Model Gemini",
            options=model_options,
            index=0,
            help="Pilih model Gemini. 'gemini-3.6-flash' / 'gemini-2.5-flash' untuk kecepatan tinggi, 'Pro' untuk penalaran lebih dalam."
        )

        # Reset button
        reset_clicked = st.button(
            "🔄 Reset Percakapan",
            use_container_width=True,
            help="Hapus seluruh riwayat chat dan mulai percakapan baru"
        )

        st.divider()

        # System status indicator
        st.subheader("📡 Status Sistem")
        
        # Check DB
        from core.config import DB_PATH
        if os.path.exists(DB_PATH):
            st.success("Database SQL: Siap (Connected)", icon="✅")
        else:
            st.warning("Database SQL: Belum dibuat", icon="⚠️")

        # Check Vectorstore
        if st.session_state.get("vectorstore") is not None:
            st.success("Knowledge Base: Aktif (FAISS)", icon="✅")
        else:
            st.info("Knowledge Base: Menunggu API key", icon="ℹ️")

        st.divider()

        # About info
        st.subheader("ℹ️ Tentang Aplikasi")
        st.caption(
            f"**HR Assistant AI** untuk **{COMPANY_NAME}**.\n\n"
            "Arsitektur: **Hybrid Agent (SQL + RAG)**\n"
            "- 🧠 Framework: **LangGraph (ReAct Agent)**\n"
            "- 🤖 LLM: **Google Gemini**\n"
            "- 📊 Database: **SQLite (Read-Only Guard)**\n"
            "- 📑 RAG: **FAISS + Gemini Embeddings**"
        )

    return api_key, selected_model, reset_clicked
