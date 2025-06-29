"""ETL: mirror core PokéAPI resources into a local SQLite/DuckDB db."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

import requests
from loguru import logger
from tqdm import tqdm

BASE_URL = "https://pokeapi.co/api/v2"
TABLES = {
    "pokemon_species": "/pokemon-species?limit=100000&offset=0",
    "pokemon": "/pokemon?limit=100000&offset=0",
    "type": "/type?limit=1000&offset=0",
    "pokemon_habitat": "/pokemon-habitat?limit=1000&offset=0",
    "growth_rate": "/growth-rate?limit=1000&offset=0",
}
DB_PATH = Path(__file__).parent / "pokedex.db"


def _paginate(url: str) -> Iterable[dict]:
    """Paginate through API results."""
    while url:
        try:
            page = requests.get(url, timeout=30).json()
            yield from page["results"]
            url = page["next"]
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            break


def load_all(force: bool = False, db_path: Path = DB_PATH) -> None:
    """Load all PokéAPI data into local SQLite database."""
    if db_path.exists() and not force:
        logger.info("DB already exists – skip ETL")
        return

    logger.info(f"Starting ETL to {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table schemas
    cur.executescript(
        """
    CREATE TABLE IF NOT EXISTS pokemon_species (
        id INTEGER PRIMARY KEY, 
        name TEXT,
        generation_id INTEGER, 
        habitat TEXT, 
        growth_rate TEXT,
        is_legendary INT, 
        is_mythical INT, 
        capture_rate INT,
        base_happiness INT,
        color TEXT,
        shape TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY, 
        name TEXT,
        species_id INTEGER, 
        base_experience INT, 
        is_default INT,
        height INTEGER,
        weight INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_types (
        pokemon_id INT, 
        type_name TEXT,
        slot INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_stats (
        pokemon_id INT,
        stat_name TEXT,
        base_stat INTEGER,
        effort INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS type (
        id INTEGER PRIMARY KEY, 
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_abilities (
        pokemon_id INT,
        ability_name TEXT,
        is_hidden INT,
        slot INTEGER
    );
    """
    )

    # Clear existing data
    cur.executescript(
        """
    DELETE FROM pokemon_abilities;
    DELETE FROM pokemon_stats;
    DELETE FROM pokemon_types;
    DELETE FROM pokemon;
    DELETE FROM pokemon_species;
    DELETE FROM type;
    """
    )

    # Load species
    logger.info("Loading species")
    for obj in tqdm(_paginate(BASE_URL + TABLES["pokemon_species"]), desc="Species"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                """INSERT INTO pokemon_species
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    data["id"],
                    data["name"],
                    data["generation"]["url"].split("/")[-2],
                    data["habitat"]["name"] if data["habitat"] else None,
                    data["growth_rate"]["name"],
                    int(data["is_legendary"]),
                    int(data["is_mythical"]),
                    data["capture_rate"],
                    data["base_happiness"],
                    data["color"]["name"],
                    data["shape"]["name"] if data["shape"] else None,
                ),
            )
        except Exception as e:
            logger.warning(f"Error loading species {obj['name']}: {e}")

    # Load pokemon + types + stats + abilities
    logger.info("Loading pokemon details")
    for obj in tqdm(_paginate(BASE_URL + TABLES["pokemon"]), desc="Pokemon"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            
            # Insert pokemon
            cur.execute(
                """INSERT INTO pokemon VALUES(?,?,?,?,?,?,?)""",
                (
                    data["id"],
                    data["name"],
                    data["species"]["url"].split("/")[-2],
                    data["base_experience"],
                    int(data["is_default"]),
                    data["height"],
                    data["weight"],
                ),
            )
            
            # Insert types
            for t in data["types"]:
                cur.execute(
                    "INSERT INTO pokemon_types VALUES (?,?,?)",
                    (data["id"], t["type"]["name"], t["slot"]),
                )
            
            # Insert stats
            for s in data["stats"]:
                cur.execute(
                    "INSERT INTO pokemon_stats VALUES (?,?,?,?)",
                    (data["id"], s["stat"]["name"], s["base_stat"], s["effort"]),
                )
            
            # Insert abilities
            for a in data["abilities"]:
                cur.execute(
                    "INSERT INTO pokemon_abilities VALUES (?,?,?,?)",
                    (data["id"], a["ability"]["name"], int(a["is_hidden"]), a["slot"]),
                )
                
        except Exception as e:
            logger.warning(f"Error loading pokemon {obj['name']}: {e}")

    # Load type lookup table
    logger.info("Loading types")
    for obj in tqdm(_paginate(BASE_URL + TABLES["type"]), desc="Types"):
        try:
            cur.execute(
                "INSERT INTO type VALUES(?,?)",
                (int(obj["url"].split("/")[-2]), obj["name"]),
            )
        except Exception as e:
            logger.warning(f"Error loading type {obj['name']}: {e}")

    conn.commit()
    conn.close()
    logger.success("ETL complete → %s", db_path) 