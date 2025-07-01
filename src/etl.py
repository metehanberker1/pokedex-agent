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

# Complete TABLES configuration aligned with models_utility.py
TABLES = {
    # Core Pokémon data
    "pokemon_species": "/pokemon-species?limit=100000&offset=0",
    "pokemon": "/pokemon?limit=100000&offset=0",
    "type": "/type?limit=1000&offset=0",
    "pokemon_habitat": "/pokemon-habitat?limit=1000&offset=0",
    "growth_rate": "/growth-rate?limit=1000&offset=0",
    "pokemon_form": "/pokemon-form?limit=10000&offset=0",
    "pokemon_color": "/pokemon-color?limit=100&offset=0",
    "pokemon_shape": "/pokemon-shape?limit=100&offset=0",
    
    # Moves and Abilities
    "move": "/move?limit=10000&offset=0",
    "ability": "/ability?limit=1000&offset=0",
    "move-category": "/move-category?limit=100&offset=0",
    "move-damage-class": "/move-damage-class?limit=100&offset=0",
    "move-target": "/move-target?limit=100&offset=0",
    "move-ailment": "/move-ailment?limit=100&offset=0",
    "move-learn-method": "/move-learn-method?limit=100&offset=0",
    "move-battle-style": "/move-battle-style?limit=100&offset=0",
    
    # Items and Equipment
    "item": "/item?limit=10000&offset=0",
    "item-category": "/item-category?limit=100&offset=0",
    "item-attribute": "/item-attribute?limit=100&offset=0",
    "item-pocket": "/item-pocket?limit=100&offset=0",
    "item-fling-effect": "/item-fling-effect?limit=100&offset=0",
    
    # Berries
    "berry": "/berry?limit=1000&offset=0",
    "berry-firmness": "/berry-firmness?limit=100&offset=0",
    "berry-flavor": "/berry-flavor?limit=100&offset=0",
    
    # Contest and Competition
    "contest-type": "/contest-type?limit=100&offset=0",
    "contest-effect": "/contest-effect?limit=100&offset=0",
    "super-contest-effect": "/super-contest-effect?limit=100&offset=0",
    
    # Evolution
    "evolution-chain": "/evolution-chain?limit=1000&offset=0",
    "evolution-trigger": "/evolution-trigger?limit=100&offset=0",
    
    # Games and Versions
    "generation": "/generation?limit=100&offset=0",
    "version": "/version?limit=100&offset=0",
    "version-group": "/version-group?limit=100&offset=0",
    "pokedex": "/pokedex?limit=100&offset=0",
    
    # Locations and Encounters
    "location": "/location?limit=1000&offset=0",
    "location-area": "/location-area?limit=1000&offset=0",
    "pal-park-area": "/pal-park-area?limit=100&offset=0",
    "region": "/region?limit=100&offset=0",
    "encounter-method": "/encounter-method?limit=100&offset=0",
    "encounter-condition": "/encounter-condition?limit=100&offset=0",
    "encounter-condition-value": "/encounter-condition-value?limit=100&offset=0",
    
    # Stats and Characteristics
    "stat": "/stat?limit=100&offset=0",
    "characteristic": "/characteristic?limit=100&offset=0",
    
    # Pokémon Classification
    "egg-group": "/egg-group?limit=100&offset=0",
    "gender": "/gender?limit=100&offset=0",
    
    # Natures and Training
    "nature": "/nature?limit=100&offset=0",
    "pokeathlon-stat": "/pokeathlon-stat?limit=100&offset=0",
    
    # Machines
    "machine": "/machine?limit=10000&offset=0",
    
    # Languages and Localization
    "language": "/language?limit=100&offset=0",
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

    # Create comprehensive table schemas
    cur.executescript(
        """
    -- Core Pokémon tables (existing)
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
        shape TEXT,
        gender_rate INTEGER,
        is_baby INTEGER,
        hatch_counter INTEGER,
        has_gender_differences INTEGER,
        forms_switchable INTEGER,
        order_ INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY, 
        name TEXT,
        species_id INTEGER, 
        base_experience INT, 
        is_default INT,
        height INTEGER,
        weight INTEGER,
        order_ INTEGER
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
    
    -- Moves and Abilities
    CREATE TABLE IF NOT EXISTS move (
        id INTEGER PRIMARY KEY,
        name TEXT,
        accuracy INTEGER,
        effect_chance INTEGER,
        pp INTEGER,
        priority INTEGER,
        power INTEGER,
        contest_type TEXT,
        damage_class TEXT,
        generation_id INTEGER,
        target TEXT,
        type_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS ability (
        id INTEGER PRIMARY KEY,
        name TEXT,
        is_main_series INTEGER,
        generation_id INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS move_category (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_damage_class (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_target (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_ailment (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_learn_method (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    -- Items
    CREATE TABLE IF NOT EXISTS item (
        id INTEGER PRIMARY KEY,
        name TEXT,
        cost INTEGER,
        fling_power INTEGER,
        fling_effect TEXT,
        category TEXT,
        attributes TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_category (
        id INTEGER PRIMARY KEY,
        name TEXT,
        pocket TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_attribute (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_pocket (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_fling_effect (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    -- Berries
    CREATE TABLE IF NOT EXISTS berry (
        id INTEGER PRIMARY KEY,
        name TEXT,
        growth_time INTEGER,
        max_harvest INTEGER,
        natural_gift_power INTEGER,
        size INTEGER,
        smoothness INTEGER,
        soil_dryness INTEGER,
        firmness TEXT,
        item_name TEXT,
        natural_gift_type TEXT
    );
    
    CREATE TABLE IF NOT EXISTS berry_firmness (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS berry_flavor (
        id INTEGER PRIMARY KEY,
        name TEXT,
        contest_type TEXT
    );
    
    -- Contest
    CREATE TABLE IF NOT EXISTS contest_type (
        id INTEGER PRIMARY KEY,
        name TEXT,
        berry_flavor TEXT
    );
    
    CREATE TABLE IF NOT EXISTS contest_effect (
        id INTEGER PRIMARY KEY,
        appeal INTEGER,
        jam INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS super_contest_effect (
        id INTEGER PRIMARY KEY,
        appeal INTEGER
    );
    
    -- Evolution
    CREATE TABLE IF NOT EXISTS evolution_chain (
        id INTEGER PRIMARY KEY,
        baby_trigger_item TEXT
    );
    
    CREATE TABLE IF NOT EXISTS evolution_trigger (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    -- Games and Versions
    CREATE TABLE IF NOT EXISTS generation (
        id INTEGER PRIMARY KEY,
        name TEXT,
        main_region TEXT
    );
    
    CREATE TABLE IF NOT EXISTS version (
        id INTEGER PRIMARY KEY,
        name TEXT,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS version_group (
        id INTEGER PRIMARY KEY,
        name TEXT,
        order_ INTEGER,
        generation TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokedex (
        id INTEGER PRIMARY KEY,
        name TEXT,
        is_main_series INTEGER,
        region TEXT
    );
    
    -- Locations
    CREATE TABLE IF NOT EXISTS location (
        id INTEGER PRIMARY KEY,
        name TEXT,
        region TEXT
    );
    
    CREATE TABLE IF NOT EXISTS location_area (
        id INTEGER PRIMARY KEY,
        name TEXT,
        game_index INTEGER,
        location TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pal_park_area (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS region (
        id INTEGER PRIMARY KEY,
        name TEXT,
        main_generation TEXT
    );
    
    -- Encounters
    CREATE TABLE IF NOT EXISTS encounter_method (
        id INTEGER PRIMARY KEY,
        name TEXT,
        order_ INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS encounter_condition (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS encounter_condition_value (
        id INTEGER PRIMARY KEY,
        name TEXT,
        condition TEXT
    );
    
    -- Stats
    CREATE TABLE IF NOT EXISTS stat (
        id INTEGER PRIMARY KEY,
        name TEXT,
        game_index INTEGER,
        is_battle_only INTEGER,
        move_damage_class TEXT
    );
    
    CREATE TABLE IF NOT EXISTS characteristic (
        id INTEGER PRIMARY KEY,
        gene_modulo INTEGER,
        possible_values TEXT,
        highest_stat TEXT
    );
    
    -- Pokémon Classification
    CREATE TABLE IF NOT EXISTS egg_group (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS gender (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_color (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_shape (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_form (
        id INTEGER PRIMARY KEY,
        name TEXT,
        order_ INTEGER,
        form_order INTEGER,
        is_default INTEGER,
        is_battle_only INTEGER,
        is_mega INTEGER,
        form_name TEXT,
        pokemon TEXT,
        version_group TEXT
    );
    
    -- Natures
    CREATE TABLE IF NOT EXISTS nature (
        id INTEGER PRIMARY KEY,
        name TEXT,
        decreased_stat TEXT,
        increased_stat TEXT,
        hates_flavor TEXT,
        likes_flavor TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokeathlon_stat (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_battle_style (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    
    -- Machines
    CREATE TABLE IF NOT EXISTS machine (
        id INTEGER PRIMARY KEY,
        item TEXT,
        move TEXT,
        version_group TEXT
    );
    
    -- Languages
    CREATE TABLE IF NOT EXISTS language (
        id INTEGER PRIMARY KEY,
        name TEXT,
        official INTEGER,
        iso639 TEXT,
        iso3166 TEXT
    );
    
    -- Junction tables for many-to-many relationships
    CREATE TABLE IF NOT EXISTS pokemon_moves (
        pokemon_id INTEGER,
        move_name TEXT,
        learn_method TEXT,
        version_group TEXT,
        level_learned_at INTEGER,
        order_ INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_held_items (
        pokemon_id INTEGER,
        item_name TEXT,
        version TEXT,
        rarity INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_forms (
        pokemon_id INTEGER,
        form_name TEXT,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_past_types (
        pokemon_id INTEGER,
        generation TEXT,
        type_name TEXT,
        slot INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_past_abilities (
        pokemon_id INTEGER,
        generation TEXT,
        ability_name TEXT,
        is_hidden INTEGER,
        slot INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_game_indices (
        pokemon_id INTEGER,
        generation TEXT,
        game_index INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_sprites (
        pokemon_id INTEGER,
        front_default TEXT,
        front_shiny TEXT,
        front_female TEXT,
        front_shiny_female TEXT,
        back_default TEXT,
        back_shiny TEXT,
        back_female TEXT,
        back_shiny_female TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_cries (
        pokemon_id INTEGER,
        latest TEXT,
        legacy TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_form_types (
        form_id INTEGER,
        type_name TEXT,
        slot INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_form_sprites (
        form_id INTEGER,
        front_default TEXT,
        front_shiny TEXT,
        back_default TEXT,
        back_shiny TEXT
    );
    
    CREATE TABLE IF NOT EXISTS type_relations (
        type_id INTEGER,
        target_type TEXT,
        damage_factor REAL
    );
    
    CREATE TABLE IF NOT EXISTS type_relations_past (
        type_id INTEGER,
        generation TEXT,
        target_type TEXT,
        damage_factor REAL
    );
    
    CREATE TABLE IF NOT EXISTS type_pokemon (
        type_id INTEGER,
        pokemon_name TEXT,
        slot INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS move_effects (
        move_id INTEGER,
        effect TEXT,
        short_effect TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_flavor_text (
        move_id INTEGER,
        flavor_text TEXT,
        language TEXT,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_stat_changes (
        move_id INTEGER,
        stat_name TEXT,
        change INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS move_meta_data (
        move_id INTEGER,
        ailment TEXT,
        category TEXT,
        min_hits INTEGER,
        max_hits INTEGER,
        min_turns INTEGER,
        max_turns INTEGER,
        drain INTEGER,
        healing INTEGER,
        crit_rate INTEGER,
        ailment_chance INTEGER,
        flinch_chance INTEGER,
        stat_chance INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS move_past_values (
        move_id INTEGER,
        accuracy INTEGER,
        effect_chance INTEGER,
        power INTEGER,
        pp INTEGER,
        type_name TEXT,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_contest_combos (
        move_id INTEGER,
        combo_type TEXT,
        use_before TEXT,
        use_after TEXT
    );
    
    CREATE TABLE IF NOT EXISTS ability_effects (
        ability_id INTEGER,
        effect TEXT,
        short_effect TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS ability_flavor_text (
        ability_id INTEGER,
        flavor_text TEXT,
        language TEXT,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS ability_effect_changes (
        ability_id INTEGER,
        version_group TEXT,
        effect TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS ability_pokemon (
        ability_id INTEGER,
        pokemon_name TEXT,
        is_hidden INTEGER,
        slot INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS item_effects (
        item_id INTEGER,
        effect TEXT,
        short_effect TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_flavor_text (
        item_id INTEGER,
        flavor_text TEXT,
        language TEXT,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_game_indices (
        item_id INTEGER,
        generation TEXT,
        game_index INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS item_sprites (
        item_id INTEGER,
        default_sprite TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_holder_pokemon (
        item_id INTEGER,
        pokemon_name TEXT,
        version TEXT,
        rarity INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS item_machines (
        item_id INTEGER,
        move_name TEXT,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS berry_flavors (
        berry_id INTEGER,
        flavor_name TEXT,
        potency INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS contest_effect_entries (
        contest_effect_id INTEGER,
        effect TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS contest_effect_flavor_text (
        contest_effect_id INTEGER,
        flavor_text TEXT,
        language TEXT,
        version TEXT
    );
    
    CREATE TABLE IF NOT EXISTS super_contest_effect_flavor_text (
        super_contest_effect_id INTEGER,
        flavor_text TEXT,
        language TEXT,
        version TEXT
    );
    
    CREATE TABLE IF NOT EXISTS super_contest_effect_moves (
        super_contest_effect_id INTEGER,
        move_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS evolution_chain_details (
        evolution_chain_id INTEGER,
        species_name TEXT,
        evolution_details TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokedex_entries (
        pokedex_id INTEGER,
        entry_number INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokedex_descriptions (
        pokedex_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokedex_names (
        pokedex_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokedex_version_groups (
        pokedex_id INTEGER,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS generation_abilities (
        generation_id INTEGER,
        ability_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS generation_moves (
        generation_id INTEGER,
        move_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS generation_pokemon_species (
        generation_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS generation_types (
        generation_id INTEGER,
        type_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS generation_version_groups (
        generation_id INTEGER,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS generation_names (
        generation_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS version_names (
        version_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS version_group_move_learn_methods (
        version_group_id INTEGER,
        move_learn_method TEXT
    );
    
    CREATE TABLE IF NOT EXISTS version_group_pokedexes (
        version_group_id INTEGER,
        pokedex TEXT
    );
    
    CREATE TABLE IF NOT EXISTS version_group_regions (
        version_group_id INTEGER,
        region TEXT
    );
    
    CREATE TABLE IF NOT EXISTS version_group_versions (
        version_group_id INTEGER,
        version TEXT
    );
    
    CREATE TABLE IF NOT EXISTS location_names (
        location_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS location_game_indices (
        location_id INTEGER,
        generation TEXT,
        game_index INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS location_areas (
        location_id INTEGER,
        area_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS location_area_encounter_method_rates (
        location_area_id INTEGER,
        encounter_method TEXT,
        version TEXT,
        rate INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS location_area_pokemon_encounters (
        location_area_id INTEGER,
        pokemon_name TEXT,
        version TEXT,
        max_chance INTEGER,
        encounter_details TEXT
    );
    
    CREATE TABLE IF NOT EXISTS location_area_names (
        location_area_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pal_park_encounter_species (
        pal_park_area_id INTEGER,
        pokemon_species TEXT,
        base_score INTEGER,
        rate INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pal_park_area_names (
        pal_park_area_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS region_locations (
        region_id INTEGER,
        location_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS region_pokedexes (
        region_id INTEGER,
        pokedex TEXT
    );
    
    CREATE TABLE IF NOT EXISTS region_version_groups (
        region_id INTEGER,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS region_names (
        region_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS encounter_method_names (
        encounter_method_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS encounter_condition_names (
        encounter_condition_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS encounter_condition_values (
        encounter_condition_id INTEGER,
        value_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS encounter_condition_value_names (
        encounter_condition_value_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS stat_affecting_moves (
        stat_id INTEGER,
        move_name TEXT,
        change INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS stat_affecting_natures (
        stat_id INTEGER,
        nature_name TEXT,
        change_type TEXT
    );
    
    CREATE TABLE IF NOT EXISTS stat_characteristics (
        stat_id INTEGER,
        characteristic_id INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS stat_names (
        stat_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS characteristic_descriptions (
        characteristic_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS egg_group_names (
        egg_group_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS egg_group_pokemon_species (
        egg_group_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS gender_pokemon_species_details (
        gender_id INTEGER,
        pokemon_species TEXT,
        rate INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS gender_required_for_evolution (
        gender_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS growth_rate_descriptions (
        growth_rate_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS growth_rate_levels (
        growth_rate_id INTEGER,
        level INTEGER,
        experience INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS growth_rate_pokemon_species (
        growth_rate_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS nature_pokeathlon_stat_changes (
        nature_id INTEGER,
        pokeathlon_stat TEXT,
        max_change INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS nature_move_battle_style_preferences (
        nature_id INTEGER,
        move_battle_style TEXT,
        low_hp_preference INTEGER,
        high_hp_preference INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS nature_names (
        nature_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokeathlon_stat_names (
        pokeathlon_stat_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokeathlon_stat_affecting_natures (
        pokeathlon_stat_id INTEGER,
        nature_name TEXT,
        max_change INTEGER,
        change_type TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_battle_style_names (
        move_battle_style_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_category_descriptions (
        move_category_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_category_moves (
        move_category_id INTEGER,
        move_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_damage_class_descriptions (
        move_damage_class_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_damage_class_moves (
        move_damage_class_id INTEGER,
        move_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_damage_class_names (
        move_damage_class_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_learn_method_descriptions (
        move_learn_method_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_learn_method_names (
        move_learn_method_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_learn_method_version_groups (
        move_learn_method_id INTEGER,
        version_group TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_target_descriptions (
        move_target_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_target_moves (
        move_target_id INTEGER,
        move_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_target_names (
        move_target_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_ailment_moves (
        move_ailment_id INTEGER,
        move_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS move_ailment_names (
        move_ailment_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_attribute_items (
        item_attribute_id INTEGER,
        item_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_attribute_names (
        item_attribute_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_attribute_descriptions (
        item_attribute_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_category_items (
        item_category_id INTEGER,
        item_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_category_names (
        item_category_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_fling_effect_entries (
        item_fling_effect_id INTEGER,
        effect TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_fling_effect_items (
        item_fling_effect_id INTEGER,
        item_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_pocket_categories (
        item_pocket_id INTEGER,
        category_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS item_pocket_names (
        item_pocket_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS berry_firmness_berries (
        berry_firmness_id INTEGER,
        berry_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS berry_firmness_names (
        berry_firmness_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS berry_flavor_berries (
        berry_flavor_id INTEGER,
        berry_name TEXT,
        potency INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS berry_flavor_names (
        berry_flavor_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS contest_type_names (
        contest_type_id INTEGER,
        name TEXT,
        language TEXT,
        color TEXT
    );
    
    CREATE TABLE IF NOT EXISTS evolution_trigger_names (
        evolution_trigger_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS evolution_trigger_pokemon_species (
        evolution_trigger_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_color_names (
        pokemon_color_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_color_pokemon_species (
        pokemon_color_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_form_types (
        pokemon_form_id INTEGER,
        type_name TEXT,
        slot INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_form_names (
        pokemon_form_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_form_form_names (
        pokemon_form_id INTEGER,
        form_name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_habitat_names (
        pokemon_habitat_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_habitat_pokemon_species (
        pokemon_habitat_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_shape_awesome_names (
        pokemon_shape_id INTEGER,
        awesome_name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_shape_names (
        pokemon_shape_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_shape_pokemon_species (
        pokemon_shape_id INTEGER,
        pokemon_species TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_species_dex_entries (
        pokemon_species_id INTEGER,
        entry_number INTEGER,
        pokedex TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_species_pal_park_encounters (
        pokemon_species_id INTEGER,
        area TEXT,
        base_score INTEGER,
        rate INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_species_flavor_text (
        pokemon_species_id INTEGER,
        flavor_text TEXT,
        language TEXT,
        version TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_species_form_descriptions (
        pokemon_species_id INTEGER,
        description TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_species_genera (
        pokemon_species_id INTEGER,
        genus TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_species_varieties (
        pokemon_species_id INTEGER,
        pokemon_name TEXT,
        is_default INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS pokemon_species_names (
        pokemon_species_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS language_names (
        language_id INTEGER,
        name TEXT,
        language TEXT
    );
    
    CREATE TABLE IF NOT EXISTS flavor_text (
        resource_type TEXT,
        resource_id INTEGER,
        flavor_text TEXT,
        language TEXT,
        version_group TEXT
    );
    """
    )

    # Clear existing data (extended)
    cur.executescript(
        """
    DELETE FROM flavor_text;
    DELETE FROM item_effects;
    DELETE FROM ability_effects;
    DELETE FROM move_effects;
    DELETE FROM type_relations;
    DELETE FROM pokemon_forms;
    DELETE FROM pokemon_held_items;
    DELETE FROM pokemon_moves;
    DELETE FROM language;
    DELETE FROM machine;
    DELETE FROM move_battle_style;
    DELETE FROM pokeathlon_stat;
    DELETE FROM nature;
    DELETE FROM pokemon_form;
    DELETE FROM pokemon_shape;
    DELETE FROM pokemon_color;
    DELETE FROM gender;
    DELETE FROM egg_group;
    DELETE FROM characteristic;
    DELETE FROM stat;
    DELETE FROM encounter_condition_value;
    DELETE FROM encounter_condition;
    DELETE FROM encounter_method;
    DELETE FROM region;
    DELETE FROM pal_park_area;
    DELETE FROM location_area;
    DELETE FROM location;
    DELETE FROM pokedex;
    DELETE FROM version_group;
    DELETE FROM version;
    DELETE FROM generation;
    DELETE FROM evolution_trigger;
    DELETE FROM evolution_chain;
    DELETE FROM super_contest_effect;
    DELETE FROM contest_effect;
    DELETE FROM contest_type;
    DELETE FROM berry_flavor;
    DELETE FROM berry_firmness;
    DELETE FROM berry;
    DELETE FROM item_fling_effect;
    DELETE FROM item_pocket;
    DELETE FROM item_attribute;
    DELETE FROM item_category;
    DELETE FROM item;
    DELETE FROM move_learn_method;
    DELETE FROM move_ailment;
    DELETE FROM move_target;
    DELETE FROM move_damage_class;
    DELETE FROM move_category;
    DELETE FROM ability;
    DELETE FROM move;
    DELETE FROM pokemon_abilities;
    DELETE FROM pokemon_stats;
    DELETE FROM pokemon_types;
    DELETE FROM pokemon;
    DELETE FROM pokemon_species;
    DELETE FROM type;
    """
    )

    # Load core data (existing functionality)
    logger.info("Loading species")
    for obj in tqdm(_paginate(BASE_URL + TABLES["pokemon_species"]), desc="Species"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                """INSERT INTO pokemon_species
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
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
                    data["gender_rate"],
                    int(data["is_baby"]),
                    data["hatch_counter"],
                    int(data["has_gender_differences"]),
                    int(data["forms_switchable"]),
                    data["order"],
                ),
            )
        except Exception as e:
            logger.warning(f"Error loading species {obj['name']}: {e}")

    # Load pokemon + types + stats + abilities (existing)
    logger.info("Loading pokemon details")
    for obj in tqdm(_paginate(BASE_URL + TABLES["pokemon"]), desc="Pokemon"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            
            # Insert pokemon
            cur.execute(
                """INSERT INTO pokemon VALUES(?,?,?,?,?,?,?,?)""",
                (
                    data["id"],
                    data["name"],
                    data["species"]["url"].split("/")[-2],
                    data["base_experience"],
                    int(data["is_default"]),
                    data["height"],
                    data["weight"],
                    data["order"],
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
            
            # Insert moves
            for m in data["moves"]:
                for vg in m["version_group_details"]:
                    cur.execute(
                        "INSERT INTO pokemon_moves VALUES (?,?,?,?,?,?)",
                        (
                            data["id"],
                            m["move"]["name"],
                            vg["move_learn_method"]["name"],
                            vg["version_group"]["name"],
                            vg["level_learned_at"],
                            vg.get("order", None),
                        ),
                    )
            
            # Insert held items
            for h in data["held_items"]:
                for vd in h["version_details"]:
                    cur.execute(
                        "INSERT INTO pokemon_held_items VALUES (?,?,?,?)",
                        (data["id"], h["item"]["name"], vd["version"]["name"], vd["rarity"]),
                    )
                
        except Exception as e:
            logger.warning(f"Error loading pokemon {obj['name']}: {e}")

    # Load type lookup table (existing)
    logger.info("Loading types")
    for obj in tqdm(_paginate(BASE_URL + TABLES["type"]), desc="Types"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO type VALUES(?,?)",
                (data["id"], data["name"]),
            )
            
            # Load type relations
            for damage_type, types in data["damage_relations"].items():
                for t in types:
                    damage_factor = 2.0 if "double" in damage_type else 0.5 if "half" in damage_type else 0.0
                    cur.execute(
                        "INSERT INTO type_relations VALUES (?,?,?)",
                        (data["id"], t["name"], damage_factor),
                    )
        except Exception as e:
            logger.warning(f"Error loading type {obj['name']}: {e}")

    # Load moves
    logger.info("Loading moves")
    for obj in tqdm(_paginate(BASE_URL + TABLES["move"]), desc="Moves"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                """INSERT INTO move VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    data["id"],
                    data["name"],
                    data["accuracy"],
                    data["effect_chance"],
                    data["pp"],
                    data["priority"],
                    data["power"],
                    data["contest_type"]["name"] if data["contest_type"] else None,
                    data["damage_class"]["name"] if data["damage_class"] else None,
                    data["generation"]["url"].split("/")[-2],
                    data["target"]["name"] if data["target"] else None,
                    data["type"]["name"],
                ),
            )
            
            # Load move effects
            for effect in data["effect_entries"]:
                cur.execute(
                    "INSERT INTO move_effects VALUES (?,?,?,?)",
                    (data["id"], effect["effect"], effect["short_effect"], effect["language"]["name"]),
                )
        except Exception as e:
            logger.warning(f"Error loading move {obj['name']}: {e}")

    # Load abilities
    logger.info("Loading abilities")
    for obj in tqdm(_paginate(BASE_URL + TABLES["ability"]), desc="Abilities"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO ability VALUES(?,?,?,?)",
                (
                    data["id"],
                    data["name"],
                    int(data["is_main_series"]),
                    data["generation"]["url"].split("/")[-2],
                ),
            )
            
            # Load ability effects
            for effect in data["effect_entries"]:
                cur.execute(
                    "INSERT INTO ability_effects VALUES (?,?,?,?)",
                    (data["id"], effect["effect"], effect["short_effect"], effect["language"]["name"]),
                )
        except Exception as e:
            logger.warning(f"Error loading ability {obj['name']}: {e}")

    # Load items
    logger.info("Loading items")
    for obj in tqdm(_paginate(BASE_URL + TABLES["item"]), desc="Items"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO item VALUES(?,?,?,?,?,?,?)",
                (
                    data["id"],
                    data["name"],
                    data["cost"],
                    data["fling_power"],
                    data["fling_effect"]["name"] if data["fling_effect"] else None,
                    data["category"]["name"] if data["category"] else None,
                    ",".join([attr["name"] for attr in data["attributes"]]),
                ),
            )
            
            # Load item effects
            for effect in data["effect_entries"]:
                cur.execute(
                    "INSERT INTO item_effects VALUES (?,?,?,?)",
                    (data["id"], effect["effect"], effect["short_effect"], effect["language"]["name"]),
                )
        except Exception as e:
            logger.warning(f"Error loading item {obj['name']}: {e}")

    # Load berries
    logger.info("Loading berries")
    for obj in tqdm(_paginate(BASE_URL + TABLES["berry"]), desc="Berries"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO berry VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (
                    data["id"],
                    data["name"],
                    data["growth_time"],
                    data["max_harvest"],
                    data["natural_gift_power"],
                    data["size"],
                    data["smoothness"],
                    data["soil_dryness"],
                    data["firmness"]["name"],
                    data["item"]["name"],
                    data["natural_gift_type"]["name"],
                ),
            )
        except Exception as e:
            logger.warning(f"Error loading berry {obj['name']}: {e}")

    # Load generations
    logger.info("Loading generations")
    for obj in tqdm(_paginate(BASE_URL + TABLES["generation"]), desc="Generations"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO generation VALUES(?,?,?)",
                (
                    data["id"],
                    data["name"],
                    data["main_region"]["name"] if data["main_region"] else None,
                ),
            )
        except Exception as e:
            logger.warning(f"Error loading generation {obj['name']}: {e}")

    # Load locations
    logger.info("Loading locations")
    for obj in tqdm(_paginate(BASE_URL + TABLES["location"]), desc="Locations"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO location VALUES(?,?,?)",
                (
                    data["id"],
                    data["name"],
                    data["region"]["name"] if data["region"] else None,
                ),
            )
        except Exception as e:
            logger.warning(f"Error loading location {obj['name']}: {e}")

    # Load natures
    logger.info("Loading natures")
    for obj in tqdm(_paginate(BASE_URL + TABLES["nature"]), desc="Natures"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO nature VALUES(?,?,?,?,?,?)",
                (
                    data["id"],
                    data["name"],
                    data["decreased_stat"]["name"] if data["decreased_stat"] else None,
                    data["increased_stat"]["name"] if data["increased_stat"] else None,
                    data["hates_flavor"]["name"] if data["hates_flavor"] else None,
                    data["likes_flavor"]["name"] if data["likes_flavor"] else None,
                ),
            )
        except Exception as e:
            logger.warning(f"Error loading nature {obj['name']}: {e}")

    # Load stats
    logger.info("Loading stats")
    for obj in tqdm(_paginate(BASE_URL + TABLES["stat"]), desc="Stats"):
        try:
            data = requests.get(obj["url"], timeout=30).json()
            cur.execute(
                "INSERT INTO stat VALUES(?,?,?,?,?)",
                (
                    data["id"],
                    data["name"],
                    data["game_index"],
                    int(data["is_battle_only"]),
                    data["move_damage_class"]["name"] if data["move_damage_class"] else None,
                ),
            )
        except Exception as e:
            logger.warning(f"Error loading stat {obj['name']}: {e}")

    # Load other reference tables
    logger.info("Loading reference tables")
    for table_name, endpoint in TABLES.items():
        if table_name in ["pokemon_species", "pokemon", "type", "move", "ability", "item", "berry", "generation", "location", "nature", "stat"]:
            continue  # Already loaded
        
        try:
            logger.info(f"Loading {table_name}")
            for obj in tqdm(_paginate(BASE_URL + endpoint), desc=table_name.title()):
                try:
                    data = requests.get(obj["url"], timeout=30).json()
                    
                    # Handle different table structures
                    if table_name == "move-category":
                        cur.execute("INSERT INTO move_category VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "move-damage-class":
                        cur.execute("INSERT INTO move_damage_class VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "move-target":
                        cur.execute("INSERT INTO move_target VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "move-ailment":
                        cur.execute("INSERT INTO move_ailment VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "move-learn-method":
                        cur.execute("INSERT INTO move_learn_method VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "item-category":
                        cur.execute("INSERT INTO item_category VALUES(?,?,?)", (
                            data["id"], data["name"], data["pocket"]["name"] if data["pocket"] else None
                        ))
                    elif table_name == "item-attribute":
                        cur.execute("INSERT INTO item_attribute VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "item-pocket":
                        cur.execute("INSERT INTO item_pocket VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "item-fling-effect":
                        cur.execute("INSERT INTO item_fling_effect VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "berry-firmness":
                        cur.execute("INSERT INTO berry_firmness VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "berry-flavor":
                        cur.execute("INSERT INTO berry_flavor VALUES(?,?,?)", (
                            data["id"], data["name"], data["contest_type"]["name"] if data["contest_type"] else None
                        ))
                    elif table_name == "contest-type":
                        cur.execute("INSERT INTO contest_type VALUES(?,?,?)", (
                            data["id"], data["name"], data["berry_flavor"]["name"] if data["berry_flavor"] else None
                        ))
                    elif table_name == "contest-effect":
                        cur.execute("INSERT INTO contest_effect VALUES(?,?,?)", (
                            data["id"], data["appeal"], data["jam"]
                        ))
                    elif table_name == "super-contest-effect":
                        cur.execute("INSERT INTO super_contest_effect VALUES(?,?)", (
                            data["id"], data["appeal"]
                        ))
                    elif table_name == "evolution-trigger":
                        cur.execute("INSERT INTO evolution_trigger VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "version":
                        cur.execute("INSERT INTO version VALUES(?,?,?)", (
                            data["id"], data["name"], data["version_group"]["name"]
                        ))
                    elif table_name == "version-group":
                        cur.execute("INSERT INTO version_group VALUES(?,?,?,?)", (
                            data["id"], data["name"], data["order"], data["generation"]["name"]
                        ))
                    elif table_name == "pokedex":
                        cur.execute("INSERT INTO pokedex VALUES(?,?,?,?)", (
                            data["id"], data["name"], int(data["is_main_series"]), data["region"]["name"] if data["region"] else None
                        ))
                    elif table_name == "encounter-method":
                        cur.execute("INSERT INTO encounter_method VALUES(?,?,?)", (
                            data["id"], data["name"], data["order"]
                        ))
                    elif table_name == "encounter-condition":
                        cur.execute("INSERT INTO encounter_condition VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "encounter-condition-value":
                        cur.execute("INSERT INTO encounter_condition_value VALUES(?,?,?)", (
                            data["id"], data["name"], data["condition"]["name"]
                        ))
                    elif table_name == "characteristic":
                        cur.execute("INSERT INTO characteristic VALUES(?,?,?,?)", (
                            data["id"], data["gene_modulo"], ",".join(map(str, data["possible_values"])), data["highest_stat"]["name"]
                        ))
                    elif table_name == "egg-group":
                        cur.execute("INSERT INTO egg_group VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "gender":
                        cur.execute("INSERT INTO gender VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "pokemon-color":
                        cur.execute("INSERT INTO pokemon_color VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "pokemon-shape":
                        cur.execute("INSERT INTO pokemon_shape VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "pokeathlon-stat":
                        cur.execute("INSERT INTO pokeathlon_stat VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "move-battle-style":
                        cur.execute("INSERT INTO move_battle_style VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "language":
                        cur.execute("INSERT INTO language VALUES(?,?,?,?,?)", (
                            data["id"], data["name"], int(data["official"]), data["iso639"], data["iso3166"]
                        ))
                    elif table_name == "machine":
                        cur.execute("INSERT INTO machine VALUES(?,?,?,?)", (
                            data["id"], data["item"]["name"], data["move"]["name"], data["version_group"]["name"]
                        ))
                    elif table_name == "region":
                        cur.execute("INSERT INTO region VALUES(?,?,?)", (
                            data["id"], data["name"], data["main_generation"]["name"] if data["main_generation"] else None
                        ))
                    elif table_name == "pal-park-area":
                        cur.execute("INSERT INTO pal_park_area VALUES(?,?)", (data["id"], data["name"]))
                    elif table_name == "location-area":
                        cur.execute("INSERT INTO location_area VALUES(?,?,?,?)", (
                            data["id"], data["name"], data["game_index"], data["location"]["name"]
                        ))
                    
                except Exception as e:
                    logger.warning(f"Error loading {table_name} {obj['name']}: {e}")
                    
        except Exception as e:
            logger.warning(f"Error loading {table_name}: {e}")

    conn.commit()
    conn.close()
    logger.success("ETL complete → %s", db_path) 