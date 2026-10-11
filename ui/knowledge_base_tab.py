"""
Knowledge Base Tab UI component for PeopleConnect AI.
Allows viewing indexed policy documents, uploading new SOP files, and rebuilding vector store.
"""
import os
import streamlit as st
from core.config import KNOWLEDGE_BASE_DIR, UPLOAD_DIR, ALLOWED_EXTENSIONS
from tools.rag_tools import add_uploaded_document, init_vectorstore


def render_knowledge_base_tab(api_key: str):
    """
    Render Knowledge Base document manager and upload ingestion interface.

    Args:
        api_key: User provided Google AI API key.
    """
    st.caption("Pusat pengelolaan dokumen kebijakan, regulasi, dan Standar Operasional Prosedur (SOP) PT IDELOGI INDONESIA.")

    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                <span style="font-size: 15px; font-weight: 600; color: #0F172A;">Dokumen Kebijakan Aktif</span>
                <span style="font-size: 11.5px; font-weight: 600; color: #0F766E; background: #CCFBF1; padding: 2px 8px; border-radius: 6px;">FAISS RAG</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Scan active documents
        doc_files = []
        for directory in [KNOWLEDGE_BASE_DIR, UPLOAD_DIR]:
            if os.path.exists(directory):
                for f in os.listdir(directory):
                    ext = os.path.splitext(f)[1].lower().replace(".", "")
                    if ext in ALLOWED_EXTENSIONS and os.path.isfile(os.path.join(directory, f)):
                        doc_files.append((f, os.path.join(directory, f), ext))

        if doc_files:
            for fname, fpath, ext in doc_files:
                size_kb = os.path.getsize(fpath) / 1024
                icon_type = "📕" if ext == "pdf" else "📘"

                with st.expander(f"{icon_type} {fname} ({size_kb:.1f} KB)", expanded=False):
                    st.caption(f"Format: `.{ext.upper()}` &bull; Lokasi: `{os.path.basename(os.path.dirname(fpath))}/`")
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as file_read:
                            preview_text = file_read.read()
                            st.text_area(
                                "Cuplikan Dokumen:",
                                preview_text[:1400] + ("..." if len(preview_text) > 1400 else ""),
                                height=180,
                                disabled=True
                            )
                    except Exception as e:
                        st.caption(f"Gagal memuat pratinjau teks: {e}")
        else:
            st.info("Belum ada dokumen yang tersedia di knowledge base.", icon=":material/info:")

        # Re-index trigger button
        st.divider()
        if st.button(":material/sync: Bangun Ulang Index Vektor (Re-Index All)", help="Proses ulang seluruh dokumen dan rekonstruksi FAISS vector index"):
            if not api_key:
                st.warning("Masukkan Google AI API Key di menu sidebar terlebih dahulu.", icon=":material/lock:")
            else:
                with st.status(":material/sync: Memproses seluruh dokumen dan menghasilkan embedding...", expanded=True) as status_box:
                    try:
                        status_box.write(":material/description: Membaca dokumen markdown, text, dan PDF...")
                        vs = init_vectorstore(api_key, force_rebuild=True)
                        st.session_state.vectorstore = vs
                        status_box.update(label=":material/check_circle: Berhasil memperbarui index vektor knowledge base!", state="complete", expanded=False)
                        st.success("Seluruh dokumen berhasil diindeks ulang ke Vector Store.", icon=":material/check_circle:")
                    except Exception as err:
                        status_box.update(label=":material/cancel: Gagal membangun index vektor", state="error", expanded=True)
                        st.error(f"Terjadi kesalahan: {err}")

    with col_right:
        st.markdown(
            """
            <div style="margin-bottom: 0.75rem;">
                <span style="font-size: 15px; font-weight: 600; color: #0F172A;">Unggah Dokumen Tambahan</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="font-size: 13px; color: #64748B; margin-bottom: 12px; line-height: 1.5;">
                Tambahkan memo internal baru, kebijakan fasilitas, atau petunjuk operasional.
                Dokumen akan otomatis dipotong (*chunking*) dan diintegrasikan ke vector store agent.
            </div>
            <div style="display: flex; gap: 6px; margin-bottom: 14px;">
                <span style="font-size: 11px; font-weight: 600; padding: 2px 7px; background: #F1F5F9; border-radius: 4px; color: #475569;">.PDF</span>
                <span style="font-size: 11px; font-weight: 600; padding: 2px 7px; background: #F1F5F9; border-radius: 4px; color: #475569;">.TXT</span>
                <span style="font-size: 11px; font-weight: 600; padding: 2px 7px; background: #F1F5F9; border-radius: 4px; color: #475569;">.MD</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        uploaded_file = st.file_uploader(
            "Pilih file dokumen:",
            type=ALLOWED_EXTENSIONS,
            help="Ukuran file maksimal 10 MB per dokumen"
        )

        if uploaded_file is not None:
            if st.button(":material/upload_file: Proses & Simpan Dokumen", use_container_width=True, type="primary"):
                if not api_key:
                    st.warning("Masukkan Google AI API Key di sidebar terlebih dahulu sebelum memproses dokumen.", icon=":material/lock:")
                else:
                    save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    with open(save_path, "wb") as f_out:
                        f_out.write(uploaded_file.getbuffer())

                    with st.status(f":material/hourglass_top: Memproses `{uploaded_file.name}`...", expanded=True) as status_box:
                        status_box.write(":material/data_object: Melakukan chunking dan embedding vektor...")
                        res = add_uploaded_document(save_path, api_key)

                        if "vectorstore" not in st.session_state or st.session_state.vectorstore is None:
                            st.session_state.vectorstore = init_vectorstore(api_key)

                        status_box.update(label=":material/check_circle: Selesai diindeks ke Knowledge Base!", state="complete", expanded=False)
                        st.success(f"Berhasil: {res}", icon=":material/check_circle:")
                        st.rerun()
