import math
import sys
import random
from suffixes import SN, ISN, SNS
from oreFunctions import (
    doOreGain,
    distribute_population,
    calculate,
    handleFL,
    returnFLRequirements,
    stochasticRound,
    cWF,
)

all_nations_output = []

file = open("Nations.txt", "r", encoding="utf-8")
info = file.read()
info2 = info.split("\n\n\n")
globalFurnaceLevel = 0
for nationBlock in info2:
    if not nationBlock.strip():
        continue

    section = "null"

    info3 = nationBlock.split("\n")
    for line in info3:
        line_clean = line.strip()
        line_lower = line_clean.lower()
        if "industry:" in line_lower:
            section = "industry"
        if "furnace level:" in line_lower:
            if section == "industry":
                currentFL = ISN(line_clean.split(": ")[1])

    if currentFL > globalFurnaceLevel:
        globalFurnaceLevel = currentFL


def crafting_tab(steel, gears, steamengine, bora, tractor, furnacelevel, research):
    ret = ""
    if furnacelevel >= 1:
        ret += f"{chr(10)}    Steel: {steelCrafting} (needs 10 iron and 1 coal for 1)"
    if furnacelevel >= 2:
        ret += f"{chr(10)}    Indus:{chr(10)}        Gear: {gearCrafting} (1 bronze for 10)"
    if furnacelevel >= 3:
        ret += f"{chr(10)}        Steam Engine: {steamEngine} (1 Steel for 1)"
    if research[20] >= 1:
        ret += f"{chr(10)}        BORA: {bora} (Needs 10K Steam Engines, 10K Gears, and 100K Coal for 1)"
    if research[21] >= 1:
        ret += f"{chr(10)}        Tractors: {tractors} (Needs 10K Steam Engines, 10K Gears, and 100K Coal for 1)"
    return ret


