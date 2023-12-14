#!/usr/bin/env python
# coding: utf-8

# # Creation of Work Layer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from tqdm.auto import tqdm
pd.set_option('display.max_columns', None)


# ### Dataset
# ###### Variables: 
# - PersonNr
# - ArbstId
# - CfarNr_LISA
# - AstNr_LISA
# - KU1CfarNr
# - ArbTid


csv_data = ' ' 

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_data)
data.head()

#map variables (if variable names in the dataset have different names)
data.rename(columns={ ' ': 'PersonNr ', 
                      ' ': ' ArbstId', 
                      ' ': 'CfarNr_LISA',
                      ' ': 'AstNr_LISA',
                      ' ': 'KU1CfarNr',
                      ' ': 'ArbTid'},inplace = True)


# Start by connecting people using just 'CfarNr'
# - 'CfarNr' gives us all the people who work for the same company.
# - Although this alone cannot be used to determine if people know each other, it may be useful for analysis in later stages e.g. how well certain companies pay...


def same_company(data): #check if people work for the same company

    start_time = time.time()

    #remove rows where 'CfarNr_LISA' is missing (equal to '-')
    data = data[data['CfarNr_LISA'] != '-']

    #dictionary mapping 'CfarNr_LISA' to a set of 'PersonNr'
    company_persons = data.groupby('CfarNr_LISA')['PersonNr'].apply(set).to_dict()

    results = []

    #tqdm progress bar
    progress_bar = tqdm(total=len(company_persons), desc='Processing companies')

    for company, persons in company_persons.items():
        #get pairs of 'PersonNr' working for the same company
        pairs = [(person1, person2) for person1 in persons for person2 in persons if person1 < person2]
        results.extend(pairs)
        #update progress bar
        progress_bar.update(1)


    progress_bar.close()
    end_time = time.time()

    results_data = pd.DataFrame(results, columns=['Person1', 'Person2'])
    results_data['Connection'] = 'works for same company'


    print(f"Time elapsed: {end_time - start_time:.2f} seconds") 
    return results_data


# ### Working Ties Approach 1:
# ###### Variables: 'PersonNr','ArbstId'
# - 'ArbstId' is an identifier which combines 4 variables: 'CfarNr_LISA', 'KU1AstNr', 'AstKommun' and 'KU1PerOrgNr'

def work_mates(data): #check ArbstId
    start_time = time.time()

    #remove rows where 'ArbstId' is missing (equal to '--0000-')
    data = data[data['ArbstId'] != '--0000-']

    #dictionary mapping 'ArbstId' to a set of 'PersonNr'
    persons = data.groupby('ArbstId')['PersonNr'].apply(set).to_dict()

    results = []

    #tqdm progress bar
    progress_bar = tqdm(total=len(persons), desc='Processing')

    for company, persons in persons.items():
        #get pairs of 'PersonNr' with the same ArbstId
        pairs = [(person1, person2) for person1 in persons for person2 in persons if person1 < person2]
        results.extend(pairs)
        #update progress bar
        progress_bar.update(1)


    progress_bar.close()
    


    results_data = pd.DataFrame(results, columns=['Person1', 'Person2'])
    results_data['Connection'] = 'workmates'

    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time:.2f} seconds")


    return results_data

#save results in CSV
results_one = work_mates(data)
csv_file_path = 'working_ties_one.csv'
results_one.to_csv(csv_file_path, index=False)


# ### Working Ties Approach 2:
# ###### Variables: 'PersonNr', 'CfarNr_LISA', 'AstNr_LISA', 'KU1CfarNr' and 'ArbTid'
# - If two people work for the same company (CfarNr_LISA), occupation (AstNr_LISA), spend around the same hours at work (ArbTid) and get their main income from the same company (KU1CfarNr) they are workmates.

def group_map(data):
    #remove rows where 'CfarNr_LISA', 'AstNr_LISA', 'KU1CfarNr', 'ArbTid' are missing (equal to '-')
    data = data[(data['CfarNr_LISA'] != '-') & (data['AstNr_LISA'] != '-') 
                & (data['KU1CfarNr'] != '-') & (data['ArbTid'] != ' ')]

    #group by the variables and create dictionary mapping to sets of 'PersonNr'
    grouped_persons = data.groupby(['CfarNr_LISA', 'KU1CfarNr', 'AstNr_LISA', 'ArbTid'])['PersonNr'].apply(set).to_dict()

    return grouped_persons


# same company, branch, primary source of income, work time and occupation
def workmates(data):
    
    start_time = time.time()

    company_persons = group_map(data)
    results = []

    #tqdm progress bar
    progress_bar = tqdm(total=len(company_persons), desc='Processing')

    for (company, ku_one, work_time, occupation), persons in company_persons.items():
        #pairs of 'PersonNr' working for same company and branch
        pairs = [(person1, person2) for person1 in persons for person2 in persons if person1 < person2]
        results.extend(pairs)
        progress_bar.update(1)


    progress_bar.close()
    end_time = time.time()


    results_data = pd.DataFrame(results, columns=['Person1', 'Person2'])
    results_data['Connection'] = 'workmates'


    print(f"Time elapsed: {end_time - start_time:.2f} seconds") 

    return results_data

results_two = workmates(data)
csv_file_path = 'working_ties_two.csv'
results_two.to_csv(csv_file_path, index=False)

