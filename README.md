# 🎮 Pokédex Conversational Agent

A self-contained chat agent that can answer any Pokémon-related question by reasoning over comprehensive data from PokéAPI. The agent uses a local SQLite database mirror of PokéAPI to eliminate rate limits and provide fast, reliable responses with the most extensive Pokémon knowledge base available.

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
# Run ETL to mirror PokéAPI data (takes ~5-10 minutes for comprehensive data)
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
│   ├── etl.py          # ETL: Comprehensive PokéAPI → SQLite
│   ├── db.py           # Database wrapper
│   ├── tools.py        # LLM tools (run_query, run_python)
│   ├── prompts.py      # System prompts
│   ├── agent.py        # ReAct loop with OpenAI
│   ├── cli.py          # CLI interface
│   ├── models_utility.py # Comprehensive PokéAPI data models
│   └── __init__.py
├── scripts/
│   └── refresh_data.py # Cron-friendly ETL runner
├── streamlit_app.py    # Web interface
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🔧 How It Works

### Data Flow
1. **Comprehensive ETL Process**: `etl.py` downloads and normalizes ALL PokéAPI endpoints into a local SQLite database
2. **Agent Loop**: The agent uses a ReAct-style loop with OpenAI function calling
3. **Tools**: Two main tools are exposed to the LLM:
   - `run_query(sql)`: Execute SQL SELECT queries on the local database
   - `run_python(code)`: Execute Python code for data analysis

### Complete Database Schema (Aligned with models_utility.py)

**CORE POKÉMON DATA:**
- **pokemon_species**: Complete species information (legendary status, habitat, growth rate, gender rates, etc.)
- **pokemon**: Individual Pokémon data (stats, experience, height, weight, order)
- **pokemon_types**: Type associations with slot information
- **pokemon_stats**: Base stats and effort values for each Pokémon
- **pokemon_abilities**: Abilities, hidden abilities, and slot information
- **pokemon_moves**: Complete move learnsets with methods, levels, version groups, and order
- **pokemon_held_items**: Items Pokémon can hold with rarity and version details
- **pokemon_form**: All forms including Mega, Gigantamax, regional variants with complete metadata

**MOVES AND ABILITIES:**
- **move**: Complete move data (power, accuracy, PP, priority, effects, targets)
- **ability**: All abilities with generation information
- **move_effects**: Detailed move descriptions and effects
- **ability_effects**: Ability descriptions and effects
- **move_category, move_damage_class, move_target, move_ailment, move_learn_method**: Move classification data

**ITEMS AND EQUIPMENT:**
- **item**: Complete item database (cost, fling power, effects, categories)
- **item_effects**: Detailed item descriptions and effects
- **item_category, item_attribute, item_pocket, item_fling_effect**: Item classification

**BERRIES:**
- **berry**: Complete berry database (growth time, harvest, firmness, flavors)
- **berry_firmness, berry_flavor**: Berry classification

**CONTEST AND COMPETITION:**
- **contest_type, contest_effect, super_contest_effect**: Contest system data

**EVOLUTION:**
- **evolution_chain, evolution_trigger**: Evolution system data

**GAMES AND VERSIONS:**
- **generation, version, version_group, pokedex**: Game version compatibility

**LOCATIONS AND ENCOUNTERS:**
- **location, location_area, region**: Complete location database
- **encounter_method, encounter_condition, encounter_condition_value**: Encounter mechanics

**STATS AND CHARACTERISTICS:**
- **stat**: All stat types with battle-only flags
- **characteristic**: Breeding characteristics and stat relationships

**POKÉMON CLASSIFICATION:**
- **egg_group, gender, pokemon_color, pokemon_shape**: Classification data

**NATURES AND TRAINING:**
- **nature**: Complete nature database with stat modifications
- **pokeathlon_stat, move_battle_style**: Training and battle mechanics

**MACHINES:**
- **machine**: TM/HM compatibility across versions

**LANGUAGES:**
- **language**: Multi-language support data

**TYPE RELATIONS:**
- **type, type_relations**: Complete type effectiveness chart

**FLAVOR TEXT:**
- **flavor_text**: Multi-language descriptions for all resources

