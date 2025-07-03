import pytest
from src import prompts

def test_prompts_imports():
    """Test that prompts module can be imported."""
    assert prompts is not None

def test_base_system_exists():
    """Test that BASE_SYSTEM constant exists."""
    assert hasattr(prompts, 'BASE_SYSTEM')
    assert isinstance(prompts.BASE_SYSTEM, str)
    assert len(prompts.BASE_SYSTEM) > 0

def test_prompts_module_structure():
    """Test basic module structure."""
    # Just verify the module exists and can be imported
    assert hasattr(prompts, '__file__')

def test_base_system_content():
    """Test that BASE_SYSTEM contains expected content."""
    base_system = prompts.BASE_SYSTEM
    
    # Check for key sections
    assert "Pokédex-Pro" in base_system
    assert "SQL access" in base_system
    assert "run_query" in base_system
    assert "run_python" in base_system
    assert "DATABASE SCHEMA" in base_system
    assert "WORKFLOW" in base_system
    assert "COMPREHENSIVE CAPABILITIES" in base_system

def test_base_system_database_schema():
    """Test that BASE_SYSTEM contains database schema information."""
    base_system = prompts.BASE_SYSTEM
    
    # Check for core tables
    assert "pokemon_species" in base_system
    assert "pokemon" in base_system
    assert "pokemon_types" in base_system
    assert "pokemon_stats" in base_system
    assert "pokemon_abilities" in base_system
    assert "pokemon_moves" in base_system
    assert "move" in base_system
    assert "ability" in base_system
    assert "item" in base_system
    assert "berry" in base_system
    assert "evolution_chain" in base_system
    assert "location" in base_system
    assert "stat" in base_system
    assert "nature" in base_system

def test_base_system_relationships():
    """Test that BASE_SYSTEM contains relationship information."""
    base_system = prompts.BASE_SYSTEM
    
    # Check for relationship descriptions
    assert "IMPORTANT RELATIONSHIPS" in base_system
    assert "links to" in base_system
    assert "pokemon.species_id" in base_system
    assert "pokemon_types.pokemon_id" in base_system

def test_base_system_workflow():
    """Test that BASE_SYSTEM contains workflow instructions."""
    base_system = prompts.BASE_SYSTEM
    
    # Check for workflow steps
    assert "WORKFLOW" in base_system
    assert "Analyze the user's question" in base_system
    assert "Write appropriate SQL queries" in base_system
    assert "Call run_query()" in base_system
    assert "Use run_python()" in base_system
    assert "Provide a clear, concise answer" in base_system

def test_base_system_capabilities():
    """Test that BASE_SYSTEM contains comprehensive capabilities."""
    base_system = prompts.BASE_SYSTEM
    # Comprehensive coverage of all major capabilities mentioned in the system prompt
    present_capabilities = [
        "Team building",
        "Type effectiveness",
        "Stat analysis",
        "Evolution chains",
        "Ability analysis",
        "Legendary",
        "Item analysis",
        "Berry farming",
        "Nature analysis",
        "Machine/TM/HM",
        "Multi-language",
        "Regional variants",
        "Encounter methods",
        "Characteristic analysis",
        "Move learning",
        "Held item analysis",
        "Form analysis"
    ]
    for capability in present_capabilities:
        assert capability in base_system

def test_base_system_sql_instructions():
    """Test that BASE_SYSTEM contains SQL usage instructions."""
    base_system = prompts.BASE_SYSTEM
    
    # Check for SQL-related instructions
    assert "```sql```" in base_system
    assert "transparency" in base_system
    assert "SQL queries" in base_system

def test_base_system_tool_instructions():
    """Test that BASE_SYSTEM contains tool usage instructions."""
    base_system = prompts.BASE_SYSTEM
    
    # Check for tool usage instructions
    assert "run_query()" in base_system
    assert "run_python()" in base_system
    assert "function" in base_system

