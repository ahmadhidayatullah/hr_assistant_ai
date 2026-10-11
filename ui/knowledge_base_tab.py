"""
Knowledge Base Tab UI component for HR Assistant AI.
Allows viewing existing policy documents, uploading new SOPs, and managing the RAG index.
"""
import os
import streamlit as st
from core.config import KNOWLEDGE_BASE_DIR, UPLOAD_DIR, ALLOWED_EXTENSIONS
from tools.rag_tools import add_uploaded_document, init_vectorstore


def render_knowledge_base_tab(api_key: str):
    """
    Render Knowledge Base management tab.

    Args:
        api_key: User provided Google API key.
    """
    st.subheader("📑 Company Knowledge Base (RAG)")
    st.caption("Pusat penyimpanan dokumen kebijakan, SOP, dan pedoman karyawan PT IDELOGI INDONESIA.")

    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        st.markdown("#### 📂 Dokumen Kebijakan Aktif")

        # Scan active documents
        doc_files = []
        for directory in [KNOWLEDGE_BASE_DIR, UPLOAD_DIR]:
            if os.path.exists(directory):
                for f in os.listdir(directory):
                    ext = os.path.splitext(f)[1].lower().replace(".", "")
                    if ext in ALLOWED_EXTENSIONS and os.path.isfile(os.path.join(directory, f)):
                        doc_files.append((f, os.path.join(directory, f)))

        if doc_files:
            for fname, fpath in doc_files:
                size_kb = os.path.getsize(fpath) / 1024
                with st.expander(f"📄 {fname} ({size_kb:.1f} KB)", expanded=False):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as file_read:
                            preview_text = file_read.read()
                            st.text_area("Cuplikan Isi:", preview_text[:1500] + ("..." if len(preview_text) > 1500 else ""), height=200, disabled=True)
                    except Exception as e:
                        st.caption(f"Tidak dapat membaca preview teks: {e}")
        else:
            st.info("Belum ada dokumen yang tersedia di knowledge base.")

        # Re-index trigger button
        st.divider()
        if st.button("🔄 Bangun Ulang Index Vektor (Re-Index All)", help="Proses ulang seluruh dokumen dan bangun ulang FAISS vector index"):
            if not api_key:
                st.warning("⚠️ Masukkan Google AI API Key di sidebar terlebih dahulu.")
            else:
                with st.spinner("Memproses seluruh dokumen dan membuat embedding..."):
                    try:
                        vs = init_vectorstore(api_key, force_rebuild=True)
                        st.session_state.vectorstore = vs
                        st.success("✅ Berhasil memperbarui index vektor knowledge base!")
                    except Exception as err:
                        st.error(f"Gagal membangun index: {err}")

    with col_right:
        st.markdown("#### 📤 Unggah Dokumen Tambahan")
        st.write(
            "Tambahkan SOP baru, memo kebijakan, atau petunjuk teknis. Format yang didukung: "
            "**`.pdf`**, **`.txt`**, dan **`.md`**."
        )

        uploaded_file = st.file_uploader(
            "Pilih file dokumen:",
            type=ALLOWED_EXTENSIONS,
            help="File akan disimpan dan otomatis diintegrasikan ke vector store agent"
        )

        if uploaded_file is not None:
            if st.button("📥 Proses & Simpan Dokumen", use_container_width=True):
                if not api_key:
                    st.warning("⚠️ Masukkan Google AI API Key di sidebar terlebih dahulu sebelum memproses dokumen.")
                else:
                    save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    with open(save_path, "wb") as f_out:
                        f_out.write(uploaded_file.getbuffer())

                    with st.spinner(f"Memproses dan melakukan embedding untuk `{uploaded_file.name}`..."):
                        res = add_uploaded_document(save_path, api_key)
                        # Re-sync session state
                        if "vectorstore" not in st.session_state or st.session_state.vectorstore is None:
                            st.session_state.vectorstore = init_vectorstore(api_key)
                        st.success(f"✅ {res}")
                        st.rerun()
