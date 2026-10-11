"""Database initialization module for the HR Assistant AI.

This module sets up the SQLite database, creates the required schemas for
employees, leave balances, leave history, and reimbursements, and populates
them with realistic seed data if the tables are empty.
"""

import os
import sqlite3
from typing import Any, Dict, List

# Define database path relative to repository base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'hr_database.db')


def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection with foreign key support enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> str:
    """Initialize the HR database schema and populate seed data if tables are empty.

    Returns:
        str: Status message describing the initialization outcome.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            job_title TEXT NOT NULL,
            join_date TEXT NOT NULL,
            employment_status TEXT NOT NULL,
            manager_name TEXT
        );
    """)

    # 2. Create leave_balances table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            year INTEGER NOT NULL,
            total_quota INTEGER NOT NULL,
            used_days INTEGER DEFAULT 0,
            remaining_days INTEGER GENERATED ALWAYS AS (total_quota - used_days) STORED,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        );
    """)

    # 3. Create leave_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_history (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            days_count INTEGER NOT NULL,
            status TEXT NOT NULL,
            reason TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        );
    """)

    # 4. Create reimbursements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reimbursements (
            claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            submit_date TEXT NOT NULL,
            receipt_date TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        );
    """)

    conn.commit()

    # Seed data definitions
    sample_employees = [
        ("EMP-001", "Budi Santoso", "budi.santoso@idelogi.co.id", "Engineering", "Senior Developer", "2021-03-15", "Active", "Fajar Nugroho"),
        ("EMP-002", "Dewi Lestari", "dewi.lestari@idelogi.co.id", "Marketing", "Marketing Manager", "2020-07-01", "Active", None),
        ("EMP-003", "Rian Pratama", "rian.pratama@idelogi.co.id", "Engineering", "Junior Developer", "2024-01-10", "Active", "Fajar Nugroho"),
        ("EMP-004", "Anisa Wijaya", "anisa.wijaya@idelogi.co.id", "Finance", "Finance Analyst", "2022-05-20", "Active", "Linda Permata"),
        ("EMP-005", "Siti Rahma", "siti.rahma@idelogi.co.id", "Marketing", "Marketing Staff", "2023-08-14", "Active", "Dewi Lestari"),
        ("EMP-006", "Hendra Gunawan", "hendra.gunawan@idelogi.co.id", "Operations", "Operations Lead", "2019-11-03", "Active", None),
        ("EMP-007", "Maya Putri", "maya.putri@idelogi.co.id", "HR", "HR Specialist", "2022-02-28", "Active", None),
        ("EMP-008", "Fajar Nugroho", "fajar.nugroho@idelogi.co.id", "Engineering", "Tech Lead", "2018-06-15", "Active", None),
        ("EMP-009", "Linda Permata", "linda.permata@idelogi.co.id", "Finance", "Finance Manager", "2019-04-22", "Active", None),
        ("EMP-010", "Arief Rahman", "arief.rahman@idelogi.co.id", "Operations", "Operations Staff", "2025-09-01", "Probation", "Hendra Gunawan"),
    ]

    sample_leave_balances = [
        ("EMP-001", 2026, 12, 4),
        ("EMP-002", 2026, 12, 7),
        ("EMP-003", 2026, 12, 3),
        ("EMP-004", 2026, 12, 6),
        ("EMP-005", 2026, 12, 2),
        ("EMP-006", 2026, 12, 5),
        ("EMP-007", 2026, 12, 1),
        ("EMP-008", 2026, 12, 8),
        ("EMP-009", 2026, 12, 3),
        ("EMP-010", 2026, 0, 0),
    ]

    sample_leave_history = [
        ("EMP-001", "annual", "2026-02-16", "2026-02-17", 2, "approved", "Liburan keluarga ke Yogyakarta"),
        ("EMP-001", "annual", "2026-05-04", "2026-05-05", 2, "approved", "Keperluan pribadi"),
        ("EMP-001", "sick", "2026-07-10", "2026-07-11", 2, "approved", "Sakit demam dan flu (disertai surat dokter)"),
        ("EMP-002", "annual", "2026-03-09", "2026-03-13", 5, "approved", "Liburan mudik awal Ramadan"),
        ("EMP-002", "annual", "2026-06-22", "2026-06-23", 2, "approved", "Acara keluarga di Bandung"),
        ("EMP-002", "sick", "2026-08-05", "2026-08-05", 1, "approved", "Pemeriksaan kesehatan rawat jalan"),
        ("EMP-003", "annual", "2026-04-15", "2026-04-17", 3, "approved", "Menghadiri wisuda adik di Malang"),
        ("EMP-003", "sick", "2026-09-01", "2026-09-02", 2, "approved", "Istirahat sakit tifus ringan"),
        ("EMP-003", "annual", "2026-10-20", "2026-10-22", 3, "rejected", "Beban sprint akhir kuartal sedang tinggi"),
        ("EMP-004", "annual", "2026-01-22", "2026-01-23", 2, "approved", "Urusan administrasi perbankan keluarga"),
        ("EMP-004", "annual", "2026-07-27", "2026-07-30", 4, "approved", "Liburan pertengahan tahun ke Bali"),
        ("EMP-005", "annual", "2026-05-18", "2026-05-19", 2, "approved", "Persiapan dokumen administrasi pernikahan"),
        ("EMP-005", "marriage", "2026-11-16", "2026-11-18", 3, "pending", "Cuti pernikahan resmi"),
        ("EMP-006", "annual", "2026-02-02", "2026-02-06", 5, "approved", "Cuti tahunan awal tahun"),
        ("EMP-006", "paternity", "2026-08-10", "2026-08-11", 2, "approved", "Pendampingan kelahiran anak kedua"),
        ("EMP-007", "annual", "2026-03-30", "2026-03-30", 1, "approved", "Perpanjangan paspor dan urusan dokumen pribadi"),
        ("EMP-007", "bereavement", "2026-06-12", "2026-06-13", 2, "approved", "Duka cita anggota keluarga dekat meninggal dunia"),
        ("EMP-008", "annual", "2026-01-05", "2026-01-09", 5, "approved", "Liburan awal tahun bersama keluarga"),
        ("EMP-008", "annual", "2026-08-18", "2026-08-20", 3, "approved", "Istirahat pasca go-live proyek sistem internal"),
        ("EMP-008", "sick", "2026-04-06", "2026-04-07", 2, "approved", "Radang tenggorokan akut disertai surat dokter"),
        ("EMP-009", "annual", "2026-06-08", "2026-06-10", 3, "approved", "Family gathering di Puncak"),
        ("EMP-010", "annual", "2026-09-25", "2026-09-26", 2, "rejected", "Karyawan masih dalam masa percobaan (probation), belum memiliki kuota cuti tahunan"),
    ]

    sample_reimbursements = [
        ("EMP-001", "glasses", 1200000.0, "2026-03-10", "2026-03-08", "paid", "Klaim penggantian kacamata kerja tahun 2026"),
        ("EMP-001", "transport", 185000.0, "2026-05-15", "2026-05-14", "paid", "Transportasi taksi online meeting client di SCBD"),
        ("EMP-002", "training", 3500000.0, "2026-04-02", "2026-03-28", "paid", "Workshop Digital Marketing Leadership"),
        ("EMP-003", "training", 1750000.0, "2026-06-10", "2026-06-05", "approved", "Sertifikasi AWS Certified Cloud Practitioner"),
        ("EMP-004", "medical", 450000.0, "2026-07-12", "2026-07-11", "paid", "Kwitansi pemeriksaan dokter gigi dan obat resep"),
        ("EMP-005", "transport", 220000.0, "2026-08-20", "2026-08-19", "approved", "Transportasi operasional photoshoot campaign produk"),
        ("EMP-006", "medical", 380000.0, "2026-09-05", "2026-09-03", "paid", "Pembelian obat resep dokter klinik mitra"),
        ("EMP-007", "medical", 275000.0, "2026-10-02", "2026-09-30", "pending", "Konsultasi dokter umum dan obat flu musiman"),
        ("EMP-008", "glasses", 1450000.0, "2026-02-18", "2026-02-15", "paid", "Penggantian lensa kacamata anti-radiasi"),
        ("EMP-008", "training", 4500000.0, "2026-07-05", "2026-07-01", "paid", "Tiket Konferensi Arsitektur Microservices 2026"),
        ("EMP-009", "transport", 550000.0, "2026-08-15", "2026-08-14", "rejected", "Klaim transport melebihi plafon harian tanpa approval manajer sebelumnya"),
        ("EMP-010", "transport", 125000.0, "2026-09-18", "2026-09-17", "pending", "Pengantaran dokumen kontrak fisik ke notaris rekanan"),
    ]

    inserted_summary = []

    # Check and insert employees
    cursor.execute("SELECT COUNT(*) FROM employees;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO employees (
                employee_id, name, email, department, job_title, join_date, employment_status, manager_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, sample_employees)
        inserted_summary.append(f"{len(sample_employees)} employees")

    # Check and insert leave balances
    cursor.execute("SELECT COUNT(*) FROM leave_balances;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO leave_balances (
                employee_id, year, total_quota, used_days
            ) VALUES (?, ?, ?, ?);
        """, sample_leave_balances)
        inserted_summary.append(f"{len(sample_leave_balances)} leave balances")

    # Check and insert leave history
    cursor.execute("SELECT COUNT(*) FROM leave_history;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO leave_history (
                employee_id, leave_type, start_date, end_date, days_count, status, reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, sample_leave_history)
        inserted_summary.append(f"{len(sample_leave_history)} leave history records")

    # Check and insert reimbursements
    cursor.execute("SELECT COUNT(*) FROM reimbursements;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO reimbursements (
                employee_id, category, amount, submit_date, receipt_date, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, sample_reimbursements)
        inserted_summary.append(f"{len(sample_reimbursements)} reimbursement records")

    conn.commit()
    conn.close()

    if inserted_summary:
        return f"Database initialized at {DB_PATH}. Populated: {', '.join(inserted_summary)}."
    return f"Database at {DB_PATH} already initialized with existing data."


def get_all_table_data(table_name: str) -> List[Dict[str, Any]]:
    """Retrieve all rows from a given database table as a list of dictionaries.

    Args:
        table_name: The table name to query (must be one of the recognized tables).

    Returns:
        List[Dict[str, Any]]: List of dictionary representations of the rows.

    Raises:
        ValueError: If the table name is not in the whitelist.
    """
    valid_tables = {"employees", "leave_balances", "leave_history", "reimbursements"}
    if table_name not in valid_tables:
        raise ValueError(f"Invalid table name '{table_name}'. Valid tables: {sorted(valid_tables)}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result


if __name__ == '__main__':
    status = init_database()
    print(status)
    for tbl in ["employees", "leave_balances", "leave_history", "reimbursements"]:
        data = get_all_table_data(tbl)
        print(f"Table '{tbl}': {len(data)} rows found.")