## 💬 Example Queries

The agent can handle incredibly comprehensive Pokémon-related questions:

### Core Pokémon Analysis
- **Team Building**: "What's the best team of 6 Pokémon for competitive battling?"
- **Stat Analysis**: "Which Pokémon have the highest attack stat?"
- **Type Effectiveness**: "What types are super effective against Water types?"
- **Legendary Pokémon**: "Show me all legendary Pokémon from Generation 1"

### Advanced Battle Analysis
- **Move Coverage**: "What moves can Pikachu learn and at what levels?"
- **Ability Analysis**: "What are the effects of the ability Intimidate?"
- **Nature Optimization**: "What are the best natures for a competitive Garchomp?"
- **Type Coverage**: "Which Pokémon have the best type coverage for competitive teams?"

### Game Mechanics
- **Evolution Chains**: "What does Eevee evolve into and what are the requirements?"
- **Item Analysis**: "What items can Charizard hold and how rare are they?"
- **Location Data**: "Where can I find Pikachu in different games?"
- **Encounter Methods**: "What are the different ways to encounter Pokémon?"

### Breeding and Training
- **Egg Groups**: "Which Pokémon can breed with Pikachu?"
- **Characteristics**: "What are the breeding characteristics for high Attack IVs?"
- **Nature Breeding**: "How do I breed for a Jolly nature?"

### Contest and Competition
- **Contest Moves**: "What are the best contest moves for each category?"
- **Berry Farming**: "How long does it take to grow different berries?"
- **Super Contest**: "What are the appeal values for different contest effects?"

### Version-Specific Data
- **Machine Compatibility**: "Which Pokémon can learn Thunderbolt via TM?"
- **Version Exclusives**: "What Pokémon are exclusive to each version?"
- **Regional Variants**: "What are all the regional forms of Pokémon?"

## 🛠️ Development

### Refreshing Data

```bash
# Force refresh (overwrites existing database)
python scripts/refresh_data.py --force

# Regular refresh (skips if database exists)
python scripts/refresh_data.py
```

## 📊 Features

- **Comprehensive Database**: Complete PokéAPI mirror with 50+ endpoints and 100+ tables
- **Local Database**: No rate limits or API dependencies during chat
- **Rich CLI**: Beautiful terminal interface with syntax highlighting
- **Web Interface**: Streamlit-based web UI for easy access
- **SQL Transparency**: All queries are shown to the user
- **Python Integration**: Advanced data analysis with Python code execution
- **Multi-language Support**: Access to flavor text in multiple languages
- **Version Compatibility**: Complete game version and generation data
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

### ETL Takes Too Long
The comprehensive ETL process downloads data from 50+ PokéAPI endpoints. This is normal and only needs to be done once.

## 📈 Performance

- **Database Size**: ~200MB SQLite database (comprehensive data)
- **ETL Time**: ~5-10 minutes for initial comprehensive setup
- **Query Response**: <1 second for most queries
- **Memory Usage**: Minimal (uses SQLite)
- **Data Coverage**: 100% of PokéAPI endpoints

## 🎯 New Capabilities

With the comprehensive database, you can now ask about:

- **Complete Move Data**: Power, accuracy, PP, priority, effects, targets, learning methods
- **Full Item Database**: Cost, effects, categories, fling power, version compatibility
- **Berry Farming**: Growth times, harvest yields, firmness, flavors, contest effects
- **Evolution Mechanics**: Complete evolution chains, triggers, and requirements
- **Location Data**: All locations, areas, regions, and encounter methods
- **Nature Analysis**: Complete nature database with stat modifications
- **Machine Compatibility**: TM/HM compatibility across all versions
- **Multi-language Support**: Access to descriptions in multiple languages
- **Form Analysis**: Mega evolutions, Gigantamax, regional variants
- **Contest System**: Complete contest mechanics and effects
- **Breeding Data**: Egg groups, characteristics, gender ratios
- **Version Exclusives**: Complete version compatibility data

---

**Ready to become a Pokémon master with the most comprehensive Pokédex ever created? Start chatting with Pokédex-Pro! 🎯** 