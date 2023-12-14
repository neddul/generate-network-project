import pandas as pd
from itertools import combinations
from tqdm import tqdm
import numpy as np
import sys
import os

pd.options.mode.chained_assignment = None

from readmulticsv import directory_of_csv_to_df

#import cProfile

#small_testdata = pd.read_csv("basictestdata/100k_rows.csv")
#small_testdata = pd.read_csv("basictestdata/pretty_good_family_data.csv")
#def create_inner_family_relationships():

def find_parent_child_relationship(subset, current_year):
    parent_relationships = []
    #also checking for 15, as some 15 year olds have been present in the data

    #probably a more elegant way to do this, but this is to make sure we match parent with a child in a right age group

    #could maybe be stored outside of this
    if current_year <= 2003:
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
                eligible_children = children[(age_difference > 15) & (age_difference < 60)]
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

def find_aunts_uncles(family_connections):
    output1 = pd.DataFrame()
    output2= pd.DataFrame()
    selection_parent = family_connections[family_connections["connection"] == "parent of"]
    selection_sibling = family_connections[family_connections["connection"] == "siblings"]
    
    options1 = selection_parent.merge(selection_sibling, left_on="personNr1", right_on="personNr1", suffixes=('_parent', '_aunt'))
    options2 = selection_parent.merge(selection_sibling, left_on="personNr1", right_on="personNr2", suffixes=('_parent', '_aunt'))
    if not options1.empty:
        aunt_connections = options1[["personNr2_aunt", "personNr2_parent" ]]
        niece_connections = options1[["personNr2_parent", "personNr2_aunt"]]
        #grandparents = grandparents.columns.str.replace('_grandparentside', '').str.replace('_childside', '')
    
        aunt_connections.columns = ['personNr1', 'personNr2']
        niece_connections.columns = ['personNr1', 'personNr2']
        aunt_connections = aunt_connections[aunt_connections['personNr1'] != aunt_connections['personNr2']]
        niece_connections = niece_connections[niece_connections['personNr1'] != niece_connections['personNr2']]

        aunt_connections['connection'] = 'aunt/uncle of'
        niece_connections['connection'] = 'niece/newphew of'
        output1 = pd.concat([aunt_connections] + [niece_connections], ignore_index=True)
    if not options2.empty: 
        aunt_connections = options2[["personNr1_aunt", "personNr2_parent" ]]
        niece_connections = options2[["personNr2_parent", "personNr1_aunt"]]
        #grandparents = grandparents.columns.str.replace('_grandparentside', '').str.replace('_childside', '')
    
        aunt_connections.columns = ['personNr1', 'personNr2']
        niece_connections.columns = ['personNr1', 'personNr2']
        aunt_connections = aunt_connections[aunt_connections['personNr1'] != aunt_connections['personNr2']]
        niece_connections = niece_connections[niece_connections['personNr1'] != niece_connections['personNr2']]


        aunt_connections['connection'] = 'aunt/uncle of'
        niece_connections['connection'] = 'niece/newphew of'
        output2 = pd.concat([aunt_connections] + [niece_connections], ignore_index=True)
    final_output = pd.concat([output1] + [output2], ignore_index=True)
    return final_output

def find_relationships(subset):
    #should i change approach here? 
    #couple_relationships = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    couple_relationships = []
    selected = subset[['PersonNr', 'Alder']]
    selected = selected.sort_values(by="PersonNr")
    #if current_connections:
    #    current_connections = pd.DataFrame(current_connections, columns= ["personNr1", "personNr2", "connection"])
    #    connections_exist = True
    #else:
    #    connections_exist = False


    for i in range(len(selected)-1):
        person1 = selected.iat[i, 0]
        person2 = selected.iat[i+1, 0]

        # Calculate age difference
        age_difference = abs(selected.iat[i, 1] - selected.iat[i+1, 1])
        
            #checking if they might be siblings 

        #if connections_exist == True:  
            #siblings_possible = (((current_connections['personNr1'] == person1) & (current_connections['personNr2'] == person2) & (current_connections['connection'] == "siblings")) | ((current_connections['personNr1'] == person2) & (current_connections['personNr2'] == person1) & (current_connections['connection'] == "siblings")) ).any()
        #else:
        #    siblings_possible=False
            #add check for amount of children (?)
        if age_difference <= 13:
                #row_data = pd.DataFrame([{'personNr1':person1 , 'personNr2': person2, 'connection': "partner of"}])
                #couple_relationships = pd.concat([couple_relationships, row_data])
            row_data = {'personNr1': person1, 'personNr2': person2, 'connection': "partner of"}
            couple_relationships.extend([row_data])

       
    return couple_relationships


def find_grandparents_aunts(family_connections):
    output = pd.DataFrame()
    selection = family_connections[family_connections["connection"] == "parent of"]
    
    grandparents_options = selection.merge(selection, left_on='personNr1', right_on='personNr2', suffixes=('_childside', '_grandparentside'))
    
    grandparents = grandparents_options[["personNr1_grandparentside", "personNr2_childside" ]]
    #grandparents = grandparents.columns.str.replace('_grandparentside', '').str.replace('_childside', '')
    
    grandparents.columns = ['personNr1', 'personNr2']

    # Add a new column 'connection' with the value 'grandparent of'
    grandparents['connection'] = 'grandparent of'
    
    grandchildren =  grandparents_options[["personNr2_childside", "personNr1_grandparentside" ]]
    grandchildren.columns = ['personNr1', 'personNr2']
    grandchildren['connection'] = 'grandchild of'
    
    output = pd.concat([grandchildren] + [grandparents], ignore_index=True)


    return   output
            
    
