"""
Centralized UI styling and CSS injection module for PeopleConnect AI.
Implements the 'calm enterprise SaaS' visual design system.
"""
import streamlit as st


def get_custom_css() -> str:
    """
    Return comprehensive CSS stylesheet for PeopleConnect AI.
    """
    return """
    <style>
    /* 1. Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* 2. Global Typography & Colors */
    :root {
        --brand-primary: #0F766E;
        --brand-primary-hover: #115E59;
        --brand-primary-soft: #CCFBF1;
        --brand-accent: #F59E0B;
        --bg-main: #F8FAFC;
        --surface: #FFFFFF;
        --border-color: #E2E8F0;
        --text-primary: #0F172A;
        --text-secondary: #64748B;
        --status-success: #16A34A;
        --status-warning: #D97706;
        --status-error: #DC2626;
        --status-info: #0284C7;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: var(--text-primary);
        overflow-x: hidden !important;
        max-width: 100vw !important;
        box-sizing: border-box !important;
    }

    code, pre, .stCodeBlock, div[data-testid="stCode"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13.5px !important;
    }

    /* 3. Streamlit Cleanup (Hide default chrome) */
    footer {
        visibility: hidden !important;
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 4. Layout & Spacing */
    .main .block-container {
        max-width: 1140px;
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* 5. Custom App Header */
    .brand-header-container {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 0.75rem 0 1.25rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    .brand-left {
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1 1 240px;
        min-width: 0;
    }
    .brand-logo-icon {
        width: 42px;
        height: 42px;
        min-width: 42px;
        flex-shrink: 0;
        border-radius: 10px;
        background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        box-shadow: 0 4px 10px rgba(15, 118, 110, 0.2);
    }
    .brand-text-wrap {
        flex: 1;
        min-width: 0;
    }
    .brand-title {
        font-size: 21px !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: #0F172A !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.25 !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }
    .brand-subtitle {
        font-size: 12.5px;
        color: #64748B;
        margin: 2px 0 0 0;
        font-weight: 500;
        line-height: 1.35;
        word-break: normal;
        overflow-wrap: break-word;
    }
    .brand-badge-wrap {
        flex-shrink: 0;
    }
    .brand-badge {
        display: inline-flex;
        align-items: center;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        background-color: #CCFBF1;
        color: #0F766E;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        white-space: nowrap;
    }

    /* 6. Tabs Styling */
    div[data-testid="stTabs"] {
        margin-top: 0.5rem;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        font-size: 14.5px !important;
        font-weight: 500 !important;
        padding: 0.65rem 1.25rem !important;
        color: #64748B !important;
        border-radius: 8px 8px 0 0 !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #0F766E !important;
        font-weight: 600 !important;
        border-bottom-color: #0F766E !important;
    }

    /* 7. Chat Message Bubbles */
    div[data-testid="stChatMessage"] {
        max-width: 840px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding: 1.15rem 1.35rem !important;
        border-radius: 12px !important;
        margin-bottom: 1.1rem !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        background-color: var(--surface) !important;
        transition: transform 0.15s ease;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #F8FAFC !important;
        border-color: #E2E8F0 !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #FFFFFF !important;
        border-left: 3px solid #0F766E !important;
    }

    /* 8. Welcome Greeting & Example Cards */
    .welcome-container {
        text-align: center;
        max-width: 720px;
        margin: 2rem auto 2.5rem auto;
        padding: 2rem;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03);
    }
    .welcome-title {
        font-size: 22px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 8px;
    }
    .welcome-desc {
        font-size: 14.5px;
        color: #64748B;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* 9. KPI Dashboard Cards (Data Explorer) */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 1.5rem;
    }
    @media (max-width: 900px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem 1.25rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .kpi-label {
        font-size: 13px;
        font-weight: 500;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .kpi-icon-wrap {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
    }

    /* 10. Source Cards & Badges */
    .source-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 11.5px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        margin-bottom: 6px;
    }
    .source-badge-db {
        background-color: #E0F2FE;
        color: #0369A1;
    }
    .source-badge-rag {
        background-color: #FEF3C7;
        color: #B45309;
    }
    .status-badge-approved {
        background-color: #DCFCE7;
        color: #15803D;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
    }
    .status-badge-pending {
        background-color: #FEF9C3;
        color: #A16207;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
    }
    .status-badge-rejected {
        background-color: #FEE2E2;
        color: #B91C1C;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
    }

    /* 11. Buttons & Inputs */
    button[kind="primary"] {
        background-color: #0F766E !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        border: none !important;
        box-shadow: 0 1px 2px rgba(15, 118, 110, 0.15) !important;
        transition: background-color 0.2s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #115E59 !important;
    }
    button[kind="secondary"] {
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 500 !important;
    }
    input, select, textarea {
        border-radius: 8px !important;
    }

    /* 12. Expanders & Status Widget */
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        background-color: #FFFFFF !important;
        margin-bottom: 0.75rem !important;
    }
    div[data-testid="stStatusWidget"] {
        border-radius: 12px !important;
        border: 1px solid #99F6E4 !important;
        background-color: #F0FDFA !important;
    }

    /* 13. Sidebar Visual Enhancements */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    .sidebar-section-title {
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    /* 14. Document Ingestion Card */
    .doc-item-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .doc-item-info {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* 15. Mobile Responsiveness */
    @media (max-width: 640px) {
        .main .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 0.85rem !important;
            padding-bottom: 2rem !important;
        }
        .brand-header-container {
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
            padding: 0.5rem 0 0.85rem 0;
            margin-bottom: 0.75rem;
        }
        .brand-left {
            gap: 10px;
            width: 100%;
        }
        .brand-logo-icon {
            width: 36px;
            height: 36px;
            min-width: 36px;
        }
        .brand-logo-icon svg {
            width: 18px;
            height: 18px;
        }
        .brand-title {
            font-size: 17.5px !important;
            letter-spacing: -0.01em !important;
            white-space: normal !important;
            word-break: normal !important;
            line-height: 1.2 !important;
        }
        .brand-subtitle {
            font-size: 11px !important;
            line-height: 1.35 !important;
        }
        .brand-badge {
            font-size: 10px !important;
            padding: 2px 7px !important;
            letter-spacing: 0.02em !important;
            white-space: nowrap !important;
        }
        /* Stack column blocks on mobile to prevent horizontal overflow */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 8px !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        .welcome-container {
            padding: 1.25rem 1rem !important;
            margin: 1rem auto 1.5rem auto !important;
        }
        .welcome-title {
            font-size: 18px !important;
        }
        .welcome-desc {
            font-size: 13px !important;
        }
        .kpi-grid {
            grid-template-columns: 1fr 1fr !important;
            gap: 10px !important;
        }
        .kpi-card {
            padding: 0.85rem 0.9rem !important;
        }
        .kpi-value {
            font-size: 20px !important;
        }
        .kpi-label {
            font-size: 11px !important;
        }
        div[data-testid="stChatMessage"] {
            padding: 0.85rem 0.95rem !important;
            border-radius: 10px !important;
        }
    }

    @media (max-width: 360px) {
        .brand-title {
            font-size: 16.5px;
        }
        .brand-subtitle {
            font-size: 10px;
        }
        .brand-logo-icon {
            width: 32px;
            height: 32px;
            min-width: 32px;
        }
        .kpi-grid {
            grid-template-columns: 1fr !important;
        }
    }

    /* 16. Dark Mode Adaptations */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-main: #0F172A;
            --surface: #1E293B;
            --border-color: #334155;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
        }
        .brand-title { color: #F8FAFC; }
        .welcome-container { background: #1E293B; border-color: #334155; }
        .welcome-title { color: #F8FAFC; }
        .kpi-card { background: #1E293B; border-color: #334155; }
        .kpi-value { color: #F8FAFC; }
        div[data-testid="stChatMessage"] { background-color: #1E293B !important; border-color: #334155 !important; }
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { background-color: #0F172A !important; }
        section[data-testid="stSidebar"] { background-color: #0F172A !important; border-right-color: #1E293B !important; }
        div[data-testid="stExpander"] { background-color: #1E293B !important; border-color: #334155 !important; }
        .doc-item-card { background: #1E293B; border-color: #334155; }
    }
    </style>
    """


def inject_css():
    """
    Inject custom CSS rules into Streamlit application.
    """
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def render_brand_header():
    """
    Render clean corporate header with wordmark and badge.
    """
    header_html = """
    <div class="brand-header-container">
        <div class="brand-left">
            <div class="brand-logo-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="3" y="3" width="8" height="8" rx="2" fill="white" fill-opacity="0.95"/>
                    <rect x="13" y="3" width="8" height="8" rx="2" fill="white" fill-opacity="0.6"/>
                    <rect x="3" y="13" width="8" height="8" rx="2" fill="white" fill-opacity="0.6"/>
                    <rect x="13" y="13" width="8" height="8" rx="2" fill="white" fill-opacity="0.95"/>
                </svg>
            </div>
            <div class="brand-text-wrap">
                <div class="brand-title">PeopleConnect AI</div>
                <div class="brand-subtitle">PT IDELOGI INDONESIA &bull; Enterprise Employee Self-Service Platform</div>
            </div>
        </div>
        <div class="brand-badge-wrap">
            <span class="brand-badge">Hybrid AI &bull; Production Ready</span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
