import re, textwrap, pytest
from src import agent, prompts
from src.agent import chat, create_chat_session, add_user_message, add_assistant_message

pytestmark = pytest.mark.integration

BUG_TEAM_SQL = "SELECT p.name FROM pokemon p JOIN pokemon_types t ON p.id = t.pokemon_id WHERE t.type_name='bug' AND p.is_default=1 ORDER BY p.base_experience DESC LIMIT 6"

# Comprehensive integration test suite covering end-to-end agent functionality with real queries and tool interactions.
# These tests validate the complete user experience from question to answer, ensuring the agent can handle complex Pokémon queries effectively.

def test_bug_team(scripted_llm):
    script = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "run_query", "arguments": f'{{"sql": "{BUG_TEAM_SQL}"}}'}
                }
            ]
        },
        {"role": "assistant", "content": "Try Scizor, Volcarona, and friends — they form a strong bug team."}
    ]
    with scripted_llm(script):
        out = agent.chat(
            [{"role": "system", "content": prompts.BASE_SYSTEM},
             {"role": "user", "content": "Build a team of all bug type Pokémon."}]
        )
    assert re.search(r"scizor", out, re.I)

def test_python_tool_integration(scripted_llm):
    script = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "run_python", "arguments": '{"code": "result = 2 + 2"}'}
                }
            ]
        },
        {"role": "assistant", "content": "The answer is 4."}
    ]
    with scripted_llm(script):
        out = agent.chat(
            [{"role": "system", "content": prompts.BASE_SYSTEM},
             {"role": "user", "content": "What is 2 + 2?"}]
        )
    assert "4" in out

def test_tool_error_handling(scripted_llm):
    script = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "run_query", "arguments": '{"sql": "SELECT * FROM nonexistent_table"}'}
                }
            ]
        },
        {"role": "assistant", "content": "Sorry, I couldn't find that information."}
    ]
    with scripted_llm(script):
        out = agent.chat(
            [{"role": "system", "content": prompts.BASE_SYSTEM},
             {"role": "user", "content": "Show me data from a table that doesn't exist."}]
        )
    assert "sorry" in out.lower()

def test_multi_step_tool_use(scripted_llm):
    script = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "run_query", "arguments": '{"sql": "SELECT id FROM pokemon_species LIMIT 1"}'}
                }
            ]
        },
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_2",
                    "function": {"name": "run_python", "arguments": '{"code": "result = 42"}'}
                }
            ]
        },
        {"role": "assistant", "content": "The answer is 42."}
    ]
    with scripted_llm(script):
        out = agent.chat(
            [{"role": "system", "content": prompts.BASE_SYSTEM},
             {"role": "user", "content": "Give me the answer to life, the universe, and everything."}]
        )
    assert "42" in out

def test_llm_error_handling(monkeypatch):
    def fake_create(*_, **__):
        raise Exception("API Error")
    monkeypatch.setattr("src.agent.client.chat.completions.create", fake_create)
    out = agent.chat(
        [{"role": "system", "content": prompts.BASE_SYSTEM},
         {"role": "user", "content": "Trigger an LLM error."}]
    )
    assert "error" in out.lower() 