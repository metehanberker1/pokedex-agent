from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

# --- Resource List Types ---
@dataclass
class NamedAPIResourceList:
    count: int
    next: str
    previous: str
    results: List[NamedAPIResource]  # NamedAPIResource should be defined elsewhere

@dataclass
class APIResourceList:
    count: int
    next: str
    previous: str
    results: List[APIResource]  # APIResource should be defined elsewhere

# --- Berries Group ---
@dataclass
class Berry:
    id: int
    name: str
    growth_time: int
    max_harvest: int
    natural_gift_power: int
    size: int
    smoothness: int
    soil_dryness: int
    firmness: NamedAPIResource  # BerryFirmness
    flavors: List[BerryFlavorMap]
    item: NamedAPIResource  # Item
    natural_gift_type: NamedAPIResource  # Type

@dataclass
class BerryFlavorMap:
    potency: int
    flavor: NamedAPIResource  # BerryFlavor

@dataclass
class BerryFirmness:
    id: int
    name: str
    berries: List[NamedAPIResource]  # Berry
    names: List[Name]

@dataclass
class BerryFlavor:
    id: int
    name: str
    berries: List[FlavorBerryMap]
    contest_type: NamedAPIResource  # ContestType
    names: List[Name]

@dataclass
class FlavorBerryMap:
    potency: int
    berry: NamedAPIResource  # Berry

# --- Contest Group ---
@dataclass
class ContestType:
    id: int
    name: str
    berry_flavor: NamedAPIResource  # BerryFlavor
    names: List[ContestName]

@dataclass
class ContestName:
    name: str
    color: str
    language: NamedAPIResource  # Language

@dataclass
class ContestEffect:
    id: int
    appeal: int
    jam: int
    effect_entries: List[Effect]
    flavor_text_entries: List[FlavorText]

@dataclass
class SuperContestEffect:
    id: int
    appeal: int
    flavor_text_entries: List[FlavorText]
    moves: List[NamedAPIResource]  # Move

# --- Utility Group ---
@dataclass
class Language:
    id: int
    name: str
    official: bool
    iso639: str
    iso3166: str
    names: List[Name]

@dataclass
class APIResource:
    url: str

@dataclass
class Description:
    description: str
    language: NamedAPIResource  # Language

@dataclass
class Effect:
    effect: str
    language: NamedAPIResource  # Language

@dataclass
class Encounter:
    min_level: int
    max_level: int
    condition_values: List[NamedAPIResource]  # EncounterConditionValue
    chance: int
    method: NamedAPIResource  # EncounterMethod

@dataclass
class FlavorText:
    flavor_text: str
    language: NamedAPIResource  # Language
    version: NamedAPIResource  # Version

@dataclass
class GenerationGameIndex:
    game_index: int
    generation: NamedAPIResource  # Generation

@dataclass
class MachineVersionDetail:
    machine: APIResource  # Machine
    version_group: NamedAPIResource  # VersionGroup

@dataclass
class Name:
    name: str
    language: NamedAPIResource  # Language

@dataclass
class NamedAPIResource:
    name: str
    url: str

@dataclass
class VerboseEffect:
    effect: str
    short_effect: str
    language: NamedAPIResource  # Language

@dataclass
class VersionEncounterDetail:
    version: NamedAPIResource  # Version
    max_chance: int
    encounter_details: List[Encounter]

@dataclass
class VersionGameIndex:
    game_index: int
    version: NamedAPIResource  # Version

@dataclass
class VersionGroupFlavorText:
    text: str
    language: NamedAPIResource  # Language
    version_group: NamedAPIResource  # VersionGroup

# --- Encounter Group ---
@dataclass
class EncounterMethod:
    id: int
    name: str
    order_: int
    names: List[Name]

@dataclass
class EncounterCondition:
    id: int
    name: str
    names: List[Name]
    values: List[NamedAPIResource]  # EncounterConditionValue

@dataclass
class EncounterConditionValue:
    id: int
    name: str
    condition: NamedAPIResource  # EncounterCondition
    names: List[Name]

# --- Evolution Group ---
@dataclass
class EvolutionChain:
    id: int
    baby_trigger_item: NamedAPIResource  # Item
    chain: ChainLink

@dataclass
class ChainLink:
    is_baby: bool
    species: NamedAPIResource  # PokemonSpecies
    evolution_details: List[EvolutionDetail]
    evolves_to: List[ChainLink]

