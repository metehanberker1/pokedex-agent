"""CLI interface for the Pokédex agent."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax

from .agent import chat, create_chat_session, add_user_message, add_assistant_message
from .db import DB_PATH
from .prompts import BASE_SYSTEM

console = Console()


def print_welcome() -> None:
    """Print the welcome message."""
    welcome_text = """
# 🎮 Pokédex Conversational Agent

Welcome to Pokédex-Pro! I'm your advanced Pokémon research assistant with access to comprehensive data from PokéAPI.

## What I can help you with:
- **Team Building**: Create competitive teams with type coverage
- **Stat Analysis**: Find Pokémon with the best stats
- **Type Effectiveness**: Understand type matchups and weaknesses
- **Habitat Information**: Learn where to find specific Pokémon
- **Evolution Chains**: Discover evolution requirements
- **Ability Analysis**: Compare abilities and hidden abilities
- **Legendary Pokémon**: Information about legendary and mythical Pokémon

Just ask me anything Pokémon-related!
    """
    
    console.print(Panel(Markdown(welcome_text), title="🎯 Ready to help!", border_style="green"))


def print_help() -> None:
    """Print help information."""
    help_text = """
## Available Commands:
- Type your question and press Enter
- `/help` - Show this help message
- `/quit` or `/exit` - Exit the application
- `/clear` - Clear the conversation history
- `/schema` - Show database schema information

## Example Questions:
- "What's the best team of 6 Pokémon for competitive battling?"
- "Which Pokémon have the highest attack stat?"
- "What types are super effective against Water types?"
- "Show me all legendary Pokémon from Generation 1"
- "Find Pokémon with high speed and special attack stats"
    """
    
    console.print(Panel(Markdown(help_text), title="📖 Help", border_style="blue"))


def print_schema() -> None:
    """Print database schema information."""
    if not DB_PATH.exists():
        console.print("[red]Database not found. Please run the ETL first.[/red]")
        return
    
    try:
        from .db import list_tables, get_table_info
        
        tables = list_tables()
        schema_text = "## Database Schema\n\n"
        
        for table in tables:
            schema_text += f"### {table}\n"
            try:
                columns = get_table_info(table)
                for col in columns:
                    schema_text += f"- `{col['name']}` ({col['type']})\n"
                schema_text += "\n"
            except Exception as e:
                schema_text += f"Error getting schema: {e}\n\n"
        
        console.print(Panel(Markdown(schema_text), title="🗄️ Database Schema", border_style="yellow"))
    except Exception as e:
        console.print(f"[red]Error displaying schema: {e}[/red]")


def main() -> None:
    """Main CLI entry point."""
    # Check if database exists
    if not DB_PATH.exists():
        console.print("[red]Database not found![/red]")
        console.print("Please run the ETL first:")
        console.print("  python -m src.etl")
        console.print("  or")
        console.print("  python scripts/refresh_data.py")
        sys.exit(1)
    
    print_welcome()
    
    messages = create_chat_session()
    
    try:
        while True:
            # Get user input
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            # Handle special commands
            if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                console.print("\n[green]Thanks for using Pokédex-Pro! Goodbye! 👋[/green]")
                break
            elif user_input.lower() == '/help':
                print_help()
                continue
            elif user_input.lower() == '/clear':
                messages = create_chat_session()
                console.print("[green]Conversation history cleared![/green]")
                continue
            elif user_input.lower() == '/schema':
                print_schema()
                continue
            elif user_input.strip() == '':
                continue
            
            # Add user message to conversation
            add_user_message(messages, user_input)
            
            # Get response from agent
            console.print("\n[bold yellow]Assistant[/bold yellow]")
            with console.status("[bold green]Thinking..."):
                response = chat(messages)
            
            # Add assistant response to conversation
            add_assistant_message(messages, response)
            
            # Display response with syntax highlighting
            if "```sql" in response:
                # Split response to handle SQL blocks
                parts = response.split("```sql")
                for i, part in enumerate(parts):
                    if i == 0:
                        console.print(part)
                    else:
                        if "```" in part:
                            sql_part, rest = part.split("```", 1)
                            console.print(Syntax(sql_part.strip(), "sql", theme="monokai"))
                            console.print(rest)
                        else:
                            console.print(Syntax(part.strip(), "sql", theme="monokai"))
            else:
                console.print(response)
                
    except (EOFError, KeyboardInterrupt):
        console.print("\n[green]Thanks for using Pokédex-Pro! Goodbye! 👋[/green]")


if __name__ == "__main__":
    main() 