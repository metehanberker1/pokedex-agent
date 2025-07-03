import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import pytest
from src import db
from unittest.mock import Mock
import contextlib
import sqlite3

@pytest.fixture(scope="session")
def mini_db(tmp_path_factory):
    """Create a minimal test database without running ETL."""
    path: Path = tmp_path_factory.mktemp("data") / "mini.db"
    
    # Create a minimal database with just the schema
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    # Create minimal tables for tests
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_species (
            id INTEGER PRIMARY KEY,
            name TEXT,
            base_happiness INTEGER,
            capture_rate INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT,
            height INTEGER,
            weight INTEGER
        )
    """)
    
    # Insert minimal test data
    cursor.execute("INSERT OR IGNORE INTO pokemon_species (id, name) VALUES (1, 'bulbasaur')")
    cursor.execute("INSERT OR IGNORE INTO pokemon (id, name) VALUES (1, 'bulbasaur')")
    
    conn.commit()
    conn.close()
    return path

@pytest.fixture(autouse=True)
def _patch_db(monkeypatch, mini_db):
    """Force src.db to use the test database."""
    monkeypatch.setattr(db, "DB_PATH", mini_db)

@pytest.fixture
def scripted_llm(monkeypatch):
    """
    Usage:
        with scripted_llm([msg1, msg2, ...]):
            ...call agent.chat()...
    """
    @contextlib.contextmanager
    def factory(sequence):
        def fake_create(*_, **__):
            response_data = sequence.pop(0)
            
            # Create a mock response that matches the OpenAI API structure
            mock_response = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            
            # Handle different response types
            if "tool_calls" in response_data:
                # Tool call response
                mock_message.tool_calls = []
                for tool_call_data in response_data["tool_calls"]:
                    mock_tool_call = Mock()
                    mock_tool_call.id = tool_call_data.get("id", "call_123")
                    mock_tool_call.function.name = tool_call_data["function"]["name"]
                    mock_tool_call.function.arguments = tool_call_data["function"]["arguments"]
                    mock_message.tool_calls.append(mock_tool_call)
                mock_message.content = response_data.get("content", "")
            else:
                # Regular response
                mock_message.tool_calls = None
                mock_message.content = response_data.get("content", "")
            
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            return mock_response
            
        # Fix the import path - patch the client instance in the agent module
        monkeypatch.setattr("src.agent.client.chat.completions.create", fake_create)
        yield
    return factory 