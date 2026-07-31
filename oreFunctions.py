import math, random
from suffixes import SN


def doOreGain(ore, nerf, tier, ML, oregain, has):
    if not ore:
        ore = 0
    if not has:
        if ML >= tier * 15:
            ore += oregain / (nerf * 10)
    else:
        if ML >= (tier-1) * 10:
            ore += oregain / nerf

    return math.floor(ore)


def distribute_population(jobs: list, new_total: int) -> list:
    old_total = sum(jobs)

    if old_total == 0:
        return [0] * len(jobs)

    baselines = []
    remainders = []

    for index, current_pop in enumerate(jobs):
        raw_share = (current_pop / old_total) * new_total
        floor_value = int(raw_share)

        baselines.append(floor_value)
        remainders.append((raw_share - floor_value, index))

    deficit = new_total - sum(baselines)

    remainders.sort(key=lambda item: item[0], reverse=True)

    for i in range(int(deficit)):
        index_to_boost = remainders[i][1]
        baselines[index_to_boost] += 1

    return baselines


def kalkulat(ml1, ml2, r):
    total = 0
    for i in range(ml1, ml2):
        if r == 1:  # tin
            total += 3 * (2**i)
        elif r == 2:  # titanium
            total += 2**i
        elif r == 3:  # iron
            total += 10 * (2**i)
        elif r == 4:  # mythril
            total += math.floor(100 * (1.71**i))
    return total


def calculate(mode, resource, tin, ml):
    finished = False
    if mode == 1:
        if resource - kalkulat(ml, ml, 2) <= 0 or tin - kalkulat(ml, ml, 3) <= 0:
            print("Err:not enough titanium, returning defaults")
            return resource, tin, ml
    elif mode == 2:
        if resource - kalkulat(ml, ml, 3) <= 0 or tin - kalkulat(ml, ml, 3) <= 0:
            print("Err:not enough iron, returning defaults")
            return resource, tin, ml
    x = 5
    while True:
        for i in range(ml, ml + x):
            if mode == 1:  # titanium
                if resource - kalkulat(ml, i, 2) <= 0 or tin - kalkulat(ml, i, 1) <= 0:
                    newML = i - 1
                    lefttin = tin - kalkulat(ml, (i - 1), 1)
                    left = resource - kalkulat(ml, (i - 1), 2)
                    finished = True
                    break
            elif mode == 2:  # Iron
                if resource - kalkulat(ml, i, 3) <= 0 or tin - kalkulat(ml, i, 1) <= 0:
                    newML = i - 1
                    lefttin = tin - kalkulat(ml, (i - 1), 1)
                    left = resource - kalkulat(ml, (i - 1), 3)
                    finished = True
                    break
        if finished:
            break
        x += 1
        if x > 1000:
            exit(code=69420)
    return left, lefttin, newML


furnace_level_requirements = [
    [10000, 1000, 500, 500, 0],
    [35000, 5000, 3000, 2000, 1000]
]
furnace_level_definitions = [
    "Iron",
    "Bronze",
    "Coal",
    "Salt",
    "Steel",
]


def handleFL(FL, curIron, curBronze, curCoal, curSalt, curSteel):
    flr=furnace_level_requirements[FL]
    reqiron = flr[0]
    reqbronze = flr[1]
    reqcoal = flr[2]
    reqsalt = flr[3]
    reqsteel = flr[4]

    if (
        curIron >= reqiron and 
        curBronze >= reqbronze and 
        curCoal >= reqcoal and 
        curSalt >= reqsalt and 
        curSteel >= reqsteel
    ):
        FL += 1
        curIron -= reqiron
        curBronze -= reqbronze
        curCoal -= reqcoal
        curSalt -= reqsalt
        curSteel -= reqsteel
    return [FL, curIron, curBronze, curCoal, curSalt, curSteel]


def returnFLRequirements(FL):
    flr=furnace_level_requirements[FL]
    ret = "("
    i=0
    for ore in flr:
        if ore!=0:
            ret += f"{furnace_level_definitions[i]}: {SN(ore)}, "
        i+=1
    ret.rstrip(", ")
    ret+=")"
    return ret

def stochasticRound(x):
    floor_val = math.floor(x)
    frac_part = x - floor_val
    if random.random() < frac_part:
        return floor_val + 1
    return floor_val

def cWF(n,k):
    return round(n*k)