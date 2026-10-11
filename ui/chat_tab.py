"""
Chat Tab UI component for HR Assistant AI.
Renders chat messages, handles user queries, and displays LangGraph reasoning steps.
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
    Render main conversation tab including chat history, user input, and agent execution.
    """
    st.subheader("💬 Asisten Kepegawaian & Kebijakan")
    st.caption("Tanyakan data cuti, klaim reimbursement, atau aturan & handbook perusahaan.")

    # Initialize messages
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]

    # Display past conversation
    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role):
            # If assistant message has stored tool details, render them
            if role == "assistant" and "sql_query" in msg and msg["sql_query"]:
                with st.expander("🔍 Query SQL yang Dijalankan", expanded=False):
                    st.code(msg["sql_query"], language="sql")
            
            if role == "assistant" and "policies_found" in msg and msg["policies_found"]:
                with st.expander("📑 Referensi Dokumen Kebijakan", expanded=False):
                    st.markdown(msg["policies_found"])

            st.markdown(extract_text_content(msg["content"]))

    # Quick prompt suggestions
    with st.expander("💡 Contoh Pertanyaan yang Bisa Dicoba", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Query Database (SQL):**\n- *Berapa sisa cuti Rian Pratama?*\n- *Siapa saja karyawan di departemen Engineering?*\n- *Ada berapa klaim reimbursement yang masih pending?*")
        with col2:
            st.markdown("**Query Kebijakan (RAG):**\n- *Berapa hari hak cuti melahirkan bagi karyawan?*\n- *Berapa plafon klaim kacamata dan apa syaratnya?*\n- *Bagaimana aturan WFH dan jam kerja inti?*")
        with col3:
            st.markdown("**Query Hybrid (SQL + RAG):**\n- *Saya Siti Rahma (EMP-005). Saya berencana menikah bulan depan. Berapa sisa cuti saya, dan apakah cuti menikah memotong cuti tahunan?*")

    # Chat input
    user_prompt = st.chat_input("Ketik pertanyaan Anda tentang data karyawan atau kebijakan perusahaan...")

    if user_prompt:
        # Check agent availability
        if "agent" not in st.session_state or st.session_state.agent is None:
            st.warning("⚠️ Silakan masukkan Google AI API Key di menu sebelah kiri (sidebar) terlebih dahulu.")
            return

        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Process agent response
        with st.chat_message("assistant"):
            extracted_sql = None
            extracted_policy = None
            final_answer = ""

            with st.status("🧠 Agent sedang berpikir dan menganalisis kebutuhan...", expanded=True) as status_box:
                try:
                    # Prepare message history
                    chat_history = format_chat_history(st.session_state.messages)
                    
                    status_box.write("🔎 Mengirim konteks ke Google Gemini...")
                    response = st.session_state.agent.invoke({"messages": chat_history})

                    # Parse message trail
                    resp_messages = response.get("messages", [])
                    
                    for msg in resp_messages:
                        # Check ToolMessages
                        if isinstance(msg, ToolMessage):
                            tool_name = getattr(msg, "name", "")
                            content = getattr(msg, "content", "")
                            
                            if tool_name == "get_hr_schema":
                                status_box.write("📋 Memeriksa skema database HR...")
                            elif tool_name == "execute_hr_sql":
                                status_box.write("⚡ Mengeksekusi query database SQL...")
                                # Attempt to extract SQL
                                if "SQL Query:" in content:
                                    parts = content.split("SQL Query:")
                                    if len(parts) > 1:
                                        extracted_sql = parts[1].split("\n\n")[0].strip()
                            elif tool_name == "search_company_policies":
                                status_box.write("📚 Menelusuri dokumen kebijakan perusahaan (RAG)...")
                                extracted_policy = content
                        
                        # Also check AIMessage tool calls
                        elif isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                tc_name = tc.get("name", "")
                                tc_args = tc.get("args", {})
                                if tc_name == "execute_hr_sql":
                                    extracted_sql = tc_args.get("sql_query")

                    # Extract final answer from last message
                    if resp_messages:
                        last_msg = resp_messages[-1]
                        raw_content = getattr(last_msg, "content", "Maaf, saya tidak dapat merumuskan respon.")
                        final_answer = extract_text_content(raw_content)
                    else:
                        final_answer = "Tidak ada jawaban yang dihasilkan."

                    status_box.update(label="✅ Selesai merangkum jawaban!", state="complete", expanded=False)

                except Exception as e:
                    status_box.update(label="❌ Terjadi kendala saat memproses query", state="error", expanded=True)
                    final_answer = f"Terjadi kesalahan saat memproses permintaan: `{str(e)}`\n\nSilakan periksa API Key atau coba ulangi pertanyaan Anda."

            # Render SQL query if executed
            if extracted_sql:
                with st.expander("🔍 Query SQL yang Dijalankan", expanded=False):
                    st.code(extracted_sql, language="sql")

            # Render Policy references if retrieved
            if extracted_policy:
                with st.expander("📑 Referensi Dokumen Kebijakan (RAG)", expanded=False):
                    st.markdown(extracted_policy)

            # Render final answer
            st.markdown(final_answer)

            # Record message in history
            msg_record = {
                "role": "assistant",
                "content": final_answer,
                "sql_query": extracted_sql,
                "policies_found": extracted_policy
            }
            st.session_state.messages.append(msg_record)
