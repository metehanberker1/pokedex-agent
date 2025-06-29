"""Thin DB wrapper with safe read-only `run_query`."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, List

from loguru import logger

DB_PATH = Path(__file__).parent / "pokedex.db"


def run_query(sql: str, db_path: Path = DB_PATH) -> List[dict[str, Any]]:
    """Execute a read-only SQL query on the Pokémon database."""
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT statements are permitted")
    
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}. Run ETL first.")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql).fetchall()
        conn.close()
        logger.debug("SQL query returned: %d rows", len(rows))
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        logger.error(f"SQL error: {e}")
        raise ValueError(f"SQL execution failed: {e}")


def get_table_info(table_name: str, db_path: Path = DB_PATH) -> List[dict[str, Any]]:
    """Get schema information for a table."""
    return run_query(f"PRAGMA table_info({table_name})", db_path)


def list_tables(db_path: Path = DB_PATH) -> List[str]:
    """List all tables in the database."""
    if not db_path.exists():
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables 