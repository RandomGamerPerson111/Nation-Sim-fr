import math
import sys
from suffixes import SN, ISN, SNS

FOCUS_DATASET = {
    "Basic": {
        "gold": 100, "happiness": 100, "population": 10000, "anger": 0,
        "pop_gain": 250, "pop_gain2": 50, "t2_cost": 50, "gpc": 0.05,
        "hap_gain": 1, "ore_boost": 1.0, "farming_boost": 1.0, "influence_boost": 1.0, "research_boost": 1.0
    },
    "Science": {
        "gold": 25, "happiness": 85, "population": 2000, "anger": 50,
        "pop_gain": 50, "pop_gain2": 10, "t2_cost": 75, "gpc": 0.01,
        "hap_gain": 1, "ore_boost": 0.75, "farming_boost": 0.9, "influence_boost": 0.8, "research_boost": 4.0
    },
    "Industry": {
        "gold": 50, "happiness": 85, "population": 7200, "anger": 10,
        "pop_gain": 150, "pop_gain2": 50, "t2_cost": 50, "gpc": 0.01,
        "hap_gain": 0, "ore_boost": 1.5, "farming_boost": 0.9, "influence_boost": 0.9, "research_boost": 1.0
    },
    "Farming": {
        "gold": 50, "happiness": 85, "population": 7200, "anger": 10,
        "pop_gain": 150, "pop_gain2": 50, "t2_cost": 60, "gpc": 0.01,
        "hap_gain": 0, "ore_boost": 0.8, "farming_boost": 1.5, "influence_boost": 0.9, "research_boost": 1.0
    },
    "Gold": {
        "gold": 450, "happiness": 100, "population": 8000, "anger": 0,
        "pop_gain": 25, "pop_gain2": 5, "t2_cost": 75, "gpc": 0.25,
        "hap_gain": 0, "ore_boost": 0.75, "farming_boost": 0.9, "influence_boost": 0.9, "research_boost": 1.0
    },
    "Population": {
        "gold": 100, "happiness": 85, "population": 11500, "anger": 0,
        "pop_gain": 350, "pop_gain2": 60, "t2_cost": 40, "gpc": 0.02,
        "hap_gain": 0, "ore_boost": 1.0, "farming_boost": 0.85, "influence_boost": 0.85, "research_boost": 1.0
    },
    "Stability": {
        "gold": 75, "happiness": 250, "population": 3500, "anger": 0,
        "pop_gain": 90, "pop_gain2": 20, "t2_cost": 60, "gpc": 0.03,
        "hap_gain": 4, "ore_boost": 1.0, "farming_boost": 0.9, "influence_boost": 0.9, "research_boost": 1.0
    },
    "Government": {
        "gold": 75, "happiness": 90, "population": 7000, "anger": 0,
        "pop_gain": 200, "pop_gain2": 35, "t2_cost": 60, "gpc": 0.04,
        "hap_gain": 1, "ore_boost": 0.85, "farming_boost": 0.95, "influence_boost": 2.5, "research_boost": 1.0
    },
    "Science^2": {
        "gold": 0, "happiness": 65, "population": 500, "anger": 25,
        "pop_gain": 0, "pop_gain2": 0, "t2_cost": 150, "gpc": 0.001,
        "hap_gain": -1, "ore_boost": 0.25, "farming_boost": 0.8, "influence_boost": 0.6, "research_boost": 16.0
    },
    "Industry^2": {
        "gold": 1, "happiness": 65, "population": 4500, "anger": 25,
        "pop_gain": 75, "pop_gain2": 10, "t2_cost": 110, "gpc": 0.01,
        "hap_gain": 0, "ore_boost": 2.75, "farming_boost": 0.8, "influence_boost": 0.75, "research_boost": 1.0
    },
    "Farming^2": {
        "gold": 2, "happiness": 65, "population": 4500, "anger": 25,
        "pop_gain": 75, "pop_gain2": 10, "t2_cost": 110, "gpc": 0.01,
        "hap_gain": 0, "ore_boost": 0.5, "farming_boost": 2.5, "influence_boost": 0.8, "research_boost": 1.0
    },
    "Gold^2": {
        "gold": 1000, "happiness": 75, "population": 500, "anger": 0,
        "pop_gain": 1, "pop_gain2": 0, "t2_cost": 100, "gpc": 1.0,
        "hap_gain": -1, "ore_boost": 0.65, "farming_boost": 0.8, "influence_boost": 0.8, "research_boost": 1.0
    },
    "Population^2": {
        "gold": 0, "happiness": 75, "population": 42000, "anger": 50,
        "pop_gain": 1500, "pop_gain2": 400, "t2_cost": 10, "gpc": 0.01,
        "hap_gain": -1, "ore_boost": 0.5, "farming_boost": 0.7, "influence_boost": 0.75, "research_boost": 0.9
    },
    "Stability^2": {
        "gold": 0, "happiness": 550, "population": 4500, "anger": 0,
        "pop_gain": 50, "pop_gain2": 10, "t2_cost": 150, "gpc": 0.01,
        "hap_gain": 10, "ore_boost": 1.0, "farming_boost": 0.8, "influence_boost": 0.85, "research_boost": 1.0
    },
    "Government^2": {
        "gold": 20, "happiness": 85, "population": 4000, "anger": 0,
        "pop_gain": 100, "pop_gain2": 25, "t2_cost": 85, "gpc": 0.01,
        "hap_gain": 0, "ore_boost": 0.65, "farming_boost": 0.85, "influence_boost": 15.0, "research_boost": 1.0
    },
    "Everything": {
        "gold": 10, "happiness": 150, "population": 15000, "anger": 0,
        "pop_gain": 750, "pop_gain2": 150, "t2_cost": 10, "gpc": 0.1,
        "hap_gain": 2, "ore_boost": 1.5, "farming_boost": 1.5, "influence_boost": 2.5, "research_boost": 1.0
    },
    "Everything^2": {
        "gold": 25, "happiness": 250, "population": 25000, "anger": 0,
        "pop_gain": 1550, "pop_gain2": 350, "t2_cost": 1, "gpc": 1,
        "hap_gain": 5, "ore_boost": 5, "farming_boost": 5, "influence_boost": 25, "research_boost": 1.0
    },
    "Singular": {
        "gold": 10, "happiness": 300, "population": 1000, "anger": 0,
        "pop_gain": 25, "pop_gain2": 5, "t2_cost": 500, "gpc": 0.5,
        "hap_gain": 5, "ore_boost": 4, "farming_boost": 4, "influence_boost": 20, "research_boost": 1.0
    },
    "Singular^2": {
        "gold": 1, "happiness": 750, "population": 100, "anger": 0,
        "pop_gain": 2, "pop_gain2": 1, "t2_cost": 500, "gpc": 2,
        "hap_gain": 7, "ore_boost": 15, "farming_boost": 15, "influence_boost": 100, "research_boost": 1.0
    },
}

