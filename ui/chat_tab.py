"""
Chat Tab UI component for PeopleConnect AI.
Renders conversational interface with clickable prompt suggestions, explainable reasoning steps,
and distinct source citation cards.
"""
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from core.agent import format_chat_history
from core.prompts import WELCOME_MESSAGE


def extract_text_content(content) -> str:
    """
    Extract plain text from AIMessage content, which can be a string,
    a list of text block dicts [{'type': 'text', 'text': '...'}], or structured parts.
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, str):
                text_parts.append(item)
            elif isinstance(item, dict):
                if item.get("type") == "text" and "text" in item:
                    text_parts.append(item["text"])
                elif "text" in item:
                    text_parts.append(item["text"])
                elif "content" in item:
                    text_parts.append(str(item["content"]))
            elif hasattr(item, "text"):
                text_parts.append(str(item.text))
        return "\n".join(text_parts).strip()
    elif isinstance(content, dict):
        if "text" in content:
            return content["text"]
        elif "content" in content:
            return str(content["content"])
    return str(content)


def render_chat_tab():
    """
    Render main conversation tab including chat history, welcome suggestions, and agent execution.
    """
    # Initialize message list
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]

    # Check for prompt submitted via quick example cards
    active_prompt = None
    if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
        active_prompt = st.session_state.pop("pending_prompt")

    # Render Welcome Cards if only welcome message is present
    if len(st.session_state.messages) <= 1:
        st.markdown(
            """
            <div class="welcome-container">
                <div class="welcome-title">Selamat Datang di PeopleConnect AI</div>
                <div class="welcome-desc">
                    Asisten kepegawaian cerdas PT IDELOGI INDONESIA. Tanyakan data kuantitatif kepegawaian Anda 
                    atau telusuri buku pedoman dan regulasi perusahaan secara instan.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<p style='font-size: 13.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Pilih salah satu contoh pertanyaan untuk langsung mencoba:</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                ":material/beach_access: **Berapa sisa cuti tahunan milik Rian Pratama?**\n\n*Contoh Query Database SQL*",
                use_container_width=True,
                key="btn_example_1"
            ):
                st.session_state.pending_prompt = "Berapa sisa cuti tahunan milik Rian Pratama (EMP-003)?"
                st.rerun()

            if st.button(
                ":material/medical_services: **Berapa plafon klaim kacamata dan apa syaratnya?**\n\n*Contoh Query Dokumen Kebijakan (RAG)*",
                use_container_width=True,
                key="btn_example_2"
            ):
                st.session_state.pending_prompt = "Berapa plafon klaim kacamata untuk karyawan dan apa syarat pengajuannya?"
                st.rerun()

        with col2:
            if st.button(
                ":material/celebration: **Saya Siti Rahma (EMP-005) mau menikah. Berapa sisa cuti saya dan apa aturan cuti menikah?**\n\n*Contoh Hybrid Query (SQL + RAG)*",
                use_container_width=True,
                key="btn_example_3"
            ):
                st.session_state.pending_prompt = "Saya Siti Rahma (EMP-005). Saya berencana menikah bulan depan. Berapa sisa cuti saya saat ini, dan apakah cuti menikah akan mengurangi kuota cuti tahunan saya?"
                st.rerun()

            if st.button(
                ":material/work: **Bagaimana aturan WFH dan jam kerja inti kantor?**\n\n*Contoh Query Regulasi Kerja*",
                use_container_width=True,
                key="btn_example_4"
            ):
                st.session_state.pending_prompt = "Bagaimana aturan WFH dan jam kerja inti kantor PT IDELOGI INDONESIA?"
                st.rerun()

        st.divider()

    # Display past conversation history
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = ":material/person:" if role == "user" else ":material/smart_toy:"

        with st.chat_message(role, avatar=avatar):
            # Inspect SQL query source if recorded
            if role == "assistant" and msg.get("sql_query"):
                with st.expander(":material/database: Sumber: Query Database SQL", expanded=False):
                    st.markdown("<span class='source-badge source-badge-db'>Relational Record &bull; SQLite</span>", unsafe_allow_html=True)
                    st.code(msg["sql_query"], language="sql")

            # Inspect Policy document source if recorded
            if role == "assistant" and msg.get("policies_found"):
                with st.expander(":material/menu_book: Sumber: Dokumen Kebijakan Perusahaan", expanded=False):
                    st.markdown("<span class='source-badge source-badge-rag'>Knowledge Retrieval &bull; Handbook</span>", unsafe_allow_html=True)
                    st.markdown(msg["policies_found"])

            clean_text = extract_text_content(msg["content"])

            # Polite Callout formatting for Security Guardrail rejections
            if "Query ditolak" in clean_text:
                st.warning(clean_text, icon=":material/security:")
            else:
                st.markdown(clean_text)

    # Chat input box
    chat_input_val = st.chat_input("Ketik pertanyaan Anda tentang data karyawan atau kebijakan perusahaan...")
    user_prompt = active_prompt or chat_input_val

    if user_prompt:
        # Verify API key availability
        if "agent" not in st.session_state or st.session_state.agent is None:
            st.warning("Silakan masukkan Google AI API Key di menu sebelah kiri (sidebar) untuk mulai berinteraksi.", icon=":material/lock:")
            return

        # Record and render user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(user_prompt)

        # Process agent execution
        with st.chat_message("assistant", avatar=":material/smart_toy:"):
            extracted_sql = None
            extracted_policy = None
            final_answer = ""

            with st.status(":material/psychology: Menganalisis kebutuhan & merumuskan solusi...", expanded=True) as status_box:
                try:
                    chat_history = format_chat_history(st.session_state.messages)

                    status_box.write(":material/search: Mengirim konteks ke engine Google Gemini...")
                    response = st.session_state.agent.invoke({"messages": chat_history})

                    resp_messages = response.get("messages", [])

                    for msg in resp_messages:
                        if isinstance(msg, ToolMessage):
                            tool_name = getattr(msg, "name", "")
                            content = getattr(msg, "content", "")

                            if tool_name == "get_hr_schema":
                                status_box.write(":material/schema: Memeriksa skema database HR...")
                            elif tool_name == "execute_hr_sql":
                                status_box.write(":material/database: Mengeksekusi query database SQL...")
                                if "SQL Query:" in content:
                                    parts = content.split("SQL Query:")
                                    if len(parts) > 1:
                                        extracted_sql = parts[1].split("\n\n")[0].strip()
                            elif tool_name == "search_company_policies":
                                status_box.write(":material/menu_book: Menelusuri buku pedoman kebijakan (RAG)...")
                                extracted_policy = content

                        elif isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                tc_name = tc.get("name", "")
                                tc_args = tc.get("args", {})
                                if tc_name == "execute_hr_sql":
                                    extracted_sql = tc_args.get("sql_query")

                    if resp_messages:
                        last_msg = resp_messages[-1]
                        raw_content = getattr(last_msg, "content", "Maaf, saya tidak dapat merumuskan respon.")
                        final_answer = extract_text_content(raw_content)
                    else:
                        final_answer = "Tidak ada jawaban yang dihasilkan."

                    status_box.update(label=":material/check_circle: Selesai merangkum jawaban", state="complete", expanded=False)

                except Exception as e:
                    status_box.update(label=":material/cancel: Terjadi kendala saat memproses query", state="error", expanded=True)
                    final_answer = f"Terjadi kesalahan saat memproses permintaan: `{str(e)}`\n\nSilakan periksa API Key atau coba ulangi pertanyaan Anda."

            # Render SQL source accordion
            if extracted_sql:
                with st.expander(":material/database: Sumber: Query Database SQL", expanded=False):
                    st.markdown("<span class='source-badge source-badge-db'>Relational Record &bull; SQLite</span>", unsafe_allow_html=True)
                    st.code(extracted_sql, language="sql")

            # Render Policy source accordion
            if extracted_policy:
                with st.expander(":material/menu_book: Sumber: Dokumen Kebijakan Perusahaan", expanded=False):
                    st.markdown("<span class='source-badge source-badge-rag'>Knowledge Retrieval &bull; Handbook</span>", unsafe_allow_html=True)
                    st.markdown(extracted_policy)

            # Render final answer
            if "Query ditolak" in final_answer:
                st.warning(final_answer, icon=":material/security:")
            else:
                st.markdown(final_answer)

            # Persist message record
            msg_record = {
                "role": "assistant",
                "content": final_answer,
                "sql_query": extracted_sql,
                "policies_found": extracted_policy
            }
            st.session_state.messages.append(msg_record)