def find_siblings(family_connections):
    unique_combinations_df = pd.DataFrame()
    selection = family_connections[family_connections["connection"] == "parent of"]
    siblings = selection.merge(selection, how='left', on='personNr1')
    # Find all the siblings (people with the same parent)

    siblings_df = siblings[siblings['personNr2_x'] != siblings['personNr2_y']][['personNr2_x', 'personNr2_y']]

    #unique_combinations_df = siblings_df.drop_duplicates(subset=['personNr2_x', 'personNr2_y'])
    # Convert columns to tuples and drop duplicates
    siblings_df['tuple_key'] = siblings_df[['personNr2_x', 'personNr2_y']].apply(lambda x: tuple(sorted(x)), axis=1)
    unique_combinations_df = siblings_df.drop_duplicates(subset='tuple_key')

    # Drop the temporary column
    #unique_combinations_df = unique_combinations_df.drop(columns=['personNr2_x', 'personNr2_y'])
    #unique_combinations_df['connection'] = 'siblings'

    # Rename columns by removing the suffixes _x and _y
    #unique_combinations_df.columns = unique_combinations_df.columns.str.replace('2_x', '1').str.replace('_y', '')
    final_df = pd.DataFrame(unique_combinations_df['tuple_key'].tolist(), columns=['personNr1', 'personNr2'])

    # Add the 'connection' column
    final_df['connection'] = 'siblings'
    
    return final_df
def find_cousins(family_connections):
    #cousines= pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    output2= pd.DataFrame()
    selection_aunts = family_connections[family_connections["connection"] == "aunt/uncle of"]
    selection_parents = family_connections[family_connections["connection"] == "parent of"]
    
    options = selection_aunts.merge(selection_parents, left_on="personNr1", right_on="personNr1", suffixes=('_aunt', '_parent'))
    cousin_connection=  options[["personNr2_aunt", "personNr2_parent" ]]
    
    cousin_connection['tuple_key'] = cousin_connection[["personNr2_aunt", "personNr2_parent"]].apply(lambda x: tuple(sorted(x)), axis=1)
    cousin_connection = cousin_connection.drop_duplicates(subset='tuple_key')

    cousin_connection = pd.DataFrame(cousin_connection['tuple_key'].tolist(), columns=['personNr1', 'personNr2'])
    #cousin_connection.columns = ['personNr1', 'personNr2']
    cousin_connection['connection'] = 'cousins'

    return cousin_connection


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
    current_year = 1990
    save_directory = 'datastorage_familylayer_onelayer'
    connections = []
    if not os.path.exists(save_directory):

        # Create a new directory because it does not exist
        os.makedirs(save_directory)
        current_year = data_preprocessing(registry_data, save_directory)
        csv_list = os.listdir(save_directory)
    else:
        csv_list = os.listdir(save_directory)
        if len(csv_list)== 0:
    
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
                relationships = find_relationships(subset)
                if relationships: 
                    connections.extend(relationships)

            
    connections = pd.DataFrame(connections)
    connections = connections.drop_duplicates()
    #sibling relationship
    #dfs_to_concat = find_siblings(connections)
    #if not dfs_to_concat.empty:
    #    connections = pd.concat([connections] + [dfs_to_concat], ignore_index=True)

    #grandparent/ aunts/uncles / niece .. /cousin relationship
    print("Saved a partial network now")
    connections.to_csv('network_produced_csvs/Partial_network.csv')
    #can add progress bars here --> but rather quick
    print("Searching possible Grandparents now")
    grandparents_connections = find_grandparents_aunts(connections)
    if not grandparents_connections.empty:
        #grandparents_connections = pd.DataFrame(grandparents_connections, columns=['personNr1', 'personNr2', 'connection'])
        connections = pd.concat([connections] + [grandparents_connections], ignore_index=True)
    print("Searching aunts and uncles now")
    aunts_uncles = find_aunts_uncles(connections)

    if not aunts_uncles.empty:
        connections = pd.concat([connections] + [aunts_uncles], ignore_index=True)
    print("Searching cousins")
    cousin_connections = find_cousins(connections)
    if not cousin_connections.empty:
        #cousin_connections = pd.DataFrame(cousin_connections)
        connections = pd.concat([connections] + [cousin_connections], ignore_index=True)
    connections = connections.drop_duplicates()
    connections = connections[~((connections.duplicated(subset=['personNr1', 'personNr2'])) & (connections['connection'] == 'partner of'))]

    connections.to_csv('network_produced_csvs/network_100k.csv')
    #os.remove(save_directory)
    print("The network was created. Please dont forget to remove the temporal files in datastorage_family, before rerunning the script.")
    return connections


# if len(sys.argv) < 2:
#     print("Missing argument: input file name")
#     sys.exit(-1)
# input_file_name = sys.argv[1]

# data = pd.read_csv(input_file_name)

#data = directory_of_csv_to_df(path="multiple_year/synthetic_scb_data_1990")
#data = pd.read_csv("basictestdata/100k_rows.csv")

#needs to be changed to data again to run through command line --> also the year
create_family_layer(data)

