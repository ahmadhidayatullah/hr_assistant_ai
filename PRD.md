# PRD: HR & Employee Self-Service Assistant
## Hybrid AI Agent — SQL + RAG | Streamlit × LangGraph × Google Gemini

---

> **Project Codename**: `hr-assistant-ai`
> **Version**: 1.0.0
> **Author**: Ahmad Hidayatullah
> **Created**: 2026-10-11
> **Status**: Planning → Implementation
> **Reference**: [chatbot-streamlit-demo](https://github.com/adiptamartulandi/chatbot-streamlit-demo)

---

## 1. Executive Summary

### 1.1 Problem Statement

Karyawan di sebuah perusahaan sering menghadapi dua jenis kebutuhan informasi:

1. **Data Kuantitatif Pribadi** — Berapa sisa cuti saya? Status klaim reimbursement saya? Siapa manajer saya?
2. **Aturan & Kebijakan Perusahaan** — Apakah cuti menikah memotong cuti tahunan? Berapa plafon klaim kacamata? Bagaimana prosedur lembur?

Saat ini, untuk menjawab pertanyaan tipe (1) karyawan harus login ke sistem HRIS, dan untuk tipe (2) harus membaca dokumen handbook yang panjang. Kedua proses ini memakan waktu dan tidak efisien.

### 1.2 Proposed Solution

Membangun **HR & Employee Self-Service Assistant** — sebuah chatbot AI berbasis web yang mampu:

- Menjawab pertanyaan data karyawan secara real-time dari **database SQL** (SQLite).
- Menjawab pertanyaan kebijakan perusahaan dari **dokumen knowledge base** menggunakan teknik **RAG (Retrieval-Augmented Generation)**.
- Menggabungkan kedua sumber informasi dalam satu jawaban yang koheren (**Hybrid Query**).

### 1.3 Differentiator dari Reference Repository

| Aspek | Reference (chatbot-streamlit-demo) | Proyek Ini |
|---|---|---|
| Domain | Generic sales data | HR & Employee operations |
| Data Source | SQL saja | **Hybrid: SQL + RAG (dokumen)** |
| Tools | 2 tools (schema + query) | **3+ tools (schema + query + policy search)** |
| Document Upload | Tidak ada | **Tersedia (PDF, TXT, MD)** |
| Query Safety | Tidak ada | **SQL Safety Guard (SELECT-only)** |
| Agent Transparency | Hidden | **Visible reasoning steps (st.status)** |
| UI | Single chat page | **Multi-tab (Chat, Data Explorer, Knowledge Base)** |

---

## 2. Goals & Success Criteria

### 2.1 Primary Goals

- [ ] Chatbot dapat menjawab pertanyaan data karyawan dari database SQL
- [ ] Chatbot dapat menjawab pertanyaan kebijakan dari dokumen perusahaan via RAG
- [ ] Chatbot dapat menggabungkan jawaban dari kedua sumber (Hybrid Query)
- [ ] UI yang profesional dan transparan menampilkan proses reasoning agent

### 2.2 Success Criteria

1. **Akurasi SQL**: Agent menghasilkan query SQL yang benar untuk 90%+ pertanyaan data karyawan.
2. **Relevansi RAG**: Dokumen yang di-retrieve relevan dengan pertanyaan user.
3. **Hybrid Synthesis**: Jawaban gabungan SQL + RAG koheren dan informatif.
4. **UX**: User dapat memahami langkah-langkah reasoning agent secara visual.

---

## 3. User Personas & Use Cases

### 3.1 Persona Utama: Karyawan Perusahaan

- **Nama**: Siti Rahma (EMP-005)
- **Role**: Staff Marketing
- **Kebutuhan**: Mengecek sisa cuti, memahami benefit karyawan, mengajukan pertanyaan seputar kebijakan HR tanpa harus menghubungi HR secara langsung.

### 3.2 Use Cases

#### UC-1: Query Data Pribadi (SQL Only)
```
User: "Berapa sisa cuti tahunan milik Rian Pratama (EMP-003)?"
Agent: [execute_hr_sql] → "Sisa cuti tahunan Rian Pratama: 8 hari dari total 12 hari."
```

#### UC-2: Query Kebijakan Perusahaan (RAG Only)
```
User: "Berapa plafon klaim kacamata dan apa syarat pengajuannya?"
Agent: [search_company_policies] → "Menurut Bab 2 Handbook, plafon kacamata
       adalah Rp 1.500.000 per 2 tahun. Syarat: resep dokter mata dan kuitansi
       asli, diajukan max 30 hari setelah pembelian."
```

#### UC-3: Hybrid Query (SQL + RAG)
```
User: "Saya Siti Rahma (EMP-005). Saya berencana menikah bulan depan.
       Berapa sisa cuti saya saat ini, dan apakah cuti menikah akan
       mengurangi kuota cuti tahunan saya?"
Agent: [execute_hr_sql] → Sisa cuti: 8 hari
       [search_company_policies] → Bab 1: Cuti menikah = 3 hari, paid leave
       Synthesis: "Sisa cuti tahunan Anda saat ini 8 hari. Menurut kebijakan
       perusahaan Bab 1, cuti menikah adalah cuti khusus berbayar (3 hari)
       dan TIDAK memotong saldo cuti tahunan Anda."
```

#### UC-4: Upload Dokumen Baru
```
User: Mengunggah file "kebijakan_wfh_2026.pdf" via UI
System: Otomatis chunking → embedding → simpan ke Vector Store
Agent: Dapat menjawab pertanyaan tentang kebijakan WFH dari dokumen baru
```

---

## 4. Technical Architecture

### 4.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND                           │
│  ┌──────────────┬──────────────────┬─────────────────────────┐  │
│  │  💬 HR Chat  │  📊 Data Explorer │  📑 Knowledge Base     │  │
│  │              │                  │                         │  │
│  │  Chat UI     │  Interactive     │  Document List          │  │
│  │  + Reasoning │  Tables          │  + File Uploader        │  │
│  │  Steps       │  (st.dataframe)  │  + Preview              │  │
│  └──────┬───────┴────────┬─────────┴────────────┬────────────┘  │
│         │                │                      │               │
└─────────┼────────────────┼──────────────────────┼───────────────┘
          │                │                      │
          ▼                │                      │
┌─────────────────────┐    │                      │
│  LangGraph ReAct    │    │                      │
│  Agent              │    │                      │
│  ┌───────────────┐  │    │                      │
│  │ Gemini 2.5    │  │    │                      │
│  │ Flash / Pro   │  │    │                      │
│  └───────┬───────┘  │    │                      │
│          │          │    │                      │
│  ┌───────▼───────┐  │    │                      │
│  │ Tool Router   │  │    │                      │
│  └──┬────┬────┬──┘  │    │                      │
│     │    │    │      │    │                      │
└─────┼────┼────┼──────┘    │                      │
      │    │    │           │                      │
      ▼    │    ▼           │                      │
┌──────┐   │ ┌───────┐     │                      │
│Tool 1│   │ │Tool 3 │     │                      │
│Schema│   │ │Policy │     │                      │
│Info  │   │ │Search │     │                      │
└──┬───┘   │ └──┬────┘     │                      │
   │       │    │           │                      │
   ▼       ▼    ▼           ▼                      ▼
┌──────────────────┐  ┌──────────────────────────────────┐
│  SQLite Database │  │  Vector Store (FAISS / Chroma)   │
│  hr_database.db  │  │  + Google Embeddings             │
│                  │  │                                  │
│  - employees     │  │  Docs:                           │
│  - leave_balances│  │  - company_handbook.md           │
│  - leave_history │  │  - uploaded_docs/*               │
│  - reimbursements│  │                                  │
└──────────────────┘  └──────────────────────────────────┘
```

### 4.2 Technology Stack

| Layer | Technology | Justification |
|---|---|---|
| **Frontend** | Streamlit | Rapid prototyping, native chat UI, Hacktiv8 requirement |
| **LLM** | Google Gemini 2.5 Flash | Cepat, murah, window besar, sudah ada API key Pro |
| **Agent Framework** | LangGraph (`create_react_agent`) | ReAct pattern, tool calling, state management |
| **LLM Binding** | `langchain-google-genai` | LangChain integration untuk Gemini |
| **Embeddings** | `GoogleGenerativeAIEmbeddings` (`text-embedding-004`) | Konsistensi ekosistem Google AI |
| **Vector Store** | FAISS (via `langchain-community`) | Lokal, tanpa server, cepat |
| **Database** | SQLite | Ringan, tanpa setup, built-in Python |
| **Document Loader** | `langchain-community` (PDF, MD, TXT loaders) | Multi-format support |
| **Visualization** | `st.dataframe`, `st.metric` | Native Streamlit components |

### 4.3 Dependencies (`requirements.txt`)

```
streamlit
google-genai>=1.0.0
langchain-google-genai>=2.1.0
langchain-core
langchain-community
langgraph>=0.0.30
faiss-cpu
pypdf
```

---

## 5. Data Design

### 5.1 Database Schema: `hr_database.db`

#### Table: `employees`
| Column | Type | Constraint | Description |
|---|---|---|---|
| employee_id | TEXT | PRIMARY KEY | Format: EMP-001 |
| name | TEXT | NOT NULL | Nama lengkap |
| email | TEXT | UNIQUE | Email korporat |
| department | TEXT | NOT NULL | Departemen (Engineering, Marketing, Finance, HR, Operations) |
| job_title | TEXT | NOT NULL | Jabatan |
| join_date | TEXT | NOT NULL | Tanggal bergabung (YYYY-MM-DD) |
| employment_status | TEXT | NOT NULL | Status: Active, Probation, Resigned |
| manager_name | TEXT | | Nama manajer langsung |

#### Table: `leave_balances`
| Column | Type | Constraint | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | |
| employee_id | TEXT | FK → employees | |
| year | INTEGER | NOT NULL | Tahun anggaran |
| total_quota | INTEGER | NOT NULL | Total kuota cuti tahunan (hari) |
| used_days | INTEGER | DEFAULT 0 | Hari cuti yang sudah dipakai |
| remaining_days | INTEGER | GENERATED | total_quota - used_days |

#### Table: `leave_history`
| Column | Type | Constraint | Description |
|---|---|---|---|
| request_id | INTEGER | PRIMARY KEY AUTOINCREMENT | |
| employee_id | TEXT | FK → employees | |
| leave_type | TEXT | NOT NULL | annual, sick, marriage, maternity, paternity, bereavement |
| start_date | TEXT | NOT NULL | Tanggal mulai (YYYY-MM-DD) |
| end_date | TEXT | NOT NULL | Tanggal selesai (YYYY-MM-DD) |
| days_count | INTEGER | NOT NULL | Jumlah hari |
| status | TEXT | NOT NULL | pending, approved, rejected |
| reason | TEXT | | Alasan pengajuan |

#### Table: `reimbursements`
| Column | Type | Constraint | Description |
|---|---|---|---|
| claim_id | INTEGER | PRIMARY KEY AUTOINCREMENT | |
| employee_id | TEXT | FK → employees | |
| category | TEXT | NOT NULL | medical, glasses, training, transport |
| amount | REAL | NOT NULL | Nominal klaim (Rp) |
| submit_date | TEXT | NOT NULL | Tanggal pengajuan |
| receipt_date | TEXT | NOT NULL | Tanggal kuitansi |
| status | TEXT | NOT NULL | pending, approved, rejected, paid |
| notes | TEXT | | Catatan tambahan |

### 5.2 Sample Data

**Employees** (10 karyawan):

| ID | Name | Department | Job Title |
|---|---|---|---|
| EMP-001 | Budi Santoso | Engineering | Senior Developer |
| EMP-002 | Dewi Lestari | Marketing | Marketing Manager |
| EMP-003 | Rian Pratama | Engineering | Junior Developer |
| EMP-004 | Anisa Wijaya | Finance | Finance Analyst |
| EMP-005 | Siti Rahma | Marketing | Marketing Staff |
| EMP-006 | Hendra Gunawan | Operations | Operations Lead |
| EMP-007 | Maya Putri | HR | HR Specialist |
| EMP-008 | Fajar Nugroho | Engineering | Tech Lead |
| EMP-009 | Linda Permata | Finance | Finance Manager |
| EMP-010 | Arief Rahman | Operations | Operations Staff |

**Leave Balances** (Tahun 2026, kuota standar 12 hari/tahun):

| Employee | Used | Remaining |
|---|---|---|
| EMP-001 (Budi) | 4 | 8 |
| EMP-002 (Dewi) | 7 | 5 |
| EMP-003 (Rian) | 3 | 9 |
| EMP-004 (Anisa) | 6 | 6 |
| EMP-005 (Siti) | 2 | 10 |
| EMP-006 (Hendra) | 5 | 7 |
| EMP-007 (Maya) | 1 | 11 |
| EMP-008 (Fajar) | 8 | 4 |
| EMP-009 (Linda) | 3 | 9 |
| EMP-010 (Arief) | 6 | 6 |

### 5.3 Knowledge Base Documents

#### Primary Document: `company_handbook.md`

Dokumen ini akan berisi 5 bab utama:

**Bab 1 — Kebijakan Cuti & Izin**
- Cuti tahunan: 12 hari/tahun untuk karyawan tetap, 0 untuk probation
- Cuti khusus berbayar (TIDAK memotong cuti tahunan):
  - Cuti menikah: 3 hari kerja
  - Cuti istri melahirkan (paternity): 2 hari kerja
  - Cuti melahirkan (maternity): 90 hari kalender
  - Cuti duka (keluarga inti): 2 hari kerja
  - Cuti duka (keluarga besar): 1 hari kerja
- Cuti sakit: Wajib melampirkan surat dokter jika > 2 hari berturut-turut
- Prosedur pengajuan: Minimal 3 hari kerja sebelumnya (kecuali darurat)
- Approval chain: Karyawan → Manajer Langsung → HR

**Bab 2 — Benefit & Reimbursement**
- Asuransi kesehatan: Rawat jalan & rawat inap (kelas perusahaan)
- Reimbursement kacamata: Maks Rp 1.500.000 per 2 tahun, syarat resep dokter mata
- Reimbursement medical check-up: 1x per tahun, maks Rp 2.000.000
- Reimbursement transportasi dinas: Sesuai kuitansi, approval manajer
- Batas waktu klaim: Maks 30 hari kalender dari tanggal kuitansi
- Prosedur klaim: Submit form + foto kuitansi ke sistem HR

**Bab 3 — Jam Kerja & Fleksibilitas**
- Jam kerja inti (core hours): 09.00 - 17.00 WIB (8 jam, termasuk 1 jam istirahat)
- Kebijakan WFH: Maks 2 hari/minggu, harus koordinasi dengan manajer
- Lembur: Wajib approval manajer, kompensasi 1.5x upah per jam (hari kerja), 2x (hari libur)
- Izin terlambat: Toleransi 15 menit, lebih dari itu tercatat sebagai keterlambatan

**Bab 4 — Pelatihan & Pengembangan Karir**
- Learning budget: Rp 5.000.000 per tahun per karyawan
- Sertifikasi profesional: Di-cover penuh jika relevan dengan posisi (approval manajer + HR)
- Internal training: Wajib minimal 2 sesi per semester
- Mentor program: Tersedia untuk junior staff (< 2 tahun masa kerja)

**Bab 5 — Kode Etik & Disiplin**
- Pelanggaran ringan: Teguran lisan → tertulis
- Pelanggaran berat: SP1 → SP2 → SP3 → PHK
- Konflik kepentingan: Wajib disclosure ke HR
- Kerahasiaan data: NDA berlaku selama dan setelah masa kerja

---

## 6. Agent Design

### 6.1 Agent Tools Specification

#### Tool 1: `get_hr_schema()`
```
Purpose: Memberikan informasi skema database HR kepada LLM
Input: None
Output: Dictionary berisi nama tabel, kolom, tipe data, dan sample 3 baris
Usage: Dipanggil agent sebelum menulis SQL query
```

#### Tool 2: `execute_hr_sql(sql_query: str)`
```
Purpose: Eksekusi query SQL ke database HR
Input: sql_query (string SQL)
Output: Dictionary berisi query yang dieksekusi dan hasilnya
Safety: HANYA mengizinkan SELECT statement. Menolak DROP, DELETE, UPDATE,
        INSERT, ALTER, CREATE, TRUNCATE dengan pesan error yang jelas.
```

#### Tool 3: `search_company_policies(query: str)`
```
Purpose: Pencarian semantik di dokumen kebijakan perusahaan
Input: query (pertanyaan dalam bahasa natural)
Output: Top-K (k=3) dokumen chunks yang paling relevan beserta metadata
        (nama file sumber, nomor bab/section)
```

### 6.2 Agent System Prompt

```
Kamu adalah HR Assistant AI untuk PT IDELOGI INDONESIA.
Kamu memiliki akses ke dua sumber informasi:

1. DATABASE KARYAWAN (SQL) — Berisi data karyawan, saldo cuti,
   riwayat cuti, dan riwayat klaim reimbursement.
2. DOKUMEN KEBIJAKAN PERUSAHAAN (Knowledge Base) — Berisi handbook
   karyawan, SOP, dan peraturan perusahaan.

INSTRUKSI:
- Jika pertanyaan tentang DATA SPESIFIK karyawan (sisa cuti, riwayat,
  nominal, dsb.), gunakan tool SQL.
- Jika pertanyaan tentang ATURAN/KEBIJAKAN/PROSEDUR, gunakan tool
  search_company_policies.
- Jika pertanyaan MEMBUTUHKAN KEDUANYA, gunakan kedua tool, lalu
  gabungkan jawabannya secara koheren.
- Selalu gunakan get_hr_schema terlebih dahulu sebelum menulis SQL.
- Jawab dalam Bahasa Indonesia yang profesional dan ramah.
- Sertakan referensi sumber (misal: "Menurut Bab 2 Handbook...").
- Jika data tidak ditemukan, sampaikan dengan jujur.
```

### 6.3 Agent Reasoning Flow

```
User Input
    │
    ▼
┌───────────────────────┐
│  Classify Question    │
│  (LLM Reasoning)     │
│                       │
│  SQL? RAG? Hybrid?    │
└──────┬────────────────┘
       │
       ├──── SQL Path ──────────────────────────┐
       │     1. get_hr_schema()                 │
       │     2. Generate SQL query              │
       │     3. execute_hr_sql(query)           │
       │     4. Interpret results               │
       │                                        │
       ├──── RAG Path ──────────────────────────┤
       │     1. search_company_policies(query)  │
       │     2. Read retrieved chunks           │
       │     3. Synthesize answer with citation │
       │                                        │
       ├──── Hybrid Path ──────────────────────┤
       │     1. SQL Path (get data)             │
       │     2. RAG Path (get policy)           │
       │     3. Combine & synthesize            │
       │                                        │
       ▼                                        │
┌───────────────────────┐◄──────────────────────┘
│  Final Answer         │
│  (with sources cited) │
└───────────────────────┘
```

---

## 7. UI/UX Design

### 7.1 Layout Structure

```
┌──────────────────────────────────────────────────────────┐
│  🏢 HR Assistant AI — PT IDELOGI INDONESIA               │
│  Asisten cerdas untuk kebutuhan HR karyawan              │
├──────────┬───────────────────────────────────────────────┤
│ SIDEBAR  │  MAIN AREA                                    │
│          │                                               │
│ Settings │  [💬 HR Chat] [📊 Data Explorer] [📑 KB]     │
│ ───────  │  ─────────────────────────────────────────    │
│          │                                               │
│ 🔑 API  │  Tab 1 (Chat):                                │
│ Key      │  ┌─────────────────────────────────────┐      │
│          │  │ 🤖 Halo! Saya HR Assistant AI.      │      │
│ 🔄 Reset│  │    Ada yang bisa saya bantu?         │      │
│          │  ├─────────────────────────────────────┤      │
│ ───────  │  │ 👤 Berapa sisa cuti Siti Rahma?     │      │
│          │  ├─────────────────────────────────────┤      │
│ ℹ️ About │  │ 🤖 ▶ Mengambil skema database...    │      │
│          │  │    ▶ Menjalankan SQL query...        │      │
│          │  │    ▶ Menyusun jawaban...             │      │
│          │  │                                     │      │
│          │  │    Sisa cuti tahunan Siti Rahma      │      │
│          │  │    (EMP-005): **10 hari** dari       │      │
│          │  │    total 12 hari.                    │      │
│          │  └─────────────────────────────────────┘      │
│          │                                               │
│          │  [💬 Type your message here...          ]     │
│          │                                               │
└──────────┴───────────────────────────────────────────────┘
```

### 7.2 Tab Details

#### Tab 1: 💬 HR Chat
- Chat interface utama (`st.chat_input`, `st.chat_message`)
- Reasoning steps ditampilkan via `st.status()` (collapsible)
- SQL query ditampilkan via `st.code(query, language="sql")`
- Dokumen sumber RAG ditampilkan via `st.info()` / `st.expander()`

#### Tab 2: 📊 HR Data Explorer
- Dropdown untuk memilih tabel (`employees`, `leave_balances`, dll.)
- `st.dataframe()` untuk menampilkan data tabel
- `st.metric()` cards: Total Karyawan, Rata-rata Sisa Cuti, Klaim Pending

#### Tab 3: 📑 Company Knowledge Base
- Daftar dokumen yang aktif di knowledge base
- `st.file_uploader()` untuk upload dokumen baru (PDF, TXT, MD)
- Preview isi dokumen yang dipilih via `st.expander()`
- Tombol untuk menghapus dokumen dari knowledge base

---

## 8. Project Structure

```
hacktiv8/
├── PRD.md                          # Dokumen ini
├── README.md                       # Instruksi setup & penggunaan
├── requirements.txt                # Python dependencies
├── Dockerfile                      # (Optional) Container deployment
├── .gitignore                      # Ignore patterns
├── .env.example                    # Template environment variables
│
├── app.py                          # Entry point Streamlit (main app)
│
├── core/
│   ├── __init__.py
│   ├── agent.py                    # LangGraph ReAct agent setup
│   ├── config.py                   # Configuration & constants
│   └── prompts.py                  # System prompts & prompt templates
│
├── tools/
│   ├── __init__.py
│   ├── sql_tools.py                # SQL query tools (schema + execute)
│   └── rag_tools.py                # RAG search tools (policy search)
│
├── database/
│   ├── __init__.py
│   ├── init_db.py                  # Database initialization & sample data
│   ├── hr_database.db              # SQLite database (auto-generated)
│   └── schema.sql                  # (Optional) Raw SQL schema reference
│
├── knowledge_base/
│   ├── company_handbook.md         # Primary handbook document
│   └── uploads/                    # User-uploaded documents directory
│
├── vectorstore/
│   └── faiss_index/                # FAISS index files (auto-generated)
│
├── ui/
│   ├── __init__.py
│   ├── chat_tab.py                 # Chat tab UI component
│   ├── data_explorer_tab.py        # Data explorer tab UI component
│   ├── knowledge_base_tab.py       # Knowledge base tab UI component
│   └── sidebar.py                  # Sidebar UI component
│
└── tests/
    ├── test_sql_tools.py           # Unit tests for SQL tools
    ├── test_rag_tools.py           # Unit tests for RAG tools
    └── test_agent.py               # Integration tests for agent
```

---

## 9. Implementation Phases

### Phase 1: Foundation (Core Infrastructure)
**Goal**: Database, dokumen, dan project skeleton siap.

| # | Task | Output |
|---|---|---|
| 1.1 | Setup project structure & requirements.txt | Folder structure + dependencies |
| 1.2 | Implementasi `database/init_db.py` | SQLite DB dengan 4 tabel + sample data |
| 1.3 | Tulis `knowledge_base/company_handbook.md` | Dokumen handbook 5 bab lengkap |
| 1.4 | Implementasi `core/config.py` | Constants, paths, model config |

### Phase 2: Tools Development (Agent Capabilities)
**Goal**: Ketiga tool agent berfungsi dan teruji.

| # | Task | Output |
|---|---|---|
| 2.1 | Implementasi `tools/sql_tools.py` | get_hr_schema() + execute_hr_sql() dengan safety guard |
| 2.2 | Implementasi `tools/rag_tools.py` | Document loader, chunker, embedder, vector store, search |
| 2.3 | Unit test tools | Pastikan SQL safety & RAG retrieval berjalan benar |

### Phase 3: Agent Assembly (Brain)
**Goal**: LangGraph ReAct agent terintegrasi dengan semua tools.

| # | Task | Output |
|---|---|---|
| 3.1 | Implementasi `core/prompts.py` | System prompt & tool descriptions |
| 3.2 | Implementasi `core/agent.py` | create_react_agent dengan 3 tools |
| 3.3 | Integration test | Agent dapat menjawab SQL, RAG, dan Hybrid queries |

### Phase 4: UI Development (Frontend)
**Goal**: Antarmuka Streamlit lengkap dan polished.

| # | Task | Output |
|---|---|---|
| 4.1 | Implementasi `ui/sidebar.py` | API key input, reset, about |
| 4.2 | Implementasi `ui/chat_tab.py` | Chat UI + reasoning step display |
| 4.3 | Implementasi `ui/data_explorer_tab.py` | Table viewer + metrics |
| 4.4 | Implementasi `ui/knowledge_base_tab.py` | Doc list + file uploader |
| 4.5 | Implementasi `app.py` | Main entry point, tab routing |

### Phase 5: Polish & Testing
**Goal**: Aplikasi siap demo dan dipresentasikan.

| # | Task | Output |
|---|---|---|
| 5.1 | End-to-end testing semua use cases | Test report |
| 5.2 | Error handling & edge cases | Robust error messages |
| 5.3 | README.md documentation | Setup guide |
| 5.4 | (Optional) Dockerfile | Container deployment |

---

## 10. Testing Plan

### 10.1 Test Scenarios

#### SQL-Only Queries
| # | Input | Expected Tool | Expected Behavior |
|---|---|---|---|
| S1 | "Tampilkan semua karyawan di departemen Engineering" | execute_hr_sql | SELECT dari employees WHERE department |
| S2 | "Berapa sisa cuti EMP-005?" | execute_hr_sql | SELECT dari leave_balances |
| S3 | "Siapa yang paling banyak menggunakan cuti?" | execute_hr_sql | SELECT dengan ORDER BY used_days DESC |
| S4 | "Ada berapa klaim reimbursement yang masih pending?" | execute_hr_sql | SELECT COUNT dengan status filter |

#### RAG-Only Queries
| # | Input | Expected Tool | Expected Behavior |
|---|---|---|---|
| R1 | "Apa saja jenis cuti khusus yang tersedia?" | search_company_policies | Retrieve Bab 1 handbook |
| R2 | "Bagaimana prosedur klaim kacamata?" | search_company_policies | Retrieve Bab 2 handbook |
| R3 | "Berapa jam kerja inti perusahaan?" | search_company_policies | Retrieve Bab 3 handbook |
| R4 | "Apa hukuman untuk pelanggaran berat?" | search_company_policies | Retrieve Bab 5 handbook |

#### Hybrid Queries
| # | Input | Expected Tools | Expected Behavior |
|---|---|---|---|
| H1 | "Siti Rahma mau menikah. Berapa sisa cutinya dan apa aturan cuti menikah?" | SQL + RAG | Data cuti + kebijakan cuti khusus |
| H2 | "Budi Santoso mau klaim kacamata Rp 2 juta. Bisa tidak?" | SQL + RAG | Cek riwayat klaim + cek plafon di handbook |
| H3 | "Siapa saja karyawan probation dan apakah mereka berhak cuti?" | SQL + RAG | Data status + aturan cuti probation |

#### Safety Tests
| # | Input | Expected Behavior |
|---|---|---|
| X1 | "DELETE FROM employees" | Ditolak dengan pesan error |
| X2 | "DROP TABLE leave_balances" | Ditolak dengan pesan error |
| X3 | "UPDATE employees SET name='Hacker'" | Ditolak dengan pesan error |

---

## 11. Future Enhancements (v2.0+)

Fitur-fitur berikut dapat dikembangkan di iterasi berikutnya:

- [ ] **Multi-language Support**: Jawaban dalam Bahasa Inggris jika user bertanya dalam English
- [ ] **Auto-Charting**: Visualisasi grafik otomatis (bar chart cuti per departemen, pie chart kategori reimbursement)
- [ ] **Attendance Tracking**: Integrasi data absensi/kehadiran
- [ ] **Slack/Teams Integration**: Deploy sebagai bot di platform messaging perusahaan
- [ ] **Authentication**: Login karyawan untuk mengakses data pribadinya saja
- [ ] **Audit Log**: Mencatat semua query yang dijalankan agent untuk compliance
- [ ] **PDF Export**: Export hasil percakapan ke format PDF sebagai laporan
- [ ] **Voice Input**: Integrasi speech-to-text untuk input suara

---

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| API Key limit/quota exceeded | App tidak bisa menjawab | Tampilkan pesan error yang jelas + retry guidance |
| LLM generates incorrect SQL | Data salah ditampilkan | SQL safety guard + schema info tool |
| RAG retrieves irrelevant chunks | Jawaban tidak akurat | Tuning chunk size + overlap, gunakan k=3 |
| Large PDF upload crashes app | UX buruk | Limit file size (max 10MB) + progress indicator |
| Gemini model unavailable | App down | Fallback message + error handling |

---

## 13. Glossary

| Term | Definition |
|---|---|
| **ReAct Agent** | Reasoning + Acting pattern; agent yang melakukan penalaran kemudian mengambil aksi secara iteratif |
| **RAG** | Retrieval-Augmented Generation; teknik menggabungkan pencarian dokumen dengan generasi teks LLM |
| **Vector Store** | Database yang menyimpan dokumen dalam bentuk embedding vektor untuk pencarian semantik |
| **FAISS** | Facebook AI Similarity Search; library untuk pencarian similarity vektor yang efisien |
| **LangGraph** | Framework dari LangChain untuk membangun agent berbasis graph |
| **Tool Calling** | Kemampuan LLM untuk memanggil fungsi/tool eksternal berdasarkan kebutuhan |
| **Chunk** | Potongan dokumen yang dipecah untuk diproses dan di-embed ke vector store |
| **Embedding** | Representasi numerik (vektor) dari teks yang menangkap makna semantik |
| **System Prompt** | Instruksi awal yang diberikan ke LLM untuk menentukan perilaku dan persona |
| **Session State** | Mekanisme Streamlit untuk menyimpan variabel antar interaksi pengguna |
