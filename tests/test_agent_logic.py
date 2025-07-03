from src import agent
from unittest.mock import Mock, patch
import pytest
import json

# Comprehensive test suite covering all aspects of the agent's ReAct loop, tool execution, error handling, and edge cases.
# These tests ensure the agent can handle various scenarios including tool calls, API errors, message formats, and iteration limits.

def test_agent_returns_final_response(scripted_llm):
    """Test that agent returns the final response after tool calls."""
    script = [
        {
            "role": "assistant", 
            "tool_calls": [{
                "id": "call_123",
                "function": {"name": "run_query", "arguments": '{"sql":"SELECT 1"}'}
            }]
        },
        {"role": "assistant", "content": "Done!"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert answer == "Done!"

def test_agent_handles_tool_execution_error(scripted_llm):
    """Test that agent handles tool execution errors gracefully."""
    script = [
        {
            "role": "assistant", 
            "tool_calls": [{
                "id": "call_123",
                "function": {"name": "invalid_tool", "arguments": '{"sql":"SELECT 1"}'}
            }]
        },
        {"role": "assistant", "content": "Error handled!"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert "Error handled!" in answer

def test_agent_handles_openai_api_error(scripted_llm):
    """Test that agent handles OpenAI API errors gracefully."""
    def fake_create(*_, **__):
        raise Exception("API Error")
    
    with patch("src.agent.client.chat.completions.create", side_effect=fake_create):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert "Sorry, I encountered an error" in answer

def test_agent_max_iterations_reached(scripted_llm):
    """Test that agent stops after max iterations."""
    # Create a script that always returns tool calls to trigger max iterations
    script = [
        {
            "role": "assistant", 
            "tool_calls": [{
                "id": "call_123",
                "function": {"name": "run_query", "arguments": '{"sql":"SELECT 1"}'}
            }]
        }
    ] * 15  # More than max_iterations (10)
    
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ], max_iterations=2)
    assert "maximum number of iterations" in answer

def test_create_chat_session():
    """Test creating a new chat session."""
    session = agent.create_chat_session()
    assert len(session) == 1
    assert session[0]["role"] == "system"
    assert "content" in session[0]

def test_add_user_message():
    """Test adding a user message to conversation."""
    messages = [{"role": "system", "content": "Hello"}]
    agent.add_user_message(messages, "How are you?")
    assert len(messages) == 2
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "How are you?"

def test_add_assistant_message():
    """Test adding an assistant message to conversation."""
    messages = [{"role": "system", "content": "Hello"}]
    agent.add_assistant_message(messages, "I'm doing well!")
    assert len(messages) == 2
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "I'm doing well!"

def test_agent_handles_multiple_tool_calls(scripted_llm):
    """Test that agent handles multiple tool calls in one response."""
    script = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "run_query", "arguments": '{"sql":"SELECT 1"}'}
                },
                {
                    "id": "call_2", 
                    "function": {"name": "run_python", "arguments": '{"code":"result = 42"}'}
                }
            ]
        },
        {"role": "assistant", "content": "Multiple tools executed!"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert "Multiple tools executed!" in answer

def test_agent_handles_empty_tool_calls(scripted_llm):
    """Test that agent handles empty tool_calls list."""
    script = [
        {
            "role": "assistant",
            "tool_calls": []
        },
        {"role": "assistant", "content": "No tools needed!"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert "Sorry, I encountered an error" in answer or answer == ""

def test_agent_handles_none_tool_calls(scripted_llm):
    """Test that agent handles None tool_calls."""
    script = [
        {
            "role": "assistant",
            "tool_calls": None
        },
        {"role": "assistant", "content": "Direct response!"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert "Sorry, I encountered an error" in answer

def test_agent_handles_json_parsing_error(scripted_llm):
    """Test that agent handles JSON parsing errors in tool arguments."""
    script = [
        {
            "role": "assistant",
            "tool_calls": [{
                "id": "call_123",
                "function": {"name": "run_query", "arguments": 'invalid json'}
            }]
        },
        {"role": "assistant", "content": "JSON error handled!"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert "Sorry, I encountered an error" in answer

def test_agent_handles_missing_tool_arguments(scripted_llm):
    """Test that agent handles missing tool arguments."""
    script = [
        {
            "role": "assistant",
            "tool_calls": [{
                "id": "call_123",
                "function": {"name": "run_query"}
            }]
        },
        {"role": "assistant", "content": "Missing args handled!"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ])
    assert "Sorry, I encountered an error" in answer

def test_agent_handles_empty_messages():
    """Test that agent handles empty message list."""
    answer = agent.chat([])
    assert "Sorry, I encountered an error" in answer

def test_agent_handles_none_messages():
    """Test that agent handles None messages."""
    answer = agent.chat(None)
    assert "Sorry, I encountered an error" in answer

def test_agent_handles_invalid_message_format(scripted_llm):
    """Test that agent handles invalid message format."""
    script = [
        {"role": "assistant", "content": "Valid response"}
    ]
    with scripted_llm(script):
        answer = agent.chat([
            {"invalid": "format"},
            {"role": "user", "content": "hi"}
        ])
    assert "Valid response" in answer

def test_agent_handles_zero_iterations():
    """Test that agent handles zero max_iterations."""
    answer = agent.chat([
        {"role": "system", "content": "x"},
        {"role": "user", "content": "hi"}
    ], max_iterations=0)
    assert "maximum number of iterations" in answer

def test_agent_handles_negative_iterations():
    """Test that agent handles negative max_iterations."""
    answer = agent.chat([
        {"role": "system", "content": "x"},
        {"role": "user", "content": "hi"}
    ], max_iterations=-1)
    assert "maximum number of iterations" in answer

def test_agent_handles_large_iterations(scripted_llm):
    """Test that agent handles very large max_iterations."""
    script = [
        {
            "role": "assistant",
            "tool_calls": [{
                "id": "call_123",
                "function": {"name": "run_query", "arguments": '{"sql":"SELECT 1"}'}
            }]
        }
    ] * 5
    with scripted_llm(script):
        answer = agent.chat([
            {"role": "system", "content": "x"},
            {"role": "user", "content": "hi"}
        ], max_iterations=100)
    assert "Sorry, I encountered an error" in answer or "Done!" in answer or "maximum number of iterations" in answer

def test_agent_tool_map_structure():
    """Test that TOOL_MAP has expected structure."""
    assert "run_query" in agent.TOOL_MAP
    assert "run_python" in agent.TOOL_MAP
    assert callable(agent.TOOL_MAP["run_query"])
    assert callable(agent.TOOL_MAP["run_python"])

def test_agent_tools_structure():
    """Test that TOOLS list has expected structure."""
    assert len(agent.TOOLS) == 2
    for tool in agent.TOOLS:
        assert "type" in tool
        assert "function" in tool
        assert "name" in tool["function"]
        assert "description" in tool["function"]
        assert "parameters" in tool["function"]

def test_agent_client_initialization():
    """Test that OpenAI client is properly initialized."""
    assert hasattr(agent, 'client')
    assert agent.client is not None 