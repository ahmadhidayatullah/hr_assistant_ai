"""
SQL Tools for HR Assistant AI.

Provides database interaction tools for a LangGraph ReAct agent:
- execute_sql_query: Internal helper to run SQL queries and return dict results.
- get_table_schema: Internal helper to introspect table columns and constraints.
- get_hr_schema: LangChain tool to inspect database structure and sample rows.
- execute_hr_sql: LangChain tool to execute secure, read-only SELECT queries.
"""
import os
import re
import sys
import json
import sqlite3
from typing import List, Dict, Any, Optional

# Ensure parent directory is in Python path for module resolution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import DB_PATH, FORBIDDEN_SQL_KEYWORDS
from langchain_core.tools import tool

try:
    from database.init_db import init_database
except ImportError:
    def init_database() -> None:
        """
        Fallback initialization function in case database.init_db
        is loaded dynamically or not yet present at import time.
        """
        try:
            import importlib
            mod = importlib.import_module("database.init_db")
            if hasattr(mod, "init_database"):
                mod.init_database()
        except (ImportError, AttributeError):
            pass


def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """
    Internal helper to execute an SQL query against the SQLite database.

    Args:
        query: SQL query string to execute.

    Returns:
        List of dicts representing rows for queries returning data (e.g. SELECT, PRAGMA),
        affected_rows count for non-SELECT queries, or an error dict if execution fails.
    """
    if not os.path.exists(DB_PATH):
        init_database()

    # Ensure the parent directory of DB_PATH exists
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)

        # Check if query returned rows (e.g. SELECT or PRAGMA statements)
        if cursor.description is not None:
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
        else:
            conn.commit()
            results = [{"affected_rows": cursor.rowcount}]
        return results
    except sqlite3.Error as e:
        return [{"error": str(e)}]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        if conn:
            conn.close()


def get_table_schema() -> Dict[str, List[Dict[str, str]]]:
    """
    Internal helper to retrieve the schema of all user tables in the HR database.

    Queries sqlite_master for table names and PRAGMA table_info for column definitions.

    Returns:
        Dictionary mapping table names to lists of column information dictionaries:
        {table_name: [{"name": str, "type": str, "notnull": int, "pk": int}, ...]}
    """
    if not os.path.exists(DB_PATH):
        init_database()

    schema: Dict[str, List[Dict[str, Any]]] = {}

    # Query sqlite_master for user tables, excluding SQLite internal tables
    table_rows = execute_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
    )

    for t_row in table_rows:
        if "error" in t_row or "name" not in t_row:
            continue
        table_name = t_row["name"]

        pragma_rows = execute_sql_query(f"PRAGMA table_info({table_name});")
        columns = []
        for col in pragma_rows:
            if "error" in col:
                continue
            columns.append({
                "name": str(col.get("name", "")),
                "type": str(col.get("type", "")),
                "notnull": col.get("notnull", 0),
                "pk": col.get("pk", 0),
            })
        schema[table_name] = columns

    return schema


@tool
def get_hr_schema() -> str:
    """Get the complete database schema and sample data for the HR database. Use this tool FIRST before writing any SQL query to understand the table structures, column names, and data types."""
    if not os.path.exists(DB_PATH):
        init_database()

    schema = get_table_schema()
    if not schema:
        return "Database HR tidak memiliki tabel atau database belum diinisialisasi."

    output_lines = []
    for table_name, columns in schema.items():
        output_lines.append(f"Table: {table_name}")

        # Format column definitions
        col_strs = []
        for col in columns:
            name = col.get("name", "")
            data_type = col.get("type", "")
            is_pk = col.get("pk") in (1, "1", True)
            if is_pk:
                col_strs.append(f"{name} ({data_type}, PK)")
            else:
                col_strs.append(f"{name} ({data_type})")
        output_lines.append(f"Columns: {', '.join(col_strs)}")

        # Retrieve first 3 rows as sample data
        sample_rows = execute_sql_query(f"SELECT * FROM {table_name} LIMIT 3;")
        output_lines.append("Sample Data:")
        if sample_rows and "error" not in sample_rows[0]:
            for row in sample_rows:
                row_values = [str(v) if v is not None else "NULL" for v in row.values()]
                output_lines.append(f"  {' | '.join(row_values)}")
        else:
            output_lines.append("  (No data available)")

        output_lines.append("")  # Blank line separating tables

    return "\n".join(output_lines).strip()


@tool
def execute_hr_sql(sql_query: str) -> str:
    """Execute a SQL query against the HR database. ONLY SELECT queries are allowed for security. Use this tool after understanding the schema with get_hr_schema. Args: sql_query: The SQL SELECT query to execute."""
    if not os.path.exists(DB_PATH):
        init_database()

    # Validate non-empty query
    if not sql_query or not sql_query.strip():
        return "❌ Query ditolak: Query SQL tidak boleh kosong."

    clean_query = sql_query.strip()

    # Strip markdown code blocks if the agent wrapped the query in them
    if clean_query.startswith("```"):
        lines = clean_query.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        clean_query = "\n".join(lines).strip()

    # CRITICAL: SQL Safety Guard
    # 1. Check if any word in FORBIDDEN_SQL_KEYWORDS appears as a standalone SQL keyword
    for keyword in FORBIDDEN_SQL_KEYWORDS:
        pattern = rf"\b{re.escape(keyword)}\b"
        if re.search(pattern, clean_query, re.IGNORECASE):
            return f"❌ Query ditolak: Operasi '{keyword}' tidak diizinkan. Hanya SELECT query yang diperbolehkan untuk keamanan data."

    # 2. Reject if query does not start with SELECT (case-insensitive after stripping)
    if not clean_query.upper().startswith("SELECT"):
        return "❌ Query ditolak: Hanya SELECT query yang diperbolehkan untuk keamanan data."

    # Execute query
    results = execute_sql_query(clean_query)

    # Handle errors gracefully
    if results and "error" in results[0]:
        return f"❌ Terjadi kesalahan saat mengeksekusi query:\nQuery: {clean_query}\nError: {results[0]['error']}"

    # Handle empty results
    if not results:
        return f"Query:\n```sql\n{clean_query}\n```\n\nHasil: Tidak ada data yang ditemukan (0 baris)."

    # Format results nicely as a markdown table
    columns = list(results[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    data_rows = []
    for row in results:
        row_values = [str(row.get(col, "")) if row.get(col) is not None else "NULL" for col in columns]
        data_rows.append("| " + " | ".join(row_values) + " |")

    table_content = "\n".join([header, separator] + data_rows)
    return f"Query:\n```sql\n{clean_query}\n```\n\nHasil ({len(results)} baris):\n{table_content}"
