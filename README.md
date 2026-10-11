# 🏢 HR Assistant AI — PT IDELOGI INDONESIA
> **Hybrid AI Agent (SQL + RAG) berbasis Streamlit, LangGraph, dan Google Gemini**

Proyek ini merupakan modifikasi dan evolusi dari demo reference [chatbot-streamlit-demo](https://github.com/adiptamartulandi/chatbot-streamlit-demo). Dikembangkan untuk mendemonstrasikan kapabilitas **Enterprise Hybrid AI Agent** yang mampu menggabungkan data kuantitatif karyawan (SQL) dengan data kualitatif peraturan perusahaan (RAG Knowledge Base).

---

## 🌟 Fitur Utama & Diferensiasi

1. **🧠 Hybrid AI Agent (LangGraph ReAct Pattern)**
   - Menggunakan model **Google Gemini (3.6 Flash / 2.5 Flash / Pro)** dengan reasoning loop otonom.
   - Otomatis melakukan routing: kapan harus membaca database SQL, kapan harus mencari di dokumen kebijakan, atau kapan harus menggabungkan keduanya (*Hybrid Query*).

2. **📊 SQL Database Tool (Read-Only Guard)**
   - Database SQLite terintegrasi (`hr_database.db`) dengan 4 tabel: `employees`, `leave_balances`, `leave_history`, dan `reimbursements`.
   - Dilengkapi **SQL Safety Guard** yang secara tegas menolak perintah destruktif (`DROP`, `DELETE`, `UPDATE`, `INSERT`) dan hanya mengizinkan `SELECT`.

3. **📑 RAG Document Knowledge Base (FAISS + Gemini Embeddings)**
   - Dilengkapi dokumen default komprehensif `company_handbook.md` (5 bab: Cuti, Benefit & Reimbursement, Jam Kerja, Pelatihan, Kode Etik).
   - Pengguna dapat mengunggah file SOP baru (`.pdf`, `.txt`, `.md`) langsung dari antarmuka web, dan sistem akan mengindeksnya secara otomatis.

4. **✨ UI Streamlit Multi-Tab yang Transparan**
   - **Tab 1 — 💬 HR Chatbot**: Menampilkan percakapan interaktif lengkap dengan penalaran agent via `st.status()` dan inspeksi query SQL / kutipan dokumen.
   - **Tab 2 — 📊 HR Data Explorer**: Ringkasan KPI dan tabel interaktif untuk memverifikasi keakuratan database.
   - **Tab 3 — 📑 Knowledge Base**: Eksplorasi dokumen aktif dan fitur upload SOP baru.

---

## 🛠️ Instalasi & Menjalankan Aplikasi

### 1. Prasyarat
- Python 3.10 atau lebih baru.
- Google AI API Key (Dapat diperoleh gratis di [Google AI Studio](https://aistudio.google.com)).

### 2. Clone / Masuk ke Direktori Proyek
```bash
cd /Users/ahmadhidayatullah/Documents/Projects/hacktiv8
```

### 3. Buat dan Aktifkan Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Untuk macOS / Linux
# venv\Scripts\activate   # Untuk Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Inisialisasi Database (Opsional, otomatis saat app dijalankan)
```bash
python3 database/init_db.py
```

### 6. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```
Buka browser di URL yang tertera (biasanya `http://localhost:8501`). Masukkan Google AI API Key Anda di sidebar sebelah kiri untuk mulai mengobrol!

---

## 🧪 Skenario Pengujian (Demonstrasi)

Coba uji agent dengan berbagai jenis skenario berikut:

| Kategori | Pertanyaan Contoh | Ekspektasi Perilaku Agent |
|---|---|---|
| **SQL Data** | *"Berapa sisa cuti tahunan milik Rian Pratama (EMP-003)?"* | Memanggil `execute_hr_sql` dan menjawab angka sisa cuti (9 hari). |
| **SQL Data** | *"Siapa saja karyawan di departemen Engineering?"* | Menjalankan filter SQL dan menampilkan daftar staf Engineering. |
| **RAG Policy** | *"Berapa plafon klaim kacamata dan apa syarat pengajuannya?"* | Memanggil `search_company_policies`, mengutip plafon Rp 1.500.000 / 2 tahun dan resep dokter. |
| **RAG Policy** | *"Apakah karyawan berhak WFH dan berapa hari dalam seminggu?"* | Mengutip Bab 3 terkait kuota WFH maksimal 2 hari/minggu. |
| **HYBRID** | *"Saya Siti Rahma (EMP-005). Saya berencana menikah bulan depan. Berapa sisa cuti saya saat ini, dan apakah cuti menikah memotong cuti tahunan?"* | **Langkah 1**: Query SQL saldo cuti Siti Rahma (10 hari).<br>**Langkah 2**: Cari aturan cuti menikah di handbook (3 hari berbayar).<br>**Langkah 3**: Merangkum bahwa kuota cuti tahunan tetap utuh 10 hari. |
| **Safety Guard** | *"DELETE FROM employees WHERE employee_id='EMP-001'"* | Sistem menolak query dan memberikan peringatan keamanan. |

---

## 📁 Struktur Direktori
```
hacktiv8/
├── app.py                      # Entry point Streamlit aplikasi
├── PRD.md                      # Product Requirements Document
├── README.md                   # Dokumentasi proyek
├── requirements.txt            # Daftar pustaka dependencies
├── core/
│   ├── config.py               # Konfigurasi & konstanta
│   ├── prompts.py              # System prompt & template persona
│   └── agent.py                # LangGraph ReAct agent builder
├── database/
│   ├── init_db.py              # Inisialisasi skema & sample data SQLite
│   └── hr_database.db          # File SQLite database
├── knowledge_base/
│   ├── company_handbook.md     # Dokumen kebijakan 5 bab
│   └── uploads/                # Direktori file upload user
├── tools/
│   ├── sql_tools.py            # LangChain SQL tools dengan Read-Only Guard
│   └── rag_tools.py            # LangChain RAG tools dengan FAISS
├── ui/
│   ├── sidebar.py              # Komponen sidebar (API key, model, reset)
│   ├── chat_tab.py             # Komponen tab chat dengan visualisasi status
│   ├── data_explorer_tab.py    # Komponen tab visualisasi database
│   └── knowledge_base_tab.py   # Komponen tab manajemen dokumen & upload
└── tests/
    ├── test_sql_tools.py       # Unit test SQL tools & safety guard
    └── test_rag_tools.py       # Unit test RAG tools
```