for nation in range(len(info2)):
    linestack = ""
    info3 = info2[nation].splitlines()
    name = info3[0].split(":")[0]
    focus = info3[1].split(": ")[1]
    section = "null"

    # base cases for conditionals
    steelCrafting = 0
    gearCrafting = 0
    steamEngine = 0
    bora = 0
    tractors = 0
    militaryCopy = ""

    civilWar = False

    # testing zone
    for line in info3:
        # Clean up whitespace but keep case intact for checking structure
        line_clean = line.strip()
        line_lower = line_clean.lower()

        # --- SECTION & CONTEXT TRACKERS ---
        if "uneducated occupation:" in line_lower:
            section = "uneducated"
        elif "education type" in line_lower:
            section = "education type"
        elif "educated occupation:" in line_lower:
            section = "educated"
        elif "military occupation:" in line_lower:
            section = "military"
        elif line_lower == "food:":
            section = "food"
        elif "industry:" in line_lower:
            section = "industry"
        elif "military:" in line_lower:
            section = "militaryStuff"
        elif "weapons:" in line_lower and section == "militaryStuff":
            section = "militaryCopy"
        elif "farming boosts:" in line_lower:
            boost_context = "farming"
        elif "ore boosts:" in line_lower:
            boost_context = "ore"
        elif "research boosts:" in line_lower:
            boost_context = "research"
        elif "influence boosts:" in line_lower:
            boost_context = "govt"

        # --- ECONOMY & GOLD ---
        if "gold:" in line_lower and "gold ore:" in line_lower:
            gold = ISN(line_clean.split(": ")[1].split(",")[0])
            goldOre = ISN(line_clean.split(": ")[2].split(" (")[0])
            goldOreGain = ISN(line_clean.split("(+")[1].split(")")[0])
        elif "gold per capita:" in line_lower:
            gpc = ISN(line_clean.split(": ")[1].split(",")[0])
            tax = ISN(line_clean.split(": ")[2].split("%")[0])

        # --- POPULATION & HAPPINESS ---
        elif "population:" in line_lower and "stats" not in line_lower:
            population = ISN(line_clean.split(": ")[1].split(" (")[0])
            popGain = ISN(line_clean.split("+")[1].split(")")[0])
            popGain2 = ISN(line_clean.split("+")[2].split("/")[0])
            popBoost = ISN(line_clean.split("+")[3].split("%")[0])
        elif "citizen happiness:" in line_lower:
            citHap = ISN(line_clean.split(": ")[1].split(" (")[0])
            citHapGain = ISN(line_clean.split("+")[1].split(")")[0])
            citHapGain2 = ISN(line_clean.split("+")[2].split(")")[0])
        elif "citizen anger:" in line_lower:
            citAng = ISN(line_clean.split(": ")[1].split(" (")[0])
            citAngGain = ISN(line_clean.split("+")[1].split(")")[0])
            citAngDiv = ISN(line_clean.split("/")[1].split(")")[0])

        # --- GLOBAL DEMOGRAPHIC COUNTS ---
        elif "child" in line_lower and section == "education type":
            childCount = ISN(line_clean.split()[0])
        elif (
            "uneducated" in line_lower
            and "occupation" not in line_lower
            and section == "education type"
        ):
            uneducatedCount = ISN(line_clean.split()[0])
        elif (
            "educated" in line_lower
            and "occupation" not in line_lower
            and section == "education type"
        ):
            educatedCount = ISN(line_clean.split()[0])
        elif (
            "military" in line_lower
            and "occupation" not in line_lower
            and section == "education type"
        ):
            militaryCount = ISN(line_clean.split()[0])

        # --- OCCUPATIONS ---
        elif "farmer" in line_lower:
            if section == "uneducated":
                uneducatedFarmer = ISN(line_clean.split()[0])
            elif section == "educated":
                educatedFarmer = ISN(line_clean.split()[0])
            elif section == "military":
                militaryFarmer = ISN(line_clean.split()[0])
        elif "miner" in line_lower:
            if section == "uneducated":
                uneducatedMiner = ISN(line_clean.split()[0])
            elif section == "educated":
                educatedMiner = ISN(line_clean.split()[0])
            elif section == "military":
                militaryMiner = ISN(line_clean.split()[0])
        elif "govt" in line_lower:
            if section == "uneducated":
                uneducatedGovt = ISN(line_clean.split()[0])
            elif section == "educated":
                educatedGovt = ISN(line_clean.split()[0])
        elif "scientist" in line_lower and section == "educated":
            educatedScientist = ISN(line_clean.split()[0])
        elif "solders" in line_lower and section == "military":
            militarySoldiers = ISN(line_clean.split()[0])

        # --- FOOD ---
        elif "excess" in line_lower and section == "food":
            food = ISN(line_clean.split(" (")[0].replace("Food:", "").strip())
            foodExcess = ISN(line_clean.split("(+")[1].split(" ")[0])
        elif "retention" in line_lower and section == "food":
            foodRetention = ISN(line_clean.split("%")[0])
        elif "power:" in line_lower and section == "food":
            droughtPower = ISN(line_clean.split(" ")[2])
        elif "nerf:" in line_lower and section == "food":
            droughtNerf = ISN(line_clean.split(" ")[2].split("%")[0])
        elif "duration:" in line_lower and section == "food":
            droughtDuration = ISN(line_clean.split(" ")[2])

        # --- ORES (TIER 1, 2, 3) ---
        elif "coal:" in line_lower and section != "industry":
            coal = ISN(line_clean.split("Coal: ")[1].split(",")[0])
            iron = ISN(line_clean.split("Iron: ")[1].split(",")[0])
            copper = ISN(line_clean.split("Copper: ")[1].split(",")[0])
            tin = ISN(line_clean.split("Tin: ")[1].split(",")[0])
            salt = ISN(line_clean.split("Salt: ")[1].split(",")[0])
            sulphur = ISN(line_clean.split("Sulphur: ")[1].strip())
        elif "titanium:" in line_lower and section != "industry":
            titanium = ISN(line_clean.split("Titanium: ")[1].split(",")[0])
            cobalt = ISN(line_clean.split("Cobalt: ")[1].split(",")[0])
            tungsten = ISN(line_clean.split("Tungsten: ")[1].split(",")[0])
            oil = ISN(line_clean.split("Oil: ")[1].split(",")[0])
            magnesium = ISN(line_clean.split("Magnesium: ")[1].strip())
        elif "uranium:" in line_lower and section != "industry":
            uranium = ISN(line_clean.split("Uranium: ")[1].split(",")[0])
            silicon = ISN(line_clean.split("Silicon: ")[1].split(",")[0])
            beryllium = ISN(line_clean.split("Beryllium: ")[1].split(",")[0])
            hydrogen = ISN(line_clean.split("Hydrogen: ")[1].split(",")[0])
            plutonium = ISN(line_clean.split("Plutonium: ")[1].split(",")[0])
            radium = ISN(line_clean.split("Radium: ")[1].split(",")[0])
            mythril = ISN(line_clean.split("Mythril: ")[1].strip())
        elif "has:" in line_lower:
            has = line_clean.split("Has: ")[1].split(", ")
        elif "mining level:" in line_lower and "boosts" not in line_lower:
            if "(x" not in line_lower:
                miningLevel = ISN(line_clean.split(": ")[1])

        # --- BOOST MODIFIERS ---
        elif "research:" in line_lower and "(+" in line_lower:
            if boost_context == "farming":
                researchFarmingBoost = ISN(line_clean.split("(+")[1].split("%")[0])
            elif boost_context == "ore":
                researchOreBoost = ISN(line_clean.split("(+")[1].split("%")[0])
            elif boost_context == "research":
                researchResearchBoost = ISN(line_clean.split("(+")[1].split("%")[0])
            elif boost_context == "govt":
                researchGovtBoost = ISN(line_clean.split("(+")[1].split("%")[0])
        elif "focus:" in line_lower and "(+" in line_lower:
            if boost_context == "farming":
                focusFarmingBoost = ISN(line_clean.split("(+")[1].split("%")[0])
            elif boost_context == "ore":
                focusOreBoost = ISN(line_clean.split("(+")[1].split("%")[0])
            elif boost_context == "research":
                focusResearchBoost = ISN(line_clean.split("(+")[1].split("%")[0])
            elif boost_context == "govt":
                focusGovtBoost = ISN(line_clean.split("(+")[1].split("%")[0])
        elif "furnace level:" in line_lower:
            if boost_context == "farming":
                furnaceFarmingBoost = ISN(line_clean.split("(+")[1].split("%")[0])
            elif boost_context == "ore":
                furnaceLeveOrelBoost = ISN(line_clean.split("x")[1].split(")")[0])
            elif boost_context == "research":
                furnaceResearchBoost = ISN(line_clean.split("x")[1].split(")")[0])
            elif section == "industry":
                furnaceLevel = ISN(line_clean.split(": ")[1])
        elif (
            "mining level:" in line_lower
            and "x" in line_lower
            and boost_context == "ore"
        ):
            MiningLevelOreBoost = ISN(line_clean.split("x")[1].split(")")[0])
        elif "scientists:" in line_lower and boost_context == "research":
            scientistResearchBoost = ISN(line_clean.split("x")[1].split(")")[0])

        # --- GOVERNMENT ---
        elif "current educated government employees:" in line_lower:
            currentEducatedGovernmentEmployees = ISN(line_clean.split(": ")[1])
        elif "current uneducated government employees:" in line_lower:
            currentUneducatedGovernmentEmployees = ISN(line_clean.split(": ")[1])
        elif "influence per educated employee:" in line_lower:
            influencePerEducatedEmployee = ISN(line_clean.split(": ")[1])
        elif "influence per uneducated employee:" in line_lower:
            influencePerUneducatedEmployee = ISN(line_clean.split(": ")[1])

        # --- INDUSTRY CRAFTING ---
        elif "bronze:" in line_lower:
            bronzeCrafting = ISN(line_clean.split(": ")[1].split(" (")[0])
        elif "gunpowder:" in line_lower:
            gunpowderCrafting = ISN(line_clean.split(": ")[1].split(" (")[0])
        elif "steel:" in line_lower:
            steelCrafting = ISN(line_clean.split(": ")[1].split(" (")[0])
        elif "gear:" in line_lower:
            gearCraftung = ISN(line_clean.split(": ")[1].split(" (")[0])
        elif "steam engine:" in line_lower:
            steamEngine = ISN(line_clean.split(": ")[1].split(" (")[0])
        elif "bora:" in line_lower:
            bora = ISN(line_clean.split(": ")[1].split(" (")[0])
        elif "tractors:" in line_lower:
            tractors = ISN(line_clean.split(": ")[1].split(" (")[0])

        # --- RESEARCH ARRAY ---
        elif "research: [" in line_lower:
            research = line_clean.split("[")[1].split("]")[0].split(",")
            research = [1 if x.strip() == "1" else 0 for x in research]

        elif "farming nerf" in line_lower and section == "militaryStuff":
            farmingWarNerf = ISN(line_clean.split("%")[0].strip("-"))
        elif section == "militaryCopy" and not ("weapons:" in line_lower):
            militaryCopy += "\n" + line_clean

    # test zone end

    # on to calculating the next round

    # calculate research
    educationPercent = (
        (0.5 * research[12])
        + (0.25 * research[16])
        + (0.25 * research[23])
        + (1 * research[44])
        + (1.5 * research[58])
    )
    researchFarmingBoost = (
        (5 * research[0])
        + (5 * research[8])
        + (5 * research[10])
        + (5 * research[15])
        + (10 * research[22])
        + (20 * research[26])
        + (15 * research[33])
        + (50 * research[39])
        + (25 * research[52])
        + (5 * research[61])
    )
    researchOreBoost = (
        (10 * research[7])
        + (10 * research[13])
        + (5 * research[17])
        + (15 * research[30])
        + (10 * research[34])
        + (15 * research[43])
        + (20 * research[53])
    )
    researchGovtBoost = (
        (15 * research[9])
        + (15 * research[14])
        + (50 * research[31])
        + (10 * research[56])
    )
    researchResearchBoost = (
        (15 * research[9])
        + (10 * research[11])
        + (15 * research[24])
        + (10 * research[35])
        + (35 * research[55])
    )

    # citHap and citAng
    citHapGain = -math.floor(tax / 5) + 2
    citHap += citHapGain + citHapGain2

    # calculate government stats
    neededInfluence = furnaceLevel * (
        uneducatedCount + (10 * educatedCount) + (3 * militaryCount)
    )
    influencePerUneducatedEmployee = (
        100 * (1 + (focusGovtBoost / 100)) * (1 + (researchGovtBoost / 100))
    )
    influencePerEducatedEmployee = influencePerUneducatedEmployee * 15
    influenceGain = (uneducatedGovt * influencePerUneducatedEmployee) + (
        educatedGovt * influencePerEducatedEmployee
    )
    if neededInfluence != 0:
        influenceGradient = influenceGain / neededInfluence
        if influenceGradient > 8:
            govtNerf = 1.2
        elif influenceGradient > 4:
            govtNerf = 1.1
        elif influenceGradient > 1:
            govtNerf = 1
        elif influenceGradient > 0.9:
            govtNerf = 0.9
        else:
            govtNerf = 0.6
    else:
        govtNerf = 1

    # food calculation
    foodperperson = (
        (
            2
            * (1 + (researchFarmingBoost / 100))
            * (1 + (focusFarmingBoost / 100))
            * (1 + (furnaceLevel / 5))
        )
        * (1 - (farmingWarNerf / 100))
        * (1 - (droughtNerf / 100))
    )
    foodGain = round(
        govtNerf * foodperperson * (uneducatedFarmer + educatedFarmer + militaryFarmer)
    )
    neededFood = population + childCount
    if neededFood > foodGain:
        foodEconomy = foodGain
        if foodGain + food < neededFood:
            foodDebt = neededFood - (food + foodGain)
            food = 0
            children_to_starve = min(math.ceil(foodDebt / 2), childCount)
            childCount -= children_to_starve
            population -= children_to_starve
            foodDebt -= children_to_starve * 2
            citHap -= 3
            if foodDebt > 0:
                uneducated_to_starve = min(int(foodDebt), uneducatedCount)
                uneducatedCount -= uneducated_to_starve
                population -= uneducated_to_starve
                foodDebt -= uneducated_to_starve
                citHap -= 3
            if foodDebt > 0:
                educated_to_starve = min(int(foodDebt), educatedCount)
                educatedCount -= educated_to_starve
                population -= educated_to_starve
                foodDebt -= educated_to_starve
                citHap -= 4
            if foodDebt > 0:
                military_to_starve = min(int(foodDebt), militaryCount)
                militaryCount -= military_to_starve
                population -= military_to_starve
                foodDebt -= military_to_starve
                citHap -= 5
        else:
            food = (food * foodRetention / 100) - neededFood + foodGain
    else:
        foodEconomy = neededFood
        food = (food * foodRetention / 100) - neededFood + foodGain
    foodExcess = foodGain - neededFood

    # drought stuff
    if droughtDuration > 1:
        droughtDuration -= 1
    elif droughtDuration == 1:
        droughtDuration = 0
        droughtPower = 0
        droughtNerf = 0
    elif random.random() <= ((droughtPower**2) / 1000):
        droughtDuration = stochasticRound(math.sqrt(droughtPower))
        droughtNerf = stochasticRound(droughtPower)
        droughtPower = 0
        print("drought has started for " + name)
    else:
        droughtPower += 1

    # economy stuff
    gold += (
        govtNerf
        * gpc
        * (tax / 100)
        * foodEconomy
        * round(1.1**furnaceLevel + 0.1 * furnaceLevel, 2)
    )
    goldOre += goldOreGain
    gold -= gpc * 0.1 * (uneducatedFarmer + educatedFarmer + militaryFarmer)
    gold -= gpc * 0.2 * (uneducatedMiner + educatedMiner + militaryMiner)
    gold -= gpc * 0.5 * (militarySoldiers)
    gold -= gpc * 1.5 * (uneducatedGovt + educatedGovt)
    gold -= gpc * 2.5 * educatedScientist
    gold = round(gold, 2)
    if gold <= 0:
        citHap -= 3

    # population
    temp = childCount
    childCount = math.floor(childCount * 0.8)
    uneducatedCount += math.floor((temp - childCount) * (1 - educationPercent / 100))
    educatedCount += math.ceil((temp - childCount) * (educationPercent / 100))
    childCount += popGain * (1 + popBoost / 100)
    population += popGain * (1 + popBoost / 100)
    popGain += popGain2 * (1 + popBoost / 100)
    temp = distribute_population(
        [uneducatedFarmer, uneducatedMiner, uneducatedGovt], uneducatedCount
    )
    uneducatedFarmer = temp[0]
    uneducatedMiner = temp[1]
    uneducatedGovt = temp[2]
    temp = distribute_population(
        [educatedFarmer, educatedMiner, educatedGovt, educatedScientist], educatedCount
    )
    educatedFarmer = temp[0]
    educatedMiner = temp[1]
    educatedGovt = temp[2]
    educatedScientist = temp[3]
    temp = distribute_population(
        [militaryFarmer, militaryMiner, militarySoldiers], militaryCount
    )
    militaryFarmer = temp[0]
    militaryMiner = temp[1]
    militarySoldiers = temp[2]

    # Mining stuff
    MiningLevelOreBoost = 1.15**miningLevel
    furnaceLeveOrelBoost = 2.5**furnaceLevel
    globalFurnaceBoost = 1.3 ** (
        (max(globalFurnaceLevel, furnaceLevel + 1)) - furnaceLevel - 1
    )
    oreGain = (
        govtNerf
        * ((uneducatedMiner + educatedMiner + militaryMiner) / 12)
        * MiningLevelOreBoost
        * furnaceLeveOrelBoost
        * globalFurnaceBoost
        * (1 + focusOreBoost / 100)
        * (1 + researchOreBoost / 100)
    )
    coal = doOreGain(coal, 1, 1, miningLevel, oreGain, has.__contains__("Coal"))
    iron = doOreGain(iron, 1, 1, miningLevel, oreGain, has.__contains__("Iron"))
    copper = doOreGain(copper, 1, 1, miningLevel, oreGain, has.__contains__("Copper"))
    tin = doOreGain(tin, 1, 1, miningLevel, oreGain, has.__contains__("Tin"))
    salt = doOreGain(salt, 1, 1, miningLevel, oreGain, has.__contains__("Salt"))
    sulphur = doOreGain(
        sulphur, 100, 1, miningLevel, oreGain, has.__contains__("Sulphur")
    )
    titanium = doOreGain(
        titanium, 5, 2, miningLevel, oreGain, has.__contains__("Titanium")
    )
    cobalt = doOreGain(cobalt, 1, 2, miningLevel, oreGain, has.__contains__("Cobalt"))
    tungsten = doOreGain(
        tungsten, 100, 2, miningLevel, oreGain, has.__contains__("Tungsten")
    )
    oil = doOreGain(oil, 10, 2, miningLevel, oreGain, has.__contains__("Oil"))
    magnesium = doOreGain(
        magnesium, 1, 2, miningLevel, oreGain, has.__contains__("Magnesium")
    )
    uranium = doOreGain(
        uranium, 10000, 3, miningLevel, oreGain, has.__contains__("Uranium")
    )
    hydrogen = doOreGain(
        hydrogen, 1000, 3, miningLevel, oreGain, has.__contains__("Hydrogen")
    )
    radium = doOreGain(
        radium, 10000, 3, miningLevel, oreGain, has.__contains__("Radium")
    )
    beryllium = doOreGain(
        beryllium, 1000, 3, miningLevel, oreGain, has.__contains__("Beryllium")
    )
    plutonium = doOreGain(
        plutonium, 100000, 3, miningLevel, oreGain, has.__contains__("Plutonium")
    )
    mythril = doOreGain(
        mythril, 1000000, 3, miningLevel, oreGain, has.__contains__("Mythril")
    )
    domininglevel = input("max mining level for " + name + "?:")
    if domininglevel == "end":
        sys.exit("You said end")
    oldml = miningLevel
    if domininglevel == "1":
        if has.__contains__("Titanium"):
            MLstats = calculate(1, titanium, tin, int(miningLevel))
            titanium = MLstats[0]
            tin = MLstats[1]
            miningLevel = MLstats[2]
        else:
            MLstats = calculate(2, iron, tin, int(miningLevel))
            iron = MLstats[0]
            tin = MLstats[1]
            miningLevel = MLstats[2]
    temp = handleFL(furnaceLevel, iron, bronzeCrafting, coal, salt, steelCrafting)
    furnaceLevel = temp[0]
    furnaceReq = returnFLRequirements(furnaceLevel)
    iron = temp[1]
    bronzeCrafting = temp[2]
    coal = temp[3]
    salt = temp[4]
    steel = temp[5]

    goldBuff = ((govtNerf * round(1.1**furnaceLevel + 0.1 * furnaceLevel, 2)) - 1) / 100

    cWLF = 0
    cWKF = 1
    if citHap <= 50:
        civilWar = True
        cWLF = min(2 * (50 - citHap), 90) / 100
        cWKF = 1 - cWLF
        citHap = round(66 + citHap * 34)

    final_output = f"""{name}:
Country focus: {focus}
Gold: {SN(round(gold*cWKF,2))}, Gold ore: {goldOre} (+{goldOreGain}), Buff/Nerf: +{goldBuff}%
Gold per capita: {SN(gpc)}, Tax: {tax}%
Population Stats:
    Population: {SNS(cWF(childCount,cWKF)+cWF(uneducatedFarmer,cWKF)+cWF(uneducatedMiner,cWKF)+cWF(uneducatedGovt,cWKF)+cWF(educatedFarmer,cWKF)+cWF(educatedMiner,cWKF)+cWF(educatedGovt,cWKF)+cWF(educatedScientist,cWKF)+cWF(militaryFarmer,cWKF)+cWF(militaryMiner,cWKF)+cWF(militarySoldiers,cWKF))} (+{cWF(popGain,cWKF)}) (+{cWF(popGain2,cWKF)}/t2) (+{popBoost}%) (t2 cost: 50)
    Citizen happiness: {citHap} (+{citHapGain}) (+{citHapGain2})
    Citizen anger: {citAng} (+{citAngGain}) (/{citAngDiv})
Education Type:
    {cWF(childCount,cWKF)} Child
    {cWF(uneducatedFarmer,cWKF)+cWF(uneducatedMiner,cWKF)+cWF(uneducatedGovt,cWKF)} Uneducated
    {cWF(educatedFarmer,cWKF)+cWF(educatedMiner,cWKF)+cWF(educatedGovt,cWKF)+cWF(educatedScientist,cWKF)} Educated
    {cWF(militaryFarmer,cWKF)+cWF(militaryMiner,cWKF)+cWF(militarySoldiers,cWKF)} Military
Uneducated Occupation:
    {cWF(uneducatedFarmer,cWKF)} Farmer, Recommended: {math.ceil((2*cWF(childCount,cWKF)+cWF(uneducatedFarmer,cWKF)+cWF(uneducatedMiner,cWKF)+cWF(uneducatedGovt,cWKF)+cWF(educatedFarmer,cWKF)+cWF(educatedMiner,cWKF)+cWF(educatedGovt,cWKF)+cWF(educatedScientist,cWKF)+cWF(militaryFarmer,cWKF)+cWF(militaryMiner,cWKF)+cWF(militarySoldiers,cWKF))/(foodperperson*0.95))}
    {cWF(uneducatedMiner,cWKF)} Miner
    {cWF(uneducatedGovt,cWKF)} Govt
Educated occupation:
    {cWF(educatedFarmer,cWKF)} Farmer
    {cWF(educatedMiner,cWKF)} Miner
    {cWF(educatedGovt,cWKF)} Govt
    {cWF(educatedScientist,cWKF)} Scientist
Military Occupation:
    {cWF(militaryFarmer,cWKF)} Farmer
    {cWF(militaryMiner,cWKF)} Miner
    {cWF(militarySoldiers,cWKF)} Solders
Food:
    {cWF(food,cWKF)} (+{foodExcess} Excess per year)
    {foodRetention}% retention
    Farming Boosts:
        Research: (+{researchFarmingBoost}%)
        Focus: (+{focusFarmingBoost}%)
        Furnace Level: (+{furnaceFarmingBoost}%)
    Drought:
        Drought Power: {droughtPower}
        Drought Nerf: {droughtNerf}%
        Drought Duration: {droughtDuration}
Ore:
    -Teir 1 ores-
    Coal: {SN(cWF(coal,cWKF))}, Iron: {SN(cWF(iron,cWKF))}, Copper: {SN(cWF(copper,cWKF))}, Tin: {SN(cWF(tin,cWKF))}, Salt: {SN(cWF(salt,cWKF))}, Sulphur: {SN(cWF(sulphur,cWKF))}
    -Teir 2 ores-
    Titanium: {SN(cWF(titanium,cWKF))}, Cobalt: {SN(cWF(cobalt,cWKF))}, Tungsten: {SN(cWF(tungsten,cWKF))}, Oil: {SN(cWF(oil,cWKF))}, Magnesium: {SN(cWF(magnesium,cWKF))}
    -Teir 3 ores-
    Uranium: {SN(cWF(uranium,cWKF))}, Silicon: {SN(cWF(silicon,cWKF))}, Beryllium: {SN(cWF(beryllium,cWKF))}, Hydrogen: {SN(cWF(hydrogen,cWKF))}, Plutonium: {SN(cWF(plutonium,cWKF))}, Radium: {SN(cWF(radium,cWKF))}, Mythril: {SN(cWF(mythril,cWKF))}
    Has: {", ".join(has)}
    Mining Level: {miningLevel}
    Ore Boosts:
        Research: (+{researchOreBoost}%)
        Focus: (+{focusOreBoost}%)
        Mining Level: (x{MiningLevelOreBoost})
        Furnace Level: (x{furnaceLeveOrelBoost})
Research Boosts:
    Research: (+{researchResearchBoost}%)
    Focus: (+{focusResearchBoost}%)
    Furnace level: (x{furnaceResearchBoost})
    Scientists: (x{scientistResearchBoost})
Government:
    Needed influence: {neededInfluence} ({furnaceLevel}*(1*{SN(cWF(uneducatedFarmer,cWKF)+cWF(uneducatedMiner,cWKF)+cWF(uneducatedGovt,cWKF))}+10*{SN(cWF(educatedFarmer,cWKF)+cWF(educatedMiner,cWKF)+cWF(educatedGovt,cWKF)+cWF(educatedScientist,cWKF))}+3*{SN(cWF(militaryFarmer,cWKF)+cWF(militaryMiner,cWKF)+cWF(militarySoldiers,cWKF))}))
    Current educated government employees: {cWF(educatedGovt,cWKF)}
    Current uneducated government employees: {cWF(uneducatedGovt,cWKF)}
    Influence per educated employee: {influencePerEducatedEmployee}
    Influence per uneducated employee: {influencePerUneducatedEmployee}
    Influence boosts:
        Research: (+{researchGovtBoost}%)
        Focus: (+{focusGovtBoost}%)
    Government influence is multiplying food, ore, money from tax, and research by x{govtNerf}
Industry:
    Furnace Level: {furnaceLevel}
    Furnace req: ({furnaceReq})
    -Material Crafting-
    Bronze: {bronzeCrafting} (needs 1 copper and 1 tin for 1)
    Gunpowder: {gunpowderCrafting} (needs 1 sulphur and 1 coal for 1)     {crafting_tab(steel, gearCrafting, steamEngine, bora, tractors, furnaceLevel, research)}
Research: {str(research).replace(' ', '')}
Military:
    War:
        -{farmingWarNerf}% Farming Nerf
    Weapons:
        {militaryCopy.strip()}"""

    if civilWar:
        final_output += "\n\n\n" + f"""Rebelion of {name}:
Country focus: {focus}
Gold: {SN(round(gold*cWLF,2))}, Gold ore: {goldOre} (+{goldOreGain}), Buff/Nerf: +{goldBuff}%
Gold per capita: {SN(gpc)}, Tax: {tax}%
Population Stats:
    Population: {SNS(cWF(childCount,cWLF)+cWF(uneducatedFarmer,cWLF)+cWF(uneducatedMiner,cWLF)+cWF(uneducatedGovt,cWLF)+cWF(educatedFarmer,cWLF)+cWF(educatedMiner,cWLF)+cWF(educatedGovt,cWLF)+cWF(educatedScientist,cWLF)+cWF(militaryFarmer,cWLF)+cWF(militaryMiner,cWLF)+cWF(militarySoldiers,cWLF))} (+{cWF(popGain,cWLF)}) (+{cWF(popGain2,cWLF)}/t2) (+{popBoost}%) (t2 cost: 50)
    Citizen happiness: 100 (+{citHapGain}) (+{citHapGain2})
    Citizen anger: {citAng} (+{citAngGain}) (/{citAngDiv})
Education Type:
    {cWF(childCount,cWLF)} Child
    {cWF(uneducatedFarmer,cWLF)+cWF(uneducatedMiner,cWLF)+cWF(uneducatedGovt,cWLF)} Uneducated
    {cWF(educatedFarmer,cWLF)+cWF(educatedMiner,cWLF)+cWF(educatedGovt,cWLF)+cWF(educatedScientist,cWLF)} Educated
    {cWF(militaryFarmer,cWLF)+cWF(militaryMiner,cWLF)+cWF(militarySoldiers,cWLF)} Military
Uneducated Occupation:
    {cWF(uneducatedFarmer,cWLF)} Farmer, Recommended: {math.ceil((2*cWF(childCount,cWLF)+cWF(uneducatedFarmer,cWLF)+cWF(uneducatedMiner,cWLF)+cWF(uneducatedGovt,cWLF)+cWF(educatedFarmer,cWLF)+cWF(educatedMiner,cWLF)+cWF(educatedGovt,cWLF)+cWF(educatedScientist,cWLF)+cWF(militaryFarmer,cWLF)+cWF(militaryMiner,cWLF)+cWF(militarySoldiers,cWLF))/(foodperperson*0.95))}
    {cWF(uneducatedMiner,cWLF)} Miner
    {cWF(uneducatedGovt,cWLF)} Govt
Educated occupation:
    {cWF(educatedFarmer,cWLF)} Farmer
    {cWF(educatedMiner,cWLF)} Miner
    {cWF(educatedGovt,cWLF)} Govt
    {cWF(educatedScientist,cWLF)} Scientist
Military Occupation:
    {cWF(militaryFarmer,cWLF)} Farmer
    {cWF(militaryMiner,cWLF)} Miner
    {cWF(militarySoldiers,cWLF)} Solders
Food:
    {cWF(food,cWLF)} (+{foodExcess} Excess per year)
    {foodRetention}% retention
    Farming Boosts:
        Research: (+{researchFarmingBoost}%)
        Focus: (+{focusFarmingBoost}%)
        Furnace Level: (+{furnaceFarmingBoost}%)
    Drought:
        Drought Power: {droughtPower}
        Drought Nerf: {droughtNerf}%
        Drought Duration: {droughtDuration}
Ore:
    -Teir 1 ores-
    Coal: {SN(cWF(coal,cWLF))}, Iron: {SN(cWF(iron,cWLF))}, Copper: {SN(cWF(copper,cWLF))}, Tin: {SN(cWF(tin,cWLF))}, Salt: {SN(cWF(salt,cWLF))}, Sulphur: {SN(cWF(sulphur,cWLF))}
    -Teir 2 ores-
    Titanium: {SN(cWF(titanium,cWLF))}, Cobalt: {SN(cWF(cobalt,cWLF))}, Tungsten: {SN(cWF(tungsten,cWLF))}, Oil: {SN(cWF(oil,cWLF))}, Magnesium: {SN(cWF(magnesium,cWLF))}
    -Teir 3 ores-
    Uranium: {SN(cWF(uranium,cWLF))}, Silicon: {SN(cWF(silicon,cWLF))}, Beryllium: {SN(cWF(beryllium,cWLF))}, Hydrogen: {SN(cWF(hydrogen,cWLF))}, Plutonium: {SN(cWF(plutonium,cWLF))}, Radium: {SN(cWF(radium,cWLF))}, Mythril: {SN(cWF(mythril,cWLF))}
    Has: {", ".join(has)}
    Mining Level: {miningLevel}
    Ore Boosts:
        Research: (+{researchOreBoost}%)
        Focus: (+{focusOreBoost}%)
        Mining Level: (x{MiningLevelOreBoost})
        Furnace Level: (x{furnaceLeveOrelBoost})
Research Boosts:
    Research: (+{researchResearchBoost}%)
    Focus: (+{focusResearchBoost}%)
    Furnace level: (x{furnaceResearchBoost})
    Scientists: (x{scientistResearchBoost})
Government:
    Needed influence: {neededInfluence} ({furnaceLevel}*(1*{SN(cWF(uneducatedFarmer,cWLF)+cWF(uneducatedMiner,cWLF)+cWF(uneducatedGovt,cWLF))}+10*{SN(cWF(educatedFarmer,cWLF)+cWF(educatedMiner,cWLF)+cWF(educatedGovt,cWLF)+cWF(educatedScientist,cWLF))}+3*{SN(cWF(militaryFarmer,cWLF)+cWF(militaryMiner,cWLF)+cWF(militarySoldiers,cWLF))}))
    Current educated government employees: {cWF(educatedGovt,cWLF)}
    Current uneducated government employees: {cWF(uneducatedGovt,cWLF)}
    Influence per educated employee: {influencePerEducatedEmployee}
    Influence per uneducated employee: {influencePerUneducatedEmployee}
    Influence boosts:
        Research: (+{researchGovtBoost}%)
        Focus: (+{focusGovtBoost}%)
    Government influence is multiplying food, ore, money from tax, and research by x{govtNerf}
Industry:
    Furnace Level: {furnaceLevel}
    Furnace req: ({furnaceReq})
    -Material Crafting-
    Bronze: {bronzeCrafting} (needs 1 copper and 1 tin for 1)
    Gunpowder: {gunpowderCrafting} (needs 1 sulphur and 1 coal for 1)     {crafting_tab(steel, gearCrafting, steamEngine, bora, tractors, furnaceLevel, research)}
Research: {str(research).replace(' ', '')}
Military:
    War:
        -{farmingWarNerf}% Farming Nerf
    Weapons:
        {militaryCopy.strip()}"""
    all_nations_output.append(final_output)


combined_text = "\n\n\n".join(all_nations_output)

# 4. Overwrite output.txt with the entire combined block
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(combined_text)
