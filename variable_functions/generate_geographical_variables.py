import random
import pandas as pd
import json
scbinternal_fastlopnr = {}
numbers = [str(x) for x in range(10)]

with open('variable_data/selfmade_dictionaries/county_dict.json', 'r') as json_file:
    counties_with_municipals = json.load(json_file)

with open('variable_data/selfmade_dictionaries/tatorter_in_municipals_dict.json', 'r') as json_file:
    tatorter_in_municipals = json.load(json_file)

with open('variable_data/selfmade_dictionaries/forsamling_dict.json', 'r') as json_file:
    forsamlingar_in_municipals = json.load(json_file)

with open('variable_data/selfmade_dictionaries/district_codes_from_Forsamling_dict.json', 'r') as json_file:
    districtcodes_from_Forsamling = json.load(json_file)


def generate_syntethic_FastBet(municipal_name):
    tatorter = tatorter_in_municipals[municipal_name]
    tatort = tatorter[random.randint(0, len(tatorter)-1)] #Chooses randomly which "Tätort" the person lives in of the ones available to that municipal
    number = str(random.randint(1, 400))
    if random.randint(0, 100) > 30: #It is quite likely that there are numbers followed by the first one
        number += ":" + str(random.randint(1, 400))

    FastBet = f"{municipal_name} {tatort} {number}"
    return FastBet

def generate_synthetic_FastLopNr(FastBet):
    if FastBet in scbinternal_fastlopnr: #If there are people in the same new FastBet then they should have the same FastLopNr as well
        return scbinternal_fastlopnr[FastBet]
    else:
        FastLopNr = "" #If the FastBet does not already exist then we should make a new FastLopNr
        taken_values = scbinternal_fastlopnr.values()
        
        while True:
            for _ in range(5):
                FastLopNr = FastLopNr + numbers[random.randint(0, 9)]
            if FastLopNr not in taken_values: #Making sure we don't make the same FastLopNr for different FastBet
                scbinternal_fastlopnr[FastBet] = FastLopNr
                return FastLopNr

def generate_synthetic_Distriktskod(Forsamling):
    possible_districts = districtcodes_from_Forsamling[Forsamling]
    return possible_districts[random.randint(0, len(possible_districts)-1)]

def generate_county():
    counties = list(counties_with_municipals.keys())
    Lan = counties[random.randint(0, len(counties)-1)] #Chooses a random Lan to begin with
    return Lan

def generate_municipal(Lan):
    municipals = counties_with_municipals[Lan]
    Kommun = municipals[random.randint(0, len(municipals)-1)] #Chooses a random Kommun in that county
    return Kommun

def generate_forsamling(Kommun):
    forsamlingar = forsamlingar_in_municipals[Kommun]
    Forsamling = forsamlingar[random.randint(0, len(forsamlingar)-1)] #Chooses a random municipal in that county
    return Forsamling

def generate_geographical():
    Lan                 = generate_county()
    Kommun              = generate_municipal(Lan)
    Forsamling          = generate_forsamling(Kommun)
    Distriktskod        = generate_synthetic_Distriktskod(Forsamling) #Chooses a random district_code based on the Forsamling
    FastBet             = generate_syntethic_FastBet(Kommun) #Generates a random Fastighetsbeteckning based on municipal and places to live in that municipal
    FastLopNr           = generate_synthetic_FastLopNr(FastBet) #Generates a random FastLopNr that is unique to that FastBet or returns the already existing if the FastBet already exists
    geographical_data   = {
                            'Lan'           : [Lan],
                            'Kommun'        : [Kommun],
                            'Forsamling'    : [Forsamling],
                            'Distriktskod'  : [Distriktskod],
                            'FastLopNr'     : [FastLopNr],
                            'FastBet'       : [FastBet]
                          }
    data = pd.DataFrame.from_dict(geographical_data)
    return data