@dataclass
class EvolutionDetail:
    item: NamedAPIResource  # Item
    trigger: NamedAPIResource  # EvolutionTrigger
    gender: int
    held_item: NamedAPIResource  # Item
    known_move: NamedAPIResource  # Move
    known_move_type: NamedAPIResource  # Type
    location: NamedAPIResource  # Location
    min_level: int
    min_happiness: int
    min_beauty: int
    min_affection: int
    needs_overworld_rain: bool
    party_species: NamedAPIResource  # PokemonSpecies
    party_type: NamedAPIResource  # Type
    relative_physical_stats: int
    time_of_day: str
    trade_species: NamedAPIResource  # PokemonSpecies
    turn_upside_down: bool

@dataclass
class EvolutionTrigger:
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource]  # PokemonSpecies

# --- Pokedex/Version/Generation Group ---
@dataclass
class PokemonEntry:
    entry_number: int
    pokemon_species: NamedAPIResource  # PokemonSpecies

@dataclass
class Pokedex:
    id: int
    name: str
    is_main_series: bool
    descriptions: List[Description]
    names: List[Name]
    pokemon_entries: List[PokemonEntry]
    region: NamedAPIResource  # Region
    version_groups: List[NamedAPIResource]  # VersionGroup

@dataclass
class Version:
    id: int
    name: str
    names: List[Name]
    version_group: NamedAPIResource  # VersionGroup

@dataclass
class Generation:
    id: int
    name: str
    abilities: List[NamedAPIResource]  # Ability
    names: List[Name]
    main_region: NamedAPIResource  # Region
    moves: List[NamedAPIResource]  # Move
    pokemon_species: List[NamedAPIResource]  # PokemonSpecies
    types: List[NamedAPIResource]  # Type
    version_groups: List[NamedAPIResource]  # VersionGroup

@dataclass
class VersionGroup:
    id: int
    name: str
    order_: int
    generation: NamedAPIResource  # Generation
    move_learn_methods: List[NamedAPIResource]  # MoveLearnMethod
    pokedexes: List[NamedAPIResource]  # Pokedex
    regions: List[NamedAPIResource]  # Region
    versions: List[NamedAPIResource]  # Version

# --- Items Group ---
@dataclass
class Item:
    id: int
    name: str
    cost: int
    fling_power: int
    fling_effect: NamedAPIResource  # ItemFlingEffect
    attributes: List[NamedAPIResource]  # ItemAttribute
    category: NamedAPIResource  # ItemCategory
    effect_entries: List[VerboseEffect]
    flavor_text_entries: List[VersionGroupFlavorText]
    game_indices: List[GenerationGameIndex]
    names: List[Name]
    sprites: ItemSprites
    held_by_pokemon: List[ItemHolderPokemon]
    baby_trigger_for: APIResource  # EvolutionChain
    machines: List[MachineVersionDetail]

@dataclass
class ItemSprites:
    default: str

@dataclass
class ItemHolderPokemon:
    pokemon: NamedAPIResource  # Pokemon
    version_details: List[ItemHolderPokemonVersionDetail]

@dataclass
class ItemHolderPokemonVersionDetail:
    rarity: int
    version: NamedAPIResource  # Version

@dataclass
class ItemAttribute:
    id: int
    name: str
    items: List[NamedAPIResource]  # Item
    names: List[Name]
    descriptions: List[Description]

@dataclass
class ItemCategory:
    id: int
    name: str
    items: List[NamedAPIResource]  # Item
    names: List[Name]
    pocket: NamedAPIResource  # ItemPocket

@dataclass
class ItemFlingEffect:
    id: int
    name: str
    effect_entries: List[Effect]
    items: List[NamedAPIResource]  # Item

@dataclass
class ItemPocket:
    id: int
    name: str
    categories: List[NamedAPIResource]  # ItemCategory
    names: List[Name]

# --- Locations Group ---
@dataclass
class Location:
    id: int
    name: str
    region: NamedAPIResource  # Region
    names: List[Name]
    game_indices: List[GenerationGameIndex]
    areas: List[NamedAPIResource]  # LocationArea

@dataclass
class LocationArea:
    id: int
    name: str
    game_index: int
    encounter_method_rates: List[EncounterMethodRate]
    location: NamedAPIResource  # Location
    names: List[Name]
    pokemon_encounters: List[PokemonEncounter]

@dataclass
class EncounterMethodRate:
    encounter_method: NamedAPIResource  # EncounterMethod
    version_details: List[EncounterVersionDetails]

@dataclass
class EncounterVersionDetails:
    rate: int
    version: NamedAPIResource  # Version

@dataclass
class PokemonEncounter:
    pokemon: NamedAPIResource  # Pokemon
    version_details: List[VersionEncounterDetail]

