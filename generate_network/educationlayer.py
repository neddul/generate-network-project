#!/usr/bin/env python
# coding: utf-8

# # Creation of Education Layer

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from collections import defaultdict
from tqdm import tqdm
from tqdm.auto import tqdm
pd.set_option('display.max_columns', None)


# ### Dataset
# ###### Variables: 
# - PersonNr
# - Sun2000niva_old
# - SUN2000niva	
# - SUN2000Inr
# - SUN2000Grp
# - ExamAr
# - ExamKommun

csv_data = ' ' 

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_data)
data.head()


#map variables (if variable names in the dataset have different names)
data.rename(columns={ ' ': 'PersonNr ', 
                      ' ': 'Sun2000niva_old', 
                      ' ': 'SUN2000niva',
                      ' ': 'SUN2000Inr',
                      ' ': 'SUN2000Grp',
                      ' ': 'ExamAr',
                      ' ': 'ExamKommun'},inplace = True)

#split dataset into manageable size (process smaller chunks)
chunk_size = 1000000
chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


# ### Educational Ties:
# ###### Variables: 'PersonNr', 'Sun2000niva_old', 'SUN2000niva', 'SUN2000Inr', 'SUN2000Grp, 'ExamAr' and 'ExamKommun'
#  
# - If two people studied in the same level and field of education, the same specialisation, same graduation year, in the same kommun then they are school mates.


def group_map(data, sample_year=2002): 
    start_time = time.time()
    
    #check year to use SUN2000niva_old or SUN2000niva_new
    if sample_year <= 1999:
        sun_2000_niva = 'Sun2000niva_old'
    else:
        sun_2000_niva = 'SUN2000niva'
    
    #to be changed if missing values are not represented the same in the dataset
    #remove rows where 'Sun2000niva_old', 'SUN2000niva', 'SUN2000Inr', 'SUN2000Grp', 'ExamAr' and 'ExamKommun' are missing (equal to '-')
    data = data[(data[sun_2000_niva] != '-')
                & (data['SUN2000Inr'] != '-') & (data['SUN2000Grp'] != ' ')
               & (data['ExamAr'] != '-') & (data['ExamKommun'] != ' ')]

    #group by the variables and create dictionary mapping to sets of 'PersonNr'
    grouped_persons = defaultdict(set)

    for index, row in data.iterrows():
        key = (row[sun_2000_niva], row['SUN2000Inr'], row['SUN2000Grp'], row['ExamAr'], row['ExamKommun'])
        grouped_persons[key].add(row['PersonNr'])

    end_time = time.time()
    print(f"Time elapsed (group_map): {end_time - start_time:.2f} seconds") 
    return grouped_persons



def school_mates(data):
    
    start_time = time.time()

    school_persons = group_map(data)
    results = []

    #tqdm progress bar
    progress_bar = tqdm(total=len(school_persons), desc='Processing')

    for (sun_niva, sun_inr, sun_grp, exam_ar, exam_kom), persons in school_persons.items():
        #pairs of 'PersonNr' working for same company and branch
        pairs = [(person1, person2) for person1 in persons for person2 in persons if person1 < person2]
        results.extend(pairs)
        progress_bar.update(1)


    progress_bar.close()
    end_time = time.time()


    results_data = pd.DataFrame(results, columns=['Person1', 'Person2'])
    results_data['Connection'] = 'schoolmates'


    print(f"Time elapsed: {end_time - start_time:.2f} seconds") 

    return results_data



results = [school_mates(chunk) for chunk in chunks]
combined_results = pd.concat(results, ignore_index=True)
combined_results

#call the function on chunks of the dataset 
results = [school_mates(chunk) for chunk in chunks]
combined_results = pd.concat(results, ignore_index=True)
csv_file_path = 'educational_ties.csv'
combined_results.to_csv(csv_file_path, index=False)
