import pandas as pd
from variable_functions.generate_demographic_variables import generate_demographic
from variable_functions.generate_economic_variables import generate_economic
from variable_functions.generate_family_variables import generate_family
from variable_functions.generate_geographical_variables import generate_geographical
from variable_functions.generate_work_variables import generate_work

def generate_person(sample_year=2019):
    amount = 1
    Geographical = generate_geographical()
    Lan = Geographical.loc[0, 'Lan']

    Family = generate_family(sample_year, amount)
    PersonNr = Family.loc[0, 'PersonNr']

    Economic = generate_economic(amount, sample_year)
    income = [Economic.loc[0, 'KU1lnk'], Economic.loc[0, 'KU2lnk'], Economic.loc[0, 'KU3lnk']]
    yrks = Economic.loc[0, 'YrkStalln']

    Demographic = generate_demographic(PersonNr)
    Work = generate_work(PersonNr, Lan, income, yrks)
    person = pd.concat([Geographical, Family, Economic, Demographic, Work], axis=1)
    return person

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
    data = pd.DataFrame()
    for _ in range(amount):
        person = generate_person(sample_year)
        data = pd.concat([data, person])
    return data