"""
Data Explorer Tab UI component for HR Assistant AI.
Provides interactive tables, summary metrics, and data inspection for the HR database.
"""
import streamlit as st
import pandas as pd
from database.init_db import get_all_table_data


def render_data_explorer_tab():
    """
    Render database inspector tab showing metrics and table records.
    """
    st.subheader("📊 HR Data Explorer")
    st.caption("Inspeksi data terstruktur dalam database SQLite (`hr_database.db`).")

    # Fetch data for metrics
    emp_data = get_all_table_data("employees")
    balances_data = get_all_table_data("leave_balances")
    claims_data = get_all_table_data("reimbursements")

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Karyawan", len(emp_data))

    with col2:
        if balances_data:
            df_b = pd.DataFrame(balances_data)
            avg_rem = df_b["remaining_days"].mean() if "remaining_days" in df_b.columns else 0
            st.metric("Rata-rata Sisa Cuti", f"{avg_rem:.1f} hari")
        else:
            st.metric("Rata-rata Sisa Cuti", "0 hari")

    with col3:
        if claims_data:
            pending_count = sum(1 for c in claims_data if c.get("status") == "pending")
            st.metric("Klaim Pending", pending_count)
        else:
            st.metric("Klaim Pending", 0)

    with col4:
        if emp_data:
            active_count = sum(1 for e in emp_data if e.get("employment_status") == "Active")
            st.metric("Karyawan Aktif", active_count)
        else:
            st.metric("Karyawan Aktif", 0)

    st.divider()

    # Table viewer selector
    table_options = {
        "employees": "Daftar Karyawan (employees)",
        "leave_balances": "Saldo Cuti Tahunan 2026 (leave_balances)",
        "leave_history": "Riwayat Pengajuan Cuti (leave_history)",
        "reimbursements": "Klaim Benefit & Reimbursement (reimbursements)",
    }

    selected_table_key = st.selectbox(
        "Pilih Tabel untuk Dilihat:",
        options=list(table_options.keys()),
        format_func=lambda k: table_options[k]
    )

    # Fetch and display table data
    table_rows = get_all_table_data(selected_table_key)

    if table_rows:
        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Menampilkan {len(df)} baris data dari tabel `{selected_table_key}`.")
    else:
        st.info(f"Tabel `{selected_table_key}` belum memiliki data.")
