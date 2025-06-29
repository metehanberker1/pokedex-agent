# 🎮 Pokédex Conversational Agent

A self-contained chat agent that can answer any Pokémon-related question by reasoning over data from PokéAPI. The agent uses a local SQLite database mirror of PokéAPI to eliminate rate limits and provide fast, reliable responses.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd pokedex-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file in the project root and put your OPEN_API_KEY.

### 3. Build Local Database

```bash
# Run ETL to mirror PokéAPI data (takes ~2-3 minutes)
python -m src.etl

# Or use the refresh script
python scripts/refresh_data.py
```

### 4. Start Chatting

```bash
# Start the interactive CLI
python -m src.cli

# Or run the web interface
streamlit run streamlit_app.py
```

## 🏗️ Architecture

```
Pokédex-Agent
├── src/                 # Main package
│   ├── etl.py          # ETL: PokéAPI → SQLite
│   ├── db.py           # Database wrapper
│   ├── tools.py        # LLM tools (run_query, run_python)
│   ├── prompts.py      # System prompts
│   ├── agent.py        # ReAct loop with OpenAI
│   ├── cli.py          # CLI interface
│   └── __init__.py
├── scripts/
│   └── refresh_data.py # Cron-friendly ETL runner
├── streamlit_app.py    # Web interface
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🔧 How It Works

### Data Flow
1. **ETL Process**: `etl.py` downloads and normalizes PokéAPI data into a local SQLite database
2. **Agent Loop**: The agent uses a ReAct-style loop with OpenAI function calling
3. **Tools**: Two main tools are exposed to the LLM:
   - `run_query(sql)`: Execute SQL SELECT queries on the local database
   - `run_python(code)`: Execute Python code for data analysis

### Database Schema
- **pokemon_species**: Basic species information (legendary status, habitat, etc.)
- **pokemon**: Individual Pokémon data (stats, experience, etc.)
- **pokemon_types**: Type associations
- **pokemon_stats**: Base stats for each Pokémon
- **pokemon_abilities**: Abilities and hidden abilities
- **type**: Type lookup table

## 💬 Example Queries

The agent can handle a wide variety of Pokémon-related questions:

- **Team Building**: "What's the best team of 6 Pokémon for competitive battling?"
- **Stat Analysis**: "Which Pokémon have the highest attack stat?"
- **Type Effectiveness**: "What types are super effective against Water types?"
- **Legendary Pokémon**: "Show me all legendary Pokémon from Generation 1"
- **Habitat Information**: "Where can I find Pikachu?"
- **Evolution Chains**: "What does Eevee evolve into?"

## 🛠️ Development

### Refreshing Data

```bash
# Force refresh (overwrites existing database)
python scripts/refresh_data.py --force

# Regular refresh (skips if database exists)
python scripts/refresh_data.py
```

## 📊 Features

- **Local Database**: No rate limits or API dependencies during chat
- **Rich CLI**: Beautiful terminal interface with syntax highlighting
- **Web Interface**: Streamlit-based web UI for easy access
- **SQL Transparency**: All queries are shown to the user
- **Python Integration**: Advanced data analysis with Python code execution
- **Comprehensive Data**: Full PokéAPI mirror with stats, types, abilities, and more
- **Error Handling**: Robust error handling and user-friendly messages

## 🔒 Security

- **Read-only SQL**: Only SELECT statements are permitted
- **Sandboxed Python**: Limited builtins and modules for safe code execution
- **No File System Access**: Python execution environment is restricted

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🐛 Troubleshooting

### Database Not Found
If you see "Database not found" error:
```bash
python -m src.etl
```

### OpenAI API Errors
Make sure your `.env` file contains a valid `OPENAI_API_KEY`.

### Import Errors
Ensure you're in the correct directory and have activated your virtual environment.

## 📈 Performance

- **Database Size**: ~40MB SQLite database
- **ETL Time**: ~2-3 minutes for initial setup
- **Query Response**: <1 second for most queries
- **Memory Usage**: Minimal (uses SQLite)

---

**Ready to become a Pokémon master? Start chatting with Pokédex-Pro! 🎯** 