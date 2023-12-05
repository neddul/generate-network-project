import pandas as pd
from itertools import combinations
from tqdm import tqdm
import sys
import os

from readmulticsv import directory_of_csv_to_df

import cProfile

#small_testdata = pd.read_csv("100k_rows.csv")
#small_testdata = pd.read_csv("pretty_good_family_data.csv")
#def create_inner_family_relationships():

def find_parent_child_relationship(subset, current_year):
    parent_relationships = []
    #also checking for 15, as some 15 year olds have been present in the data

    #probably a more elegant way to do this, but this is to make sure we match parent with a child in a right age group

    #could maybe be stored outside of this
    if current_year == 1990:
        #parents_exist = len(subset[(subset['Barn18plus']>0) | (subset['Barn11_15']>0) |  (subset['Barn16_17'] >0 )  ]) > 0
        age_conditions_parents = [
        ('parents_18plus', subset['Barn18plus'] > 0),
        ('parents11_15', subset['Barn11_15'] > 0),
        ('parents16_17', subset['Barn16_17'] > 0),
        ]
        age_conditions_children = [
        ('children_18plus', subset['Alder'] >= 18),
        ('children11_15', subset['Alder'].between(11, 15)),
        ('children16_17', subset['Alder'].between(16, 17)),
        ]
        
    #add an else if here?
    else: 
        #parents_exist = len(subset[(subset['Barn11_15']>0) |  (subset['Barn16_17'] >0 )  | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )]) > 0
        age_conditions_parents = [
        ('parents11_15', subset['Barn11_15'] > 0),
        ('parents16_17', subset['Barn16_17'] > 0),
        ('parents18_19', subset['Barn18_19'] > 0),
        ('parents_20plus', subset['Barn20plus'] > 0),
        ]
        #children = subset[subset['Alder'] >= 15]
        age_conditions_children = [
        ('children11_15', subset['Alder'].between(11, 15)),
        ('children16_17', subset['Alder'].between(16, 17)),
        ('children18_19', subset['Alder'].between(18, 19)),
        ('children_20plus', subset['Alder'] >= 20),  
        ]
    #children_list = []
    for (_, parent_condition), (_, children_condition) in zip(age_conditions_parents, age_conditions_children):
        parents = subset[parent_condition]
        children = subset[children_condition]

        if not children.empty and not parents.empty:
            for _, parent in parents.iterrows():
                age_difference = parent["Alder"] - children["Alder"]
                eligible_children = children[age_difference > 15]
                if not eligible_children.empty:
                    for _,child in eligible_children.iterrows():
                    # Assuming "Kön" is a column indicating gender
                    #gender = 'mother' if parent['Kön'] == 'female' else 'father'
                        
                        # Create DataFrame for each parent-child relationship
                        child_data = {'personNr1': child["PersonNr"],
                                    'personNr2': parent["PersonNr"],
                                'connection': "child of"}

                        parent_data = {'personNr1': parent["PersonNr"],
                                        'personNr2': child["PersonNr"],
                                        'connection': "parent of"}
                        parent_relationships.extend([child_data, parent_data])
                        
                        #parent_relationships.extend([pd.DataFrame(child_data), pd.DataFrame(parent_data)])
                            #print(eligible_children)
                    if len(eligible_children)>1:
                        personNr2_list = eligible_children['PersonNr'].tolist()
                        personNr2_list = sorted(personNr2_list)
                        if len(personNr2_list) == 2:
                            # If length is 2, create a single row with 'siblings' as the connection
                            row_data = {'personNr1': personNr2_list[0], 'personNr2': personNr2_list[1], 'connection': 'siblings'}
                            parent_relationships.extend([row_data])
                                    
                        elif len(personNr2_list) > 2:
                            # If length is greater than 2, create rows for all combinations
                            for pair in combinations(personNr2_list, 2):
                                row_data = {'personNr1': pair[0], 'personNr2': pair[1], 'connection': 'siblings'}
                                #dfs_to_concat.extend([pd.DataFrame(row_data)])
                                parent_relationships.extend([row_data])


    if not parent_relationships:
        parent_relationships = []

            
    return parent_relationships


