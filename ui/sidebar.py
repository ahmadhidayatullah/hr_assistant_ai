"""
Sidebar UI component for PeopleConnect AI.
Provides clean enterprise controls for configuration, connection status, and conversation reset.
"""
import os
import streamlit as st
from core.config import AVAILABLE_MODELS, COMPANY_NAME, DB_PATH


def render_sidebar():
    """
    Render sidebar controls organized into distinct logical sections with Material Symbols.

    Returns:
        tuple: (api_key: str, selected_model: str, reset_clicked: bool)
    """
    with st.sidebar:
        # Section 1: Brand & New Conversation Action
        st.markdown(
            f"""
            <div style="padding-bottom: 0.5rem;">
                <div style="font-size: 11px; font-weight: 700; color: #0F766E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2px;">
                    Enterprise Assistant
                </div>
                <div style="font-size: 16px; font-weight: 700; color: #0F172A;">
                    {COMPANY_NAME}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        reset_clicked = st.button(
            ":material/add_comment: Percakapan Baru",
            use_container_width=True,
            type="primary",
            help="Hapus riwayat saat ini dan mulai sesi konsultasi baru"
        )

        st.markdown("<div class='sidebar-section-title'>⚙️ Konfigurasi</div>", unsafe_allow_html=True)

        # Section 2: Model Configuration
        api_key_from_env = os.environ.get("GOOGLE_API_KEY", "")
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            value=api_key_from_env,
            placeholder="AIzaSy...",
            help="Dapatkan API key di Google AI Studio (aistudio.google.com)"
        )

        # Key Status Badge
        if api_key and api_key.strip():
            st.caption(":material/check_circle: **Status Key:** Aktif / Terhubung")
        else:
            st.caption(":material/lock: **Status Key:** Belum diisi (diperlukan)")

        selected_model = st.selectbox(
            "Model Generative AI",
            options=AVAILABLE_MODELS,
            index=0,
            help="Pilih engine Google Gemini. Flash untuk respon kilat, Pro untuk penalaran mendalam."
        )

        st.markdown("<div class='sidebar-section-title'>📡 Status Integrasi</div>", unsafe_allow_html=True)

        # Section 3: Connection & Infrastructure Status
        if os.path.exists(DB_PATH):
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 6px; font-size: 13px;">
                    <span style="display: flex; align-items: center; gap: 6px; color: #334155; font-weight: 500;">
                        Database SQL
                    </span>
                    <span style="color: #16A34A; font-weight: 600; font-size: 11.5px;">● Siap</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 10px; background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; margin-bottom: 6px; font-size: 13px;">
                    <span style="color: #92400E; font-weight: 500;">Database SQL</span>
                    <span style="color: #D97706; font-weight: 600; font-size: 11.5px;">● Menunggu DB</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.session_state.get("vectorstore") is not None:
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 6px; font-size: 13px;">
                    <span style="display: flex; align-items: center; gap: 6px; color: #334155; font-weight: 500;">
                        Knowledge Base
                    </span>
                    <span style="color: #16A34A; font-weight: 600; font-size: 11.5px;">● Terindeks</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 6px; font-size: 13px;">
                    <span style="color: #64748B; font-weight: 500;">Knowledge Base</span>
                    <span style="color: #64748B; font-weight: 600; font-size: 11.5px;">○ Butuh Key</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div class='sidebar-section-title'>💡 Panduan Penggunaan</div>", unsafe_allow_html=True)

        # Section 4: Quick Tips & Documentation
        st.markdown(
            """
            <div style="font-size: 12.5px; color: #64748B; line-height: 1.5; padding: 4px 0;">
                <p style="margin-bottom: 6px;"><b>Hybrid Query:</b> Tanyakan informasi gabungan data kuantitatif pribadi dan pasal SOP perusahaan.</p>
                <p style="margin-bottom: 0;"><b>Keamanan:</b> Operasi database dilindungi oleh <i>Read-Only Security Guard</i>.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    return api_key, selected_model, reset_clicked
