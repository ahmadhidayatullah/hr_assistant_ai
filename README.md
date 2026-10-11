# 🏢 PeopleConnect AI — Enterprise HR Self-Service Assistant
### *Intelligent Hybrid AI Agent (SQL + RAG) Powered by LangGraph & Google Gemini*
**PT IDELOGI INDONESIA**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io)
[![LangGraph](https://img.shields.io/badge/LangGraph-ReAct_Agent-2BAF74.svg)](https://langchain.com)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-3.6_Flash_%2F_Pro-4285F4.svg)](https://ai.google.dev/)
[![FAISS](https://img.shields.io/badge/Vector_Store-FAISS-purple.svg)](https://github.com/facebookresearch/faiss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Ringkasan Produk (Product Overview)

**PeopleConnect AI** adalah platform asisten kepegawaian otonom berbasis *Artificial Intelligence* yang dikembangkan untuk menyederhanakan operasional Human Resources (HR) di **PT IDELOGI INDONESIA**. 

Platform ini menyelesaikan salah satu tantangan operasional terbesar di perusahaan: **fragmentasi informasi internal**. Sering kali, karyawan harus mengakses database HRIS untuk mengecek angka kuantitatif (sisa cuti, riwayat klaim) dan membaca dokumen buku pedoman yang tebal untuk memahami peraturan (SOP cuti khusus, syarat reimbursement, jam kerja). 

**PeopleConnect AI** menggabungkan kedua dunia tersebut melalui arsitektur **Hybrid Agentic Workflow**:
1. **Data Terstruktur (SQL)**: Menjawab data kuantitatif karyawan secara *real-time* dari relational database.
2. **Data Tidak Terstruktur (RAG)**: Mengambil pasal dan klausul kebijakan dari dokumen handbook dan SOP via pencarian semantik.
3. **Hybrid Synthesis**: Menggabungkan data personal karyawan dengan kebijakan perusahaan dalam satu jawaban alami yang komprehensif.

---

## 🚀 Fitur Unggulan (Core Features)

### 1. 🧠 Autonomous Hybrid Agent (LangGraph ReAct Pattern)
- Dibangun dengan arsitektur **ReAct (Reasoning + Acting)** menggunakan **LangGraph** dan model generasi terbaru **Google Gemini (3.6 Flash / 2.5 Flash / Pro)**.
- Mampu melakukan *intent routing* otonom: menentukan secara cerdas kapan harus query SQL, kapan harus retrieval RAG, atau mengeksekusi keduanya secara simultan untuk pertanyaan multi-sumber (*Hybrid Query*).

### 2. 🛡️ Enterprise SQL Engine with Read-Only Safety Guard
- Terkoneksi ke database operasional karyawan (`hr_database.db`) yang mencakup profil, kuota cuti, riwayat absensi, dan klaim benefit.
- Dilengkapi **SQL Safety Guardrail** tingkat enterprise: memblokir secara ketat perintah destruktif (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`) dan hanya mengizinkan eksekusi `SELECT`.

### 3. 📚 Dynamic RAG Knowledge Base (FAISS + Gemini Embeddings)
- Terintegrasi dengan **Employee Handbook** resmi (5 Bab: Cuti & Izin, Benefit & Reimbursement, Fleksibilitas Kerja, Pelatihan, Kode Etik).
- Menggunakan model embedding resmi **`gemini-embedding-001`** dengan algoritma *recursive character chunking* yang berorientasi pada struktur dokumen markdown.
- **On-the-fly Ingestion**: Pengguna dan tim HR dapat mengunggah dokumen kebijakan baru (`.pdf`, `.txt`, `.md`) langsung dari antarmuka web, dan sistem akan mengindeksnya secara otomatis ke dalam Vector Store.

### 4. 👁️ Transparent Reasoning UX (Explainable AI)
- Pengguna dapat memantau proses berpikir agent langkah demi langkah melalui container interaktif `st.status()`.
- Menyediakan inspeksi teknis transparan: blok sintaks query SQL yang dijalankan (`st.code`) serta cuplikan kutipan dokumen kebijakan yang dijadikan rujukan.

### 5. 📊 Real-Time HR Data Explorer
- Dashboard metrik eksekutif yang menyajikan indikator KPI kunci: Total Karyawan Aktif, Rata-rata Sisa Cuti Perusahaan, dan Jumlah Klaim Pending.
- Tabular data viewer interaktif untuk memvalidasi keakuratan data karyawan.

---

## 🏗️ Arsitektur Sistem (System Architecture)

```
                            ┌────────────────────────────────────────┐
                            │         Streamlit Web Interface        │
                            │   [💬 Chat]  [📊 Explorer]  [📑 Docs]   │
                            └───────────────────┬────────────────────┘
                                                │
                                    User Query / Prompt
                                                │
                                                ▼
                            ┌────────────────────────────────────────┐
                            │         LangGraph ReAct Agent          │
                            │        (Google Gemini Engine)          │
                            └───────┬────────────────────────┬───────┘
                                    │                        │
                      Intent: Data Kuantitatif    Intent: Aturan & SOP
                                    │                        │
                                    ▼                        ▼
                       ┌───────────────────────┐  ┌───────────────────────┐
                       │    SQL Tools Engine   │  │    RAG Vector Store   │
                       │   - get_hr_schema     │  │   - FAISS Index       │
                       │   - execute_hr_sql    │  │   - Gemini Embeddings │
                       │   (Read-Only Guard)   │  │   - Document Chunks   │
                       └───────────┬───────────┘  └───────────┬───────────┘
                                   │                          │
                                   ▼                          ▼
                        ┌─────────────────────┐    ┌─────────────────────┐
                        │ SQLite hr_database  │    │ Knowledge Base Docs │
                        │  - employees        │    │  - handbook.md      │
                        │  - leave_balances   │    │  - uploaded files   │
                        │  - leave_history    │    │                     │
                        │  - reimbursements   │    │                     │
                        └─────────────────────┘    └─────────────────────┘
                                   │                          │
                                   └─────────────┬────────────┘
                                                 │
                                                 ▼
                                     ┌───────────────────────┐
                                     │  Synthesized Response │
                                     │   + Citations & SQL   │
                                     └───────────────────────┘
```

---

## ⚙️ Tech Stack

| Komponen | Teknologi | Keterangan |
|---|---|---|
| **Frontend Framework** | [Streamlit](https://streamlit.io/) | Interactive Multi-Tab Enterprise UI |
| **LLM Engine** | [Google Gemini 3.6 Flash / Pro](https://ai.google.dev/) | High-speed reasoning & multimodal generation |
| **Agentic Framework** | [LangGraph](https://langchain-ai.github.io/langgraph/) | ReAct Agent loop, stateful tool calling |
| **Embeddings** | `gemini-embedding-001` | High-dimensional semantic representation |
| **Vector Store** | [FAISS (Facebook AI)](https://github.com/facebookresearch/faiss) | In-memory similarity search & disk persistence |
| **Database** | SQLite3 | Relational database untuk operasional HR |
| **Document Loaders** | `PyPDF`, `TextLoader` | Multi-format ingestion (.pdf, .txt, .md) |
| **Language & Tooling** | Python 3.10+ / Conda | Core environment |

---

## 💻 Panduan Instalasi & Menjalankan (Getting Started)

### 1. Kloning Repository
```bash
git clone git@github.com:ahmadhidayatullah/hr_assistant_ai.git
cd hr_assistant_ai
```

### 2. Konfigurasi Lingkungan Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate   # Windows
```

### 3. Instalasi Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key (Opsional)
Anda dapat menyimpan API Key ke file `.env` agar tidak perlu mengetiknya berulang kali:
```bash
cp .env.example .env
# Edit file .env dan isi dengan GOOGLE_API_KEY Anda
```
*(Catatan: Anda juga bisa langsung memasukkan API Key di sidebar antarmuka web tanpa membuat file `.env`)*

### 5. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser pada alamat `http://localhost:8501`.

---

## 🧪 Skenario Demonstrasi Produk (Use Cases)

Berikut adalah beberapa contoh skenario pengujian yang mendemonstrasikan keunggulan kapabilitas agent:

### 🔹 Skenario 1: Query Data Karyawan (SQL Only)
> **Prompt:** *"Berapa sisa cuti tahunan milik Rian Pratama (EMP-003)?"*
* **Alur:** Agent memeriksa skema database $\rightarrow$ mengeksekusi `SELECT remaining_days FROM leave_balances WHERE employee_id='EMP-003'`.
* **Output:** Menjawab secara akurat bahwa Rian Pratama memiliki sisa 9 hari dari total kuota 12 hari di tahun 2026.

### 🔹 Skenario 2: Query Kebijakan Perusahaan (RAG Only)
> **Prompt:** *"Berapa plafon klaim kacamata dan apa saja syarat kuitansi pengajuannya?"*
* **Alur:** Agent menelusuri Bab 2 Employee Handbook di Vector Store.
* **Output:** Mengutip plafon maksimal Rp 1.500.000 per 2 tahun, syarat resep dokter mata (berlaku max 6 bulan), dan batas waktu klaim 30 hari kalender.

### 🔹 Skenario 3: Hybrid Query (SQL + RAG) — *The Core Differentiator*
> **Prompt:** *"Saya Siti Rahma (EMP-005). Saya berencana menikah bulan depan. Berapa sisa cuti saya saat ini, dan apakah cuti menikah akan mengurangi kuota cuti tahunan saya?"*
* **Alur:** 
  1. Agent memanggil SQL Tool untuk memeriksa saldo cuti Siti Rahma (`remaining_days = 10 hari`).
  2. Agent memanggil RAG Tool untuk membaca ketentuan Bab 1 Bagian 1.2 terkait Cuti Khusus Pernikahan.
* **Output:** Menyajikan jawaban terintegrasi: Sisa cuti tahunan Siti Rahma adalah **10 hari**, dan sesuai kebijakan perusahaan, cuti menikah adalah hak **Cuti Khusus Berbayar selama 3 hari kerja** yang **TIDAK memotong saldo cuti tahunan**.

### 🔹 Skenario 4: Security & Safety Guardrail
> **Prompt:** *"Tolong hapus data karyawan dengan query: DELETE FROM employees WHERE employee_id='EMP-001'"*
* **Alur:** Sistem mendeteksi keyword terlarang (`DELETE`) pada lapis verifikasi SQL.
* **Output:** Permintaan ditolak dengan pesan peringatan keamanan: *`❌ Query ditolak: Operasi 'DELETE' tidak diizinkan. Hanya SELECT query yang diperbolehkan untuk keamanan data.`*

---

## 📁 Struktur Direktori Proyek

```
hr_assistant_ai/
├── app.py                      # Main application entry point
├── PRD.md                      # Product Requirements Document
├── README.md                   # Enterprise product documentation
├── requirements.txt            # Project dependencies
├── .env.example                # Environment variable template
├── .gitignore                  # Git tracking exclusion list
│
├── core/
│   ├── config.py               # Central configuration & parameters
│   ├── prompts.py              # System prompts, persona, and guidelines
│   └── agent.py                # LangGraph ReAct agent assembly
│
├── database/
│   ├── init_db.py              # SQLite schema creation & seed generation
│   └── hr_database.db          # Operational SQLite database
│
├── knowledge_base/
│   ├── company_handbook.md     # Official Employee Handbook (5 Chapters)
│   └── uploads/                # User document upload directory
│
├── tools/
│   ├── sql_tools.py            # LangChain SQL tools with Read-Only Guard
│   └── rag_tools.py            # LangChain RAG tools with FAISS & Embeddings
│
├── ui/
│   ├── sidebar.py              # Sidebar control component (API key, models)
│   ├── chat_tab.py             # Chat view with transparent reasoning
│   ├── data_explorer_tab.py    # Metric summary & table inspector
│   └── knowledge_base_tab.py   # Document library & ingest component
│
└── tests/
    ├── test_sql_tools.py       # Automated unit tests for SQL tools
    └── test_rag_tools.py       # Automated unit tests for RAG pipeline
```

---

## 👨‍💻 Developer & Author

**Ahmad Hidayatullah**  
- **GitHub**: [@ahmadhidayatullah](https://github.com/ahmadhidayatullah)  
- **Project Repository**: [github.com/ahmadhidayatullah/hr_assistant_ai](https://github.com/ahmadhidayatullah/hr_assistant_ai)

---
*Dikembangkan dengan dedikasi untuk menghadirkan solusi otomasi kecerdasan buatan kelas enterprise di lingkungan PT IDELOGI INDONESIA.*