@dataclass
class PalParkArea:
    id: int
    name: str
    names: List[Name]
    pokemon_encounters: List[PalParkEncounterSpecies]

@dataclass
class PalParkEncounterSpecies:
    base_score: int
    rate: int
    pokemon_species: NamedAPIResource  # PokemonSpecies

@dataclass
class Region:
    id: int
    locations: List[NamedAPIResource]  # Location
    name: str
    names: List[Name]
    main_generation: NamedAPIResource  # Generation
    pokedexes: List[NamedAPIResource]  # Pokedex
    version_groups: List[NamedAPIResource]  # VersionGroup

# --- Machines Group ---
@dataclass
class Machine:
    id: int
    item: NamedAPIResource  # Item
    move: NamedAPIResource  # Move
    version_group: NamedAPIResource  # VersionGroup

# --- Moves Group ---
@dataclass
class Move:
    id: int
    name: str
    accuracy: int
    effect_chance: int
    pp: int
    priority: int
    power: int
    contest_combos: ContestComboSets
    contest_type: NamedAPIResource  # ContestType
    contest_effect: APIResource  # ContestEffect
    damage_class: NamedAPIResource  # MoveDamageClass
    effect_entries: List[VerboseEffect]
    effect_changes: List[AbilityEffectChange]
    learned_by_pokemon: List[NamedAPIResource]  # Pokemon
    flavor_text_entries: List[MoveFlavorText]
    generation: NamedAPIResource  # Generation
    machines: List[MachineVersionDetail]
    meta: MoveMetaData
    names: List[Name]
    past_values: List[PastMoveStatValues]
    stat_changes: List[MoveStatChange]
    super_contest_effect: APIResource  # SuperContestEffect
    target: NamedAPIResource  # MoveTarget
    type: NamedAPIResource  # Type

@dataclass
class ContestComboSets:
    normal: ContestComboDetail
    super: ContestComboDetail

@dataclass
class ContestComboDetail:
    use_before: List[NamedAPIResource]  # Move
    use_after: List[NamedAPIResource]  # Move

@dataclass
class MoveFlavorText:
    flavor_text: str
    language: NamedAPIResource  # Language
    version_group: NamedAPIResource  # VersionGroup

@dataclass
class MoveMetaData:
    ailment: NamedAPIResource  # MoveAilment
    category: NamedAPIResource  # MoveCategory
    min_hits: int
    max_hits: int
    min_turns: int
    max_turns: int
    drain: int
    healing: int
    crit_rate: int
    ailment_chance: int
    flinch_chance: int
    stat_chance: int
    
@dataclass
class MoveStatChange:
    change: int
    stat: NamedAPIResource  # Stat

@dataclass
class PastMoveStatValues:
    accuracy: int
    effect_chance: int
    power: int
    pp: int
    effect_entries: List[VerboseEffect]
    type: NamedAPIResource  # Type
    version_group: NamedAPIResource  # VersionGroup

# --- Moves Group (continued) ---
@dataclass
class MoveAilment:
    id: int
    name: str
    moves: List[NamedAPIResource]  # Move
    names: List[Name]

@dataclass
class MoveBattleStyle:
    id: int
    name: str
    names: List[Name]

@dataclass
class MoveCategory:
    id: int
    name: str
    moves: List[NamedAPIResource]  # Move
    descriptions: List[Description]

@dataclass
class MoveDamageClass:
    id: int
    name: str
    descriptions: List[Description]
    moves: List[NamedAPIResource]  # Move
    names: List[Name]

@dataclass
class MoveLearnMethod:
    id: int
    name: str
    descriptions: List[Description]
    names: List[Name]
    version_groups: List[NamedAPIResource]  # VersionGroup

@dataclass
class MoveTarget:
    id: int
    name: str
    descriptions: List[Description]
    moves: List[NamedAPIResource]  # Move
    names: List[Name]

# --- Pokémon Group ---
@dataclass
class Ability:
    id: int
    name: str
    is_main_series: bool
    generation: NamedAPIResource  # Generation
    names: List[Name]
    effect_entries: List[VerboseEffect]
    effect_changes: List[AbilityEffectChange]
    flavor_text_entries: List[AbilityFlavorText]
    pokemon: List[AbilityPokemon]

@dataclass
class AbilityEffectChange:
    effect_entries: List[Effect]
    version_group: NamedAPIResource  # VersionGroup

@dataclass
class AbilityFlavorText:
    flavor_text: str
    language: NamedAPIResource  # Language
    version_group: NamedAPIResource  # VersionGroup

