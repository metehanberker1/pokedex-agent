"""Tool functions exposed to the LLM."""
from __future__ import annotations

import json
import textwrap
from typing import Any, Dict, List

from .db import run_query


def run_query_tool(sql: str) -> List[Dict[str, Any]]:
    """JSON-serialisable wrapper used in the OpenAI function call."""
    try:
        return run_query(sql)
    except Exception as e:
        return [{"error": str(e)}]


def run_python_tool(code: str, _globals: dict | None = None) -> str:
    """Execute sandboxed Python code for advanced reasoning."""
    _globals = _globals or {}
    
    # Safe builtins for data processing
    safe_builtins = {
        "len": len, 
        "sorted": sorted, 
        "sum": sum, 
        "min": min, 
        "max": max,
        "round": round,
        "abs": abs,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "enumerate": enumerate,
        "zip": zip,
        "range": range,
        "filter": filter,
        "map": map,
        "any": any,
        "all": all,
        "reversed": reversed,
    }
    
    # Create a safe execution environment
    safe_globals = {
        "__builtins__": safe_builtins,
        "json": json,
        "math": __import__("math"),
        "statistics": __import__("statistics"),
        "collections": __import__("collections"),
        "itertools": __import__("itertools"),
    }
    safe_globals.update(_globals)
    
    try:
        # Execute the code in the safe environment
        exec(textwrap.dedent(code), safe_globals)
        
        # Return non-private variables as JSON
        result = {k: v for k, v in safe_globals.items() 
                 if not k.startswith("_") and k not in ["json", "math", "statistics", "collections", "itertools"]}
        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}) 