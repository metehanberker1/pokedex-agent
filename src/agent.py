"""Main agent module with ReAct-style loop and OpenAI function calling."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from openai import OpenAI
from dotenv import load_dotenv
from loguru import logger

from .tools import run_python_tool, run_query_tool
from .prompts import BASE_SYSTEM

load_dotenv()  # loads OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_query",
            "description": "Execute a read-only SQL SELECT on the Pokémon database to retrieve data.",
            "parameters": {
                "type": "object",
                "properties": {"sql": {"type": "string", "description": "SQL SELECT query to execute"}},
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "Execute Python code for data analysis, calculations, or post-processing of query results.",
            "parameters": {
                "type": "object",
                "properties": {"code": {"type": "string", "description": "Python code to execute"}},
                "required": ["code"],
            },
        },
    },
]

TOOL_MAP = {"run_query": run_query_tool, "run_python": run_python_tool}


def chat(messages: List[Dict[str, str]], max_iterations: int = 10) -> str:
    """Single-turn chat: feed messages, iterate function calls until finish."""
    iteration = 0
    
    while iteration < max_iterations:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.1,
            )
            
            response_message = response.choices[0].message

            if response_message.tool_calls:
                # Add the assistant's message with tool calls first
                messages.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                        for tool_call in response_message.tool_calls
                    ]
                })
                
                # Then add tool responses
                for tool_call in response_message.tool_calls:
                    fn_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    logger.info(f"🔧 {fn_name}({args})")
                    
                    try:
                        result = TOOL_MAP[fn_name](**args)
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(result, default=str),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Tool execution failed: {e}")
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({"error": str(e)}),
                            }
                        )
                
                iteration += 1
                continue  # next loop → LLM sees result
            else:
                return response_message.content
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Sorry, I encountered an error: {e}"
    
    return "I reached the maximum number of iterations. Please try rephrasing your question."


def create_chat_session() -> List[Dict[str, str]]:
    """Create a new chat session with the system prompt."""
    return [{"role": "system", "content": BASE_SYSTEM}]


def add_user_message(messages: List[Dict[str, str]], content: str) -> None:
    """Add a user message to the conversation."""
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages: List[Dict[str, str]], content: str) -> None:
    """Add an assistant message to the conversation."""
    messages.append({"role": "assistant", "content": content}) 