@dataclass
class AbilityPokemon:
    is_hidden: bool
    slot: int
    pokemon: NamedAPIResource  # Pokemon

@dataclass
class Characteristic:
    id: int
    gene_modulo: int
    possible_values: List[int]
    highest_stat: NamedAPIResource  # Stat
    descriptions: List[Description]

@dataclass
class EggGroup:
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource]  # PokemonSpecies

@dataclass
class Gender:
    id: int
    name: str
    pokemon_species_details: List[PokemonSpeciesGender]
    required_for_evolution: List[NamedAPIResource]  # PokemonSpecies

@dataclass
class PokemonSpeciesGender:
    rate: int
    pokemon_species: NamedAPIResource  # PokemonSpecies

@dataclass
class GrowthRate:
    id: int
    name: str
    formula: str
    descriptions: List[Description]
    levels: List[GrowthRateExperienceLevel]
    pokemon_species: List[NamedAPIResource]  # PokemonSpecies

@dataclass
class GrowthRateExperienceLevel:
    level: int
    experience: int

@dataclass
class Nature:
    id: int
    name: str
    decreased_stat: NamedAPIResource  # Stat
    increased_stat: NamedAPIResource  # Stat
    hates_flavor: NamedAPIResource  # BerryFlavor
    likes_flavor: NamedAPIResource  # BerryFlavor
    pokeathlon_stat_changes: List[NatureStatChange]
    move_battle_style_preferences: List[MoveBattleStylePreference]
    names: List[Name]

@dataclass
class NatureStatChange:
    max_change: int
    pokeathlon_stat: NamedAPIResource  # PokeathlonStat

@dataclass
class MoveBattleStylePreference:
    low_hp_preference: int
    high_hp_preference: int
    move_battle_style: NamedAPIResource  # MoveBattleStyle

@dataclass
class PokeathlonStat:
    id: int
    name: str
    names: List[Name]
    affecting_natures: NaturePokeathlonStatAffectSets

@dataclass
class NaturePokeathlonStatAffectSets:
    increase: List[NaturePokeathlonStatAffect]
    decrease: List[NaturePokeathlonStatAffect]

@dataclass
class NaturePokeathlonStatAffect:
    max_change: int
    nature: NamedAPIResource  # Nature

@dataclass
class Pokemon:
    id: int
    name: str
    base_experience: int
    height: int
    is_default: bool
    order_: int
    weight: int
    abilities: List[PokemonAbility]
    forms: List[NamedAPIResource]  # PokemonForm
    game_indices: List[GenerationGameIndex]
    held_items: List[PokemonHeldItem]
    location_area_encounters: str
    moves: List[PokemonMove]
    past_types: List[PokemonTypePast]
    past_abilities: List[PokemonAbilityPast]
    sprites: PokemonSprites
    cries: PokemonCries
    species: NamedAPIResource  # PokemonSpecies
    stats: List[PokemonStat]
    types: List[PokemonType]

@dataclass
class PokemonAbility:
    is_hidden: bool
    slot: int
    ability: NamedAPIResource  # Ability

@dataclass
class PokemonType:
    slot: int
    type: NamedAPIResource  # Type

@dataclass
class PokemonFormType:
    slot: int
    type: NamedAPIResource  # Type

@dataclass
class PokemonTypePast:
    generation: NamedAPIResource  # Generation
    types: List[PokemonType]

@dataclass
class PokemonAbilityPast:
    generation: NamedAPIResource  # Generation
    abilities: List[PokemonAbility]

@dataclass
class PokemonHeldItem:
    item: NamedAPIResource  # Item
    version_details: List[PokemonHeldItemVersion]

@dataclass
class PokemonHeldItemVersion:
    version: NamedAPIResource  # Version
    rarity: int
    
@dataclass
class PokemonMove:
    move: NamedAPIResource  # Move
    version_group_details: List[PokemonMoveVersion]

@dataclass
class PokemonMoveVersion:
    move_learn_method: NamedAPIResource  # MoveLearnMethod
    version_group: NamedAPIResource  # VersionGroup
    level_learned_at: int
    order_: int

@dataclass
class PokemonStat:
    stat: NamedAPIResource  # Stat
    effort: int
    base_stat: int

@dataclass
class PokemonSprites:
    front_default: str
    front_shiny: str
    front_female: str
    front_shiny_female: str
    back_default: str
    back_shiny: str
    back_female: str
    back_shiny_female: str

@dataclass
class PokemonCries:
    latest: str
    legacy: str

