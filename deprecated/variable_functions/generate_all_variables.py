import pandas as pd
from generate_demographic_variables import generate_demographic
from generate_economic_variables import generate_economic
from generate_family_variables import generate_family
from generate_geographical_variables import generate_geographical
from generate_work_variables import generate_work

def generate_person(sample_year=2019, utbildning=""):
    data2 = pd.DataFrame(columns=[  'PersonNr', 'Lan', 'Kommun', 'Forsamling', 'Distriktskod', 'FastLopNr', 'FastBet',
                                    'Barn0_3', 'Barn4_6', 'Barn7_10', 'Barn11_15', 'Barn16_17',
                                    'Barn18plus', 'Barn18_19', 'Barn20plus', 'FamId', 
                                    'Sun2000niva_old','SUN2000niva', 'SUN2000Inr', 'SUN2000Grp',
                                    'CfarNr_LISA', 'ArbstId', 'AstNr_LISA', 'AstKommun', 'AstLan',
                                    'KU1PeOrgNr', 'KU1CfarNr', 'KU1AstNr', 'KU1AstKommun', 'KU1AstLan',
                                    'KU1YrkStalln', 'KU2PeOrgNr', 'KU2CfarNr', 'KU2AstNr', 'KU2AstKommun',
                                    'KU2AstLan', 'KU2YrkStalln', 'KU3PeOrgNr', 'KU3CfarNr', 'KU3AstNr',
                                    'KU3AstKommun', 'KU3AstLan', 'KU3YrkStalln',
                                    'FodelseAr', 'DodDatum', 'Alder', 'Kon', 'InvUtvLand', 'InvUtvManad',
                                    'PostTyp', 'FodelseLandnamn', 'FodelseTidMor', 'FodelseLandnamnMor',
                                    'FodelseTidFar', 'FodelseLandnamnFar', 'UtlSvBakg',
                                    'SyssStat', 'ArbTid', 'YrkStalln', 'KU1lnk', 'KU2lnk', 'KU3lnk',
                                    'Raks_SummaInk', 'Raks_Huvudanknytning', 'Raks_EtablGrad', 'Raks_Forvink'
                                 ])
    
    family = generate_family(sample_year, utbildning)
    Geographical = generate_geographical()
    Lan = Geographical.loc[0, 'Lan']
    data2 = []

    for i, row in family.iterrows():
        PersonNr = row['PersonNr']
        row = pd.DataFrame({row.name : row})
        Family = row.transpose()

        Demographic = generate_demographic(PersonNr)
        Economic = generate_economic(1, sample_year)

        income = [Economic.loc[0, 'KU1lnk'], Economic.loc[0, 'KU2lnk'], Economic.loc[0, 'KU3lnk']]
        yrks = Economic.loc[0, 'YrkStalln']
        Work = generate_work(PersonNr, Lan, income, yrks)
        t = pd.DataFrame()
        t = pd.concat([Family, Geographical, Demographic, Economic, Work], axis=1)
        data2.append(t)
    data3 = pd.concat(data2, ignore_index=True)

    return data3

def generate_data(amount, sample_year=2019): 
    """
    Parameters
    ----------
    amount : integer
        The amount of rows you want to create.
    
    sample_year : integer
        The year you want to pretend it is (different years may create different data).

    Returns
    -------
    data: dataframe
        dataframe with data for all variables.

    """
    utbildning = pd.read_csv("../variable_data/downloaded_data/utbildning_cleaner.csv")
    people = []
    data = pd.DataFrame()
    for _ in range(amount):
        person = generate_person(sample_year, utbildning)
        people.append(person)
    
    data = pd.concat(people)
    data = data.reset_index(drop=True)
    return data

if __name__ == "__main__":
    print("This is the main part of the script")
    a = generate_data(1000)
    print(len(a))

