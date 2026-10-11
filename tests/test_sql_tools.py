"""
Unit tests for SQL Tools and Safety Guards.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.init_db import init_database
from tools.sql_tools import execute_sql_query, execute_hr_sql, get_hr_schema


class TestSQLTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_database()

    def test_select_query_success(self):
        result = execute_sql_query("SELECT count(*) as count FROM employees")
        self.assertIsInstance(result, list)
        self.assertGreater(result[0]["count"], 0)

    def test_safety_guard_rejects_delete(self):
        output = execute_hr_sql.invoke({"sql_query": "DELETE FROM employees WHERE employee_id='EMP-001'"})
        self.assertIn("Query ditolak", output)
        self.assertIn("DELETE", output)

    def test_safety_guard_rejects_drop(self):
        output = execute_hr_sql.invoke({"sql_query": "DROP TABLE leave_balances"})
        self.assertIn("Query ditolak", output)

    def test_safety_guard_rejects_insert(self):
        output = execute_hr_sql.invoke({"sql_query": "INSERT INTO employees (employee_id, name) VALUES ('EMP-999', 'Fake')"})
        self.assertIn("Query ditolak", output)

    def test_schema_tool(self):
        schema_output = get_hr_schema.invoke({})
        self.assertIn("employees", schema_output)
        self.assertIn("leave_balances", schema_output)
        self.assertIn("leave_history", schema_output)
        self.assertIn("reimbursements", schema_output)


if __name__ == "__main__":
    unittest.main()