# --- Pokémon Group (continued) ---
@dataclass
class LocationAreaEncounter:
    location_area: NamedAPIResource  # LocationArea
    version_details: List[VersionEncounterDetail]

@dataclass
class PokemonColor:
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource]  # PokemonSpecies

@dataclass
class PokemonForm:
    id: int
    name: str
    order_: int
    form_order_: int
    is_default: bool
    is_battle_only: bool
    is_mega: bool
    form_name: str
    pokemon: NamedAPIResource  # Pokemon
    types: List[PokemonFormType]
    sprites: PokemonFormSprites
    version_group: NamedAPIResource  # VersionGroup
    names: List[Name]
    form_names: List[Name]

@dataclass
class PokemonFormSprites:
    front_default: str
    front_shiny: str
    back_default: str
    back_shiny: str

@dataclass
class PokemonHabitat:
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource]  # PokemonSpecies

@dataclass
class PokemonShape:
    id: int
    name: str
    awesome_names: List[AwesomeName]
    names: List[Name]
    pokemon_species: List[NamedAPIResource]  # PokemonSpecies

@dataclass
class AwesomeName:
    awesome_name: str
    language: NamedAPIResource  # Language

@dataclass
class PokemonSpecies:
    id: int
    name: str
    order_: int
    gender_rate: int
    capture_rate: int
    base_happiness: int
    is_baby: bool
    is_legendary: bool
    is_mythical: bool
    hatch_counter: int
    has_gender_differences: bool
    forms_switchable: bool
    growth_rate: NamedAPIResource  # GrowthRate
    pokedex_numbers: List[PokemonSpeciesDexEntry]
    egg_groups: List[NamedAPIResource]  # EggGroup
    color: NamedAPIResource  # PokemonColor
    shape: NamedAPIResource  # PokemonShape
    evolves_from_species: NamedAPIResource  # PokemonSpecies
    evolution_chain: APIResource  # EvolutionChain
    habitat: NamedAPIResource  # PokemonHabitat
    generation: NamedAPIResource  # Generation
    names: List[Name]
    pal_park_encounters: List[PalParkEncounterArea]
    flavor_text_entries: List[FlavorText]
    form_descriptions: List[Description]
    genera: List[Genus]
    varieties: List[PokemonSpeciesVariety]

@dataclass
class Genus:
    genus: str
    language: NamedAPIResource  # Language

@dataclass
class PokemonSpeciesDexEntry:
    entry_number: int
    pokedex: NamedAPIResource  # Pokedex

@dataclass
class PalParkEncounterArea:
    base_score: int
    rate: int
    area: NamedAPIResource  # PalParkArea

@dataclass
class PokemonSpeciesVariety:
    is_default: bool
    pokemon: NamedAPIResource  # Pokemon

@dataclass
class Stat:
    id: int
    name: str
    game_index: int
    is_battle_only: bool
    affecting_moves: MoveStatAffectSets
    affecting_natures: NatureStatAffectSets
    characteristics: List[APIResource]  # Characteristic
    move_damage_class: NamedAPIResource  # MoveDamageClass
    names: List[Name]

@dataclass
class MoveStatAffectSets:
    increase: List[MoveStatAffect]
    decrease: List[MoveStatAffect]

@dataclass
class MoveStatAffect:
    change: int
    move: NamedAPIResource  # Move

@dataclass
class NatureStatAffectSets:
    increase: List[NamedAPIResource]  # Nature
    decrease: List[NamedAPIResource]  # Nature

@dataclass
class Type:
    id: int
    name: str
    damage_relations: TypeRelations
    past_damage_relations: List[TypeRelationsPast]
    game_indices: List[GenerationGameIndex]
    generation: NamedAPIResource  # Generation
    move_damage_class: NamedAPIResource  # MoveDamageClass
    names: List[Name]
    pokemon: List[TypePokemon]
    moves: List[NamedAPIResource]  # Move

@dataclass
class TypePokemon:
    slot: int
    pokemon: NamedAPIResource  # Pokemon

@dataclass
class TypeRelations:
    no_damage_to: List[NamedAPIResource]  # Type
    half_damage_to: List[NamedAPIResource]  # Type
    double_damage_to: List[NamedAPIResource]  # Type
    no_damage_from: List[NamedAPIResource]  # Type
    half_damage_from: List[NamedAPIResource]  # Type
    double_damage_from: List[NamedAPIResource]  # Type

@dataclass
class TypeRelationsPast:
    generation: NamedAPIResource  # Generation
    damage_relations: TypeRelations