def find_relationships(subset, current_connections):
    #should i change approach here? 
    #couple_relationships = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    couple_relationships = []
    selected = subset[['PersonNr', 'Alder']]
    if current_connections:
        current_connections = pd.DataFrame(current_connections)
        connections_exist = True
    else:
        connections_exist = False
    for i in range(len(selected)-1):
        for j in range(i+1, len(selected)):

            person1 = selected.iat[i, 0]
            person2 = selected.iat[j, 0]
            # Calculate age difference
            age_difference = abs(selected.iat[i, 1] - selected.iat[j, 1])
        
            #checking if they might be siblings 

            if connections_exist == True:  
                siblings_possible = (((current_connections['personNr1'] == person1) & (current_connections['personNr2'] == person2) & (current_connections['connection'] == "siblings")) | ((current_connections['personNr1'] == person2) & (current_connections['personNr2'] == person1) & (current_connections['connection'] == "siblings")) ).any()
            else:
                siblings_possible=False
            #add check for amount of children (?)
            if age_difference <= 13 and siblings_possible==False:
                #row_data = pd.DataFrame([{'personNr1':person1 , 'personNr2': person2, 'connection': "partner of"}])
                #couple_relationships = pd.concat([couple_relationships, row_data])
                couple_relationships.append({'personNr1': person1, 'personNr2': person2, 'connection': "partner of"})

       
    return couple_relationships

def find_grandparents_aunts(family_connections):
    
    #make this without warnings --> change append to concat 
    
    grandparents_list = []
    parent_rows = family_connections[family_connections['connection'] == 'parent of']
    sibling_rows = family_connections[family_connections['connection'] == 'siblings']
    for _, parent_row in tqdm(parent_rows.iterrows(), total=len(parent_rows), desc="Finding Grandparents, aunts, uncles"):
        # Find rows where 'Personnr1' in the original dataframe matches 'personNr2' in the current row
        matching_rows = parent_rows[parent_rows['personNr2'] == parent_row['personNr1']]
        
        matching_rows_auntsuncles_1 = sibling_rows[(sibling_rows['personNr2'] == parent_row['personNr1']) ]
        matching_rows_auntsuncles_2 = sibling_rows[(sibling_rows['personNr1'] == parent_row['personNr1'])]
        # Iterate through matching rows and add to the result dataframe

        
        if not matching_rows.empty:
            for _, matching_row in matching_rows.iterrows():

                grandparents_list.extend({
                    'personNr1': matching_row['personNr1'],
                    'personNr2': parent_row['personNr2'],
                    'connection': "grandparent of"
                })
                grandparents_list.extend({
                    'personNr1': parent_row['personNr2'],
                    'personNr2': matching_row['personNr1'],
                    'connection': "grandchild of"
                })
        
        
        if not matching_rows_auntsuncles_1.empty:
            for _, matching_row in matching_rows_auntsuncles_1.iterrows():

        #aunts and uncles

        #issue we dont know if in this case it should be person nr 1 or 2 

                grandparents_list.extend({
                    'personNr1': matching_row['personNr1'],
                    'personNr2': parent_row['personNr2'],
                    'connection': "aunt/uncle of"
                })
                grandparents_list.extend({
                    'personNr1': parent_row['personNr2'],
                    'personNr2': matching_row['personNr1'],
                    'connection': "niece/newphew of"
                })
        if not matching_rows_auntsuncles_2.empty:
            for _, matching_row in matching_rows_auntsuncles_2.iterrows():

        #aunts and uncles

        #issue we dont know if in this case it should be person nr 1 or 2 

                grandparents_list.append({
                    'personNr1': matching_row['personNr2'],
                    'personNr2': parent_row['personNr2'],
                    'connection': "aunt/uncle of"
                })
                grandparents_list.append({
                    'personNr1': parent_row['personNr2'],
                    'personNr2': matching_row['personNr2'],
                    'connection': "niece/newphew of"
                })

    return   grandparents_list
            
    