def test_base_system_step_by_step():
    """Test that BASE_SYSTEM mentions step-by-step thinking."""
    base_system = prompts.BASE_SYSTEM
    
    assert "step-by-step" in base_system
    assert "think" in base_system

def test_base_system_explanations():
    """Test that BASE_SYSTEM asks for explanations."""
    base_system = prompts.BASE_SYSTEM
    
    assert "explanations" in base_system
    assert "helpful" in base_system

def test_base_system_comprehensive_database():
    """Test that BASE_SYSTEM mentions comprehensive database."""
    base_system = prompts.BASE_SYSTEM
    
    assert "comprehensive" in base_system
    assert "PokéAPI" in base_system
    assert "most comprehensive" in base_system

def test_few_shot_examples_exist():
    """Test that FEW_SHOT_EXAMPLES constant exists."""
    assert hasattr(prompts, 'FEW_SHOT_EXAMPLES')
    assert isinstance(prompts.FEW_SHOT_EXAMPLES, list)
    assert len(prompts.FEW_SHOT_EXAMPLES) > 0

def test_few_shot_examples_structure():
    """Test that FEW_SHOT_EXAMPLES has correct structure."""
    examples = prompts.FEW_SHOT_EXAMPLES
    
    for example in examples:
        assert isinstance(example, dict)
        assert "user" in example
        assert "assistant" in example
        assert isinstance(example["user"], str)
        assert isinstance(example["assistant"], str)
        assert len(example["user"]) > 0
        assert len(example["assistant"]) > 0

def test_few_shot_examples_content():
    """Test that FEW_SHOT_EXAMPLES contain relevant content."""
    examples = prompts.FEW_SHOT_EXAMPLES
    
    # Check that examples cover different types of queries
    user_questions = [ex["user"] for ex in examples]
    
    # Should have team building example
    team_questions = [q for q in user_questions if "team" in q.lower()]
    assert len(team_questions) > 0
    
    # Should have stat analysis example
    stat_questions = [q for q in user_questions if "stat" in q.lower()]
    assert len(stat_questions) > 0
    
    # Should have type effectiveness example
    type_questions = [q for q in user_questions if "type" in q.lower()]
    assert len(type_questions) > 0
    
    # Should have move learning example
    move_questions = [q for q in user_questions if "move" in q.lower()]
    assert len(move_questions) > 0

def test_few_shot_examples_sql_usage():
    """Test that FEW_SHOT_EXAMPLES show SQL usage."""
    examples = prompts.FEW_SHOT_EXAMPLES
    
    # Check that examples show SQL queries
    sql_examples = [ex for ex in examples if "```sql" in ex["assistant"]]
    assert len(sql_examples) > 0

def test_few_shot_examples_explanation():
    """Test that FEW_SHOT_EXAMPLES include explanations."""
    examples = prompts.FEW_SHOT_EXAMPLES
    
    # Check that examples include explanations
    explained_examples = [ex for ex in examples if "useful" in ex["assistant"].lower() or "helpful" in ex["assistant"].lower()]
    assert len(explained_examples) > 0

def test_few_shot_examples_variety():
    """Test that FEW_SHOT_EXAMPLES cover a variety of scenarios."""
    examples = prompts.FEW_SHOT_EXAMPLES
    
    # Should have multiple examples
    assert len(examples) >= 5
    
    # Check for different types of queries
    user_questions = [ex["user"].lower() for ex in examples]
    
    # Team building
    assert any("team" in q for q in user_questions)
    
    # Stats
    assert any("stat" in q for q in user_questions)
    
    # Types
    assert any("type" in q for q in user_questions)
    
    # Moves
    assert any("move" in q for q in user_questions)
    
    # Items
    assert any("item" in q for q in user_questions)
    
    # Natures
    assert any("nature" in q for q in user_questions)
    
    # Forms
    assert any("mega" in q for q in user_questions)
    
    # Costs
    assert any("expensive" in q for q in user_questions)
    
    # Learning
    assert any("learn" in q for q in user_questions)

