import math, sys, random
from assembly import generate_nation_from_focus

FOCUS_DATASET = [
    "Basic", "Science", "Industry", "Farming", "Gold", "Population", "Stability", "Government", "Science^2", "Industry^2", "Farming^2", "Gold^2", "Population^2", "Stability^2", "Government^2", "Everything", "Everything^2", "Singular", "Singular^2"
]
prefixList = ['Omni', 'Szméti', 'Tarna', 'Ukwesabi', 'Alasa', 'Tila', 'Bozi', 'Reta', 'Ujarikani', 'Alven', 'Ŝercante', 'Nova', 'Malno', 'Ŝanceli', 'Taluka', 'Navari', 'Tuso']
suffixList = ['ia', 'ia', 'land', 'stan', 'tero', 'ia', 'land', 'stan', 'ia', 'land', 'stan', 'na', 'ica']
insideBannedList = ['Bozistan (AI)','Szmétia (AI)','Szmétina (AI)','Szmética (AI)']

def generateAINation(outsideBannedList):
    nameprefix = random.choice(prefixList)
    namesuffix = random.choice(suffixList)
    if random.random() < 0.05:
        namesuffix = "-" + random.choice(prefixList) + " Union"
    if namesuffix == 'ia' or namesuffix == 'ica':
        nameprefix = nameprefix[:-1]
    name = nameprefix + namesuffix + " (AI)"
    if insideBannedList.__contains__(name) or outsideBannedList.__contains__(name):
        name = generateAINation()
    focus = random.choice(FOCUS_DATASET)
    if ["Population","Population^2","Everything","Everything^2"].__contains__(focus) and random.random() < 0.65:
        focus = random.choice(FOCUS_DATASET)
    nation = generate_nation_from_focus(name,focus)
    return nation