def find_siblings(family_connections):
    selection = family_connections[family_connections["connection"] == "parent of"]

    # Find all the siblings (people with the same parent)
    siblings = selection.groupby('personNr1')['personNr2'].agg(list).reset_index()
    result_filtered = siblings[siblings['personNr2'].apply(len) > 1]
    
    # Create a list to store DataFrames
    dfs_to_concat = []

    for _, row in result_filtered.iterrows():
        personNr2_list = row['personNr2']
        #sorting to easier find duplicates at the end
        personNr2_list = sorted(personNr2_list)
        # Check the length of the list
        if len(personNr2_list) == 2:
            # If length is 2, create a single row with 'siblings' as the connection
            row_data = pd.DataFrame([{'personNr1': personNr2_list[0], 'personNr2': personNr2_list[1], 'connection': 'siblings'}])
            dfs_to_concat.append(row_data)
        elif len(personNr2_list) > 2:
            # If length is greater than 2, create rows for all combinations
            for pair in combinations(personNr2_list, 2):
                #maybe always put younger one first --> to not needing to resort at the end to not have duplicates
                row_data = pd.DataFrame([{'personNr1': pair[0], 'personNr2': pair[1], 'connection': 'siblings'}])
                dfs_to_concat.append(row_data)
    
    #drop rows which are the same
    if dfs_to_concat:
        dfs_to_concat = pd.concat(dfs_to_concat).drop_duplicates(ignore_index=True)
    
    
    return dfs_to_concat

def find_cousins(family_connections):
    #cousines= pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    cousins = []
    aunt_uncle_rows = family_connections[family_connections['connection'] == 'aunt/uncle of']
    parent_rows = family_connections[family_connections['connection'] == 'parent of']
    
    aunt_uncle_rows = aunt_uncle_rows.reset_index(drop=True)
    parent_rows = parent_rows.reset_index(drop=True)
    for _, aunt_uncle_row in tqdm(aunt_uncle_rows.iterrows(), total=len(aunt_uncle_rows), desc="Finding cousins"):
        matching_rows = parent_rows[parent_rows['personNr1'] == aunt_uncle_row['personNr1']]
        
        for _, matching_row in matching_rows.iterrows():

            existing_cousin = cousins[
                ((cousins['personNr1'] == matching_row['personNr2']) & (cousins['personNr2'] == aunt_uncle_row['personNr2'])) |
                ((cousins['personNr1'] == aunt_uncle_row['personNr2']) & (cousins['personNr2'] == matching_row['personNr2']))
            ]
            if existing_cousin.empty:
                cousins.extend({
                    'personNr1': matching_row['personNr2'],
                    'personNr2': aunt_uncle_row['personNr2'],
                    'connection': "cousins"
                }, ignore_index=True)
            
    return cousins

def data_preprocessing(registry_data, save_directory): 
        #fix for column names for now 
    if 'LopNr' in registry_data.columns and 'LopNr_FamId' in registry_data.columns:
        # Create a dictionary for column name mapping
        column_mapping = {'LopNr': 'PersonNr', 'LopNr_FamId': 'FamId'}

        # Use the rename method to rename columns
        registry_data.rename(columns=column_mapping, inplace=True)

    if 'Barn18plus' in registry_data.columns:
        registry_data = registry_data[['FamId','PersonNr', 'Barn18plus', 'Barn11_15', 'Barn16_17', 'Alder' ]]
        current_year = 1990
    else:
        registry_data = registry_data[['FamId','PersonNr', 'Barn11_15', 'Barn16_17', 'Barn18_19', 'Barn20plus', 'Alder' ]]
        current_year = 2005
    

    # Specify the batch size (number of groups in each file)
    batch_size = 30000
    if not os.path.exists(save_directory):

        # Create a new directory because it does not exist
        os.makedirs(save_directory)
    # Iterate through batches and save each batch to a separate file
    grouped_df = registry_data.groupby('FamId')
    batch_number = 0
    for _, batch_data in tqdm(grouped_df, desc="Preprocessing batches"):
        #print(batch_data)
        if len(batch_data)> 1: 
            if batch_number % batch_size == 0:
                # Create a new file for each batch
                file_name = os.path.join(save_directory, f'batch_{batch_number // batch_size}.csv')
                batch_data.to_csv(file_name, index=False)
            else:
                # Append to the existing file for the current batch
                batch_data.to_csv(file_name, mode='a', header=False, index=False)

            batch_number += 1
    
    return current_year



