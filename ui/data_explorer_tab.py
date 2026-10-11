"""
Data Explorer Tab UI component for PeopleConnect AI.
Provides an executive KPI dashboard, instant search/filter, and interactive table inspection.
"""
import streamlit as st
import pandas as pd
from database.init_db import get_all_table_data


def format_currency_idr(amount) -> str:
    """Format numeric amount to Indonesian Rupiah string."""
    try:
        val = float(amount)
        return f"Rp {val:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return str(amount)


def render_data_explorer_tab():
    """
    Render executive dashboard cards, search filters, and tabular records inspector.
    """
    st.caption("Inspeksi data terstruktur operasional kepegawaian dalam database SQLite (`hr_database.db`).")

    # Fetch datasets
    emp_data = get_all_table_data("employees")
    balances_data = get_all_table_data("leave_balances")
    claims_data = get_all_table_data("reimbursements")

    # Compute key figures
    total_emp = len(emp_data)
    active_emp = sum(1 for e in emp_data if e.get("employment_status") == "Active") if emp_data else 0

    if balances_data:
        df_b = pd.DataFrame(balances_data)
        avg_remaining = df_b["remaining_days"].mean() if "remaining_days" in df_b.columns else 0.0
    else:
        avg_remaining = 0.0

    pending_claims = sum(1 for c in claims_data if c.get("status") == "pending") if claims_data else 0

    # Executive KPI Dashboard Cards
    kpi_html = f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Total Karyawan</span>
                <div class="kpi-icon-wrap" style="background: #E0F2FE; color: #0284C7;">👥</div>
            </div>
            <div class="kpi-value">{total_emp} <span style="font-size: 14px; font-weight: 500; color: #64748B;">orang</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Karyawan Tetap Aktif</span>
                <div class="kpi-icon-wrap" style="background: #DCFCE7; color: #16A34A;">✓</div>
            </div>
            <div class="kpi-value">{active_emp} <span style="font-size: 14px; font-weight: 500; color: #64748B;">staf</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Rata-rata Sisa Cuti</span>
                <div class="kpi-icon-wrap" style="background: #CCFBF1; color: #0F766E;">🏖️</div>
            </div>
            <div class="kpi-value">{avg_remaining:.1f} <span style="font-size: 14px; font-weight: 500; color: #64748B;">hari/thn</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">
                <span class="kpi-label">Klaim Pending</span>
                <div class="kpi-icon-wrap" style="background: #FEF3C7; color: #D97706;">📄</div>
            </div>
            <div class="kpi-value">{pending_claims} <span style="font-size: 14px; font-weight: 500; color: #64748B;">menunggu</span></div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 16px; font-weight: 600; color: #0F172A; margin: 1.5rem 0 0.5rem 0;'>Tabel Data Operasional</p>", unsafe_allow_html=True)

    # Filter & Table Selection Controls
    col_sel, col_search = st.columns([1.2, 2], gap="medium")

    table_options = {
        "employees": "Daftar Karyawan (employees)",
        "leave_balances": "Saldo Cuti Tahunan 2026 (leave_balances)",
        "leave_history": "Riwayat Pengajuan Cuti (leave_history)",
        "reimbursements": "Klaim Benefit & Reimbursement (reimbursements)",
    }

    with col_sel:
        selected_table_key = st.selectbox(
            "Pilih Tabel:",
            options=list(table_options.keys()),
            format_func=lambda k: table_options[k],
            label_visibility="collapsed"
        )

    with col_search:
        search_query = st.text_input(
            "Cari data:",
            placeholder="Ketik nama, departemen, kategori, atau status...",
            label_visibility="collapsed"
        )

    # Fetch and transform table data
    table_rows = get_all_table_data(selected_table_key)

    if table_rows:
        df = pd.DataFrame(table_rows)

        # Enhance formatting depending on table
        if selected_table_key == "reimbursements" and "amount" in df.columns:
            df["nominal_rp"] = df["amount"].apply(format_currency_idr)

        # Apply search filter if query provided
        if search_query and search_query.strip():
            query_lower = search_query.strip().lower()
            mask = df.astype(str).apply(lambda row: row.str.lower().str.contains(query_lower).any(), axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df

        # Display table with column configuration
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Menampilkan **{len(filtered_df)}** dari total **{len(df)}** baris data pada tabel `{selected_table_key}`.")
    else:
        st.info("Tabel ini belum memiliki data untuk ditampilkan.", icon=":material/info:")