def test_base_system_length():
    """Test that BASE_SYSTEM has sufficient length for comprehensive instructions."""
    base_system = prompts.BASE_SYSTEM
    
    # Should be substantial in length
    assert len(base_system) > 1000

def test_base_system_formatting():
    """Test that BASE_SYSTEM has proper formatting."""
    base_system = prompts.BASE_SYSTEM
    
    # Should have proper line breaks
    assert "\n" in base_system
    
    # Should have proper sections
    assert ":" in base_system

def test_base_system_no_placeholders():
    """Test that BASE_SYSTEM doesn't contain placeholder text."""
    base_system = prompts.BASE_SYSTEM
    
    # Should not contain placeholder indicators
    assert "TODO" not in base_system
    assert "FIXME" not in base_system
    assert "XXX" not in base_system
    assert "PLACEHOLDER" not in base_system

def test_base_system_consistent_terminology():
    """Test that BASE_SYSTEM uses consistent terminology."""
    base_system = prompts.BASE_SYSTEM
    
    # Should use consistent terms
    assert "Pokédex-Pro" in base_system
    assert "PokéAPI" in base_system
    assert "SQL" in base_system
    assert "Python" in base_system

def test_base_system_clear_instructions():
    """Test that BASE_SYSTEM provides clear instructions."""
    base_system = prompts.BASE_SYSTEM
    
    # Should have clear action words
    assert "Execute" in base_system or "execute" in base_system
    assert "Analyze" in base_system or "analyze" in base_system
    assert "Provide" in base_system or "provide" in base_system

def test_few_shot_examples_realistic():
    """Test that FEW_SHOT_EXAMPLES contain realistic queries."""
    examples = prompts.FEW_SHOT_EXAMPLES
    for example in examples:
        user_question = example["user"]
        assistant_response = example["assistant"]
        # User questions should be realistic
        assert len(user_question) > 10
        # Assistant responses should be helpful
        assert len(assistant_response) > 20
        assert "I'll" in assistant_response or "Let me" in assistant_response

def test_prompts_module_docstring():
    """Test that prompts module has a docstring."""
    assert prompts.__doc__ is not None
    assert len(prompts.__doc__) > 0

def test_base_system_docstring():
    """Test that BASE_SYSTEM has proper documentation."""
    # Check that it's properly defined as a string
    assert isinstance(prompts.BASE_SYSTEM, str)
    
    # Check that it starts with a description
    assert prompts.BASE_SYSTEM.strip().startswith("You are")

def test_few_shot_examples_documentation():
    """Test that FEW_SHOT_EXAMPLES are properly documented."""
    examples = prompts.FEW_SHOT_EXAMPLES
    
    # Check that examples are well-structured
    for i, example in enumerate(examples):
        assert "user" in example, f"Example {i} missing 'user' key"
        assert "assistant" in example, f"Example {i} missing 'assistant' key"
        assert example["user"], f"Example {i} has empty user question"
        assert example["assistant"], f"Example {i} has empty assistant response"

def test_prompts_module_imports():
    """Test that prompts module can be imported without errors."""
    # Test that all expected attributes are available
    assert hasattr(prompts, 'BASE_SYSTEM')
    assert hasattr(prompts, 'FEW_SHOT_EXAMPLES')
    assert hasattr(prompts, '__file__')
    assert hasattr(prompts, '__name__')

def test_base_system_unicode_support():
    """Test that BASE_SYSTEM supports Unicode characters."""
    base_system = prompts.BASE_SYSTEM
    
    # Should handle special characters properly
    assert "Pokédex" in base_system
    assert "Pokémon" in base_system

def test_few_shot_examples_unicode_support():
    """Test that FEW_SHOT_EXAMPLES support Unicode characters."""
    examples = prompts.FEW_SHOT_EXAMPLES
    
    for example in examples:
        # Should handle special characters in questions and responses
        user_question = example["user"]
        assistant_response = example["assistant"]
        
        # Check that strings are properly encoded
        assert isinstance(user_question, str)
        assert isinstance(assistant_response, str) 