def generate_nation_from_focus(name, focus):
    if focus not in FOCUS_DATASET:
        raise ValueError(f"Focus '{focus}' is invalid.")
    if focus in ["Everything","Everything^2","Singular","Singular^2"] and not name.__contains__("(AI)"):
        raise ValueError(f"Used AI focus while being a player")

    data = FOCUS_DATASET[focus]
    
    # 1. Scaled Population Demographics (10% children, remaining uneducated farmers)
    population = data["population"]
    childCount = int(population * 0.10)
    uneducatedFarmer = population - childCount
    
    # 2. Dynamic Boost Percentage Transformations
    focusFarmingBoost = round(float((data["farming_boost"] - 1.0) * 100))
    focusOreBoost = round(float((data["ore_boost"] - 1.0) * 100))
    focusResearchBoost = round(float((data["research_boost"] - 1.0) * 100))
    focusGovtBoost = round(float((data["influence_boost"] - 1.0) * 100))
    
    # Science/Science^2 gets their multiplier applied to scientists; others default to x1
    scientistResearchBoost = data["research_boost"] if "Science" in focus else 1.0

    # --- Your Exact Template Injection with hardcoded static defaults ---
    return f"""{name}:
Country focus: {focus}
Gold: {SN(data["gold"])}, Gold ore: 1 (+0), Buff/Nerf: +0%
Gold per capita: {SN(data["gpc"])}, Tax: 14%
Population Stats:
    Population: {SNS(population)} (+{data["pop_gain"]}) (+{data["pop_gain2"]}/t2) (+0%) (t2 cost: {data["t2_cost"]})
    Citizen happiness: {data["happiness"]} (+0) (+{data["hap_gain"]})
    Citizen anger: {data["anger"]} (+0) (/2)
Education Type:
    {childCount} Child
    {uneducatedFarmer} Uneducated
    0 Educated
    0 Military
Uneducated Occupation:
    {uneducatedFarmer} Farmer
    0 Miner
    0 Govt
Educated occupation:
    0 Farmer
    0 Miner
    0 Govt
    0 Scientist
Military Occupation:
    0 Farmer
    0 Miner
    0 Solders
Food:
    0 (+0 Excess per year)
    40% retention
    Farming Boosts:
        Research: (+0%)
        Focus: (+{focusFarmingBoost}%)
        Furnace Level: (+0%)
    Drought:
        Drought Power: 0
        Drought Nerf: 0%
        Drought Duration: 0
Ore:
 -Teir 1 ores-
    Coal: 0, Iron: 0, Copper: 0, Tin: 0, Salt: 0, Sulphur: 0
 -Teir 2 ores-
    Titanium: 0, Cobalt: 0, Tungsten: 0, Oil: 0, Magnesium: 0
 -Teir 3 ores-
    Uranium: 0, Silicon: 0, Beryllium: 0, Hydrogen: 0, Plutonium: 0, Radium: 0, Mythril: 0
    Has: 
    Mining Level: 0
    Ore Boosts:
        Research: (+0%)
        Focus: (+{focusOreBoost}%)
        Mining Level: (x1)
        Furnace Level: (x1)
Research Boosts:
    Research: (+0%)
    Focus: (+{focusResearchBoost}%)
    Furnace level: (x1)
    Scientists: (x{scientistResearchBoost})
Government:
    Needed influence: 0 (0*(1*{SN(uneducatedFarmer)}+10*0+3*0))
    Current educated government employees: 0
    Current uneducated government employees: 0
    Influence per educated employee: 1500
    Influence per uneducated employee: 100
    Influence boosts:
        Research: (+0%)
        Focus: (+{focusGovtBoost}%)
    Government influence is multiplying food, ore, money from tax, and research by x1
Industry:
    Furnace Level: 0
    Furnace req: (0/10k iron, 0/1k bronze, 0/500 coal, 0/500 salt)
    -Material Crafting-
    Bronze: 0 (needs 1 copper and 1 tin for 1)
    Gunpowder: 0 (needs 1 sulphur and 1 coal for 1)
Research: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Military:
    War:
        -0% Farming Nerf
    Weapons:
        None"""



with open("output.txt", "w", encoding="utf-8") as file:
    file.write(generate_nation_from_focus("Yugoslavia", "Government^2"))