def create_family_layer(registry_data):
    #connections = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    save_directory = 'datastorage_familylayer'
    connections = []
    current_year = data_preprocessing(registry_data, save_directory)
    csv_list = os.listdir(save_directory)
    for filename in tqdm(csv_list, desc="Processing  batches "): 
        file_path = os.path.join(save_directory, filename)
        if os.path.isfile(file_path):
            filtered_data = pd.read_csv(file_path)
            grouped_data = filtered_data.groupby('FamId')
            for _, subset in tqdm(grouped_data, desc="Processing Families"):
                # Filter rows where 'famID' has the current value and reduce data to only the needed columns for this case
                #print(subset)
                #found the line that through the errors 
                #subset = registry_data[registry_data['FamId'] == family]
                # Check if each row has a value greater than or equal to 0 in the 'your_column' column
                #if len(subset)> 1: 
                    #will there be an option to check which year, we are working on

                    #work on child-parent relationship 
                    #parents = subset[(subset['Barn18plus'] > 0) | (subset['Barn16_17'] >0 ) | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )].any(axis=1)
                output = []
                if current_year == 1990:
                    parents_exist = len(subset[(subset['Barn18plus']>0) | (subset['Barn11_15']>0) |  (subset['Barn16_17'] >0 )  ]) > 0
                else:
                    parents_exist = len(subset[(subset['Barn11_15']>0) |  (subset['Barn16_17'] >0 )  | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )]) > 0
                if parents_exist:
                    output = find_parent_child_relationship(subset, current_year)

                    #connections = pd.concat([connections, output])
                    if output: 
                        connections.extend(output)
                #work on the partner relationship --> we are using the output here to reduce the running time
                relationships = find_relationships(subset, output)
                if relationships: 
                    connections.extend(relationships)

            
    connections = pd.DataFrame(connections)
    connections = connections.drop_duplicates()
    #sibling relationship
    #dfs_to_concat = find_siblings(connections)
    #if not dfs_to_concat.empty:
    #    connections = pd.concat([connections] + [dfs_to_concat], ignore_index=True)

    #grandparent/ aunts/uncles / niece .. /cousin relationship

    #can add progress bars here --> but rather quick
    grandparents_connections = find_grandparents_aunts(connections)
    if grandparents_connections:
        grandparents_connections = pd.DataFrame(grandparents_connections, columns=['personNr1', 'personNr2', 'connection'])
        connections = pd.concat([connections] + [grandparents_connections], ignore_index=True)


    cousin_connections = find_cousins(connections)
    if cousin_connections:
        cousin_connections = pd.DataFrame(cousin_connections)
        connections = pd.concat([connections] + [cousin_connections], ignore_index=True)
    

    connections.to_csv('network_full.csv')
    #os.remove(save_directory)
    print("The network was created. Please dont forget to remove the temporal files in datastorage_family, before rerunning the script.")
    return connections


#if len(sys.argv) < 2:
#    print("Missing argument: input file name")
#    sys.exit(-1)
#input_file_name = sys.argv[1]

#data = pd.read_csv(input_file_name)

data = directory_of_csv_to_df(path="multiple_year/synthetic_scb_data_1990")
#data = pd.read_csv("100k_rows.csv")

#needs to be changed to data again to run through command line --> also the year
create_family_layer(data)

#cProfile.run('create_family_layer(data)')



#ideas:

#co parent children together and not the same famId --> need to think of order to calculate 30 years
#do it year by year and update (?) --> how do prevent not recalculating every thing(?) for efficiency
# every following year will take the established connectings from the previous year as input
# are we going to connect back (?)

# 
# extension will need extra code for ex partners /co parent
# but independent functions should work nonetheless --> just way to optimize the famID dependent one with the previous established ones
# then run it reoccurent --> best network will be 1990 or we are going to add time stamps
# which connections can we connect back --> siblings(?), younger children (?), grandparents (?)
# how to deal with data
# test code on more data --> should be something we should be doing soon
# 

#next steps:
# optimizing and correcting code for one year  --> fix mistake on data , double saving of some connections
# expanding code for 30 years

#how to handle death data -> how is it in the real data 
#check edge cases -->


#suggestions Matteo: 

#variable name configuration file
# preprocessing for the possible variables in the year


#optimize --> dont change everything to dataframe all the time --> this works better
# find bottlenecks
# save every other number of connections and then just load at the end all of them together could work as well 

#change everything to a list and then to a dataframe before running the last checks --> easier

#idea read in file, group my famID and save in multiple files as preprocessing 


#then loop through the files and then run the final ones on all connections --> can this list just be tracked completely --> still effieicent