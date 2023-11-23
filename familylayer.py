import pandas as pd
from itertools import combinations

registry_data_one_year = pd.read_csv("testdatanew.csv")


def find_parent_child_relationship(subset):
    parent_relationships = []

    #this needs to be changed to work with all children variables above 16
    parents = subset[subset['Barn18plus'] > 0]
    children = subset[subset['Alder'] >= 18]
    for _, parent in parents.iterrows():
            age_difference = parent["Alder"] - children["Alder"]
            eligible_children = children[age_difference > 15]
            if not eligible_children.empty:
            
            
            # Assuming "Kön" is a column indicating gender
            #gender = 'mother' if parent['Kön'] == 'female' else 'father'
            
                # Create DataFrame for each parent-child relationship
                child_data = {'personNr1': eligible_children["PersonNr"].tolist(),
                              'personNr2': parent["PersonNr"],
                              'connection': "child of"}

                parent_data = {'personNr1': parent["PersonNr"],
                               'personNr2': eligible_children["PersonNr"].tolist(),
                               'connection': "parent of"}

                parent_relationships.extend([pd.DataFrame(child_data), pd.DataFrame(parent_data)])

    if parent_relationships:
        # Concatenate all DataFrames in the list
        parent_relationships = pd.concat(parent_relationships, ignore_index=True)
    else:
        # Create an empty DataFrame
        parent_relationships = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    return parent_relationships

def find_relationships(subset):
    #should i change approach here? 
    couple_relationships = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    selected = subset[['PersonNr', 'Alder']]
    for i in range(len(selected)-1):
        for j in range(i+1, len(selected)):

            person1 = selected.iat[i, 0]
            person2 = selected.iat[j, 0]
            # Calculate age difference
            age_difference = abs(selected.iat[i, 1] - selected.iat[j, 1])
        
            # Check if age difference is less than or equal to 15 years
            
            
            #add check for amount of children (?)
            if age_difference <= 13:
                row_data = pd.DataFrame([{'personNr1':person1 , 'personNr2': person2, 'connection': "partner of"}])
                couple_relationships = pd.concat([couple_relationships, row_data])
               
    return couple_relationships

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
    dfs_to_concat = pd.concat(dfs_to_concat).drop_duplicates(ignore_index=True)
    
    
    return dfs_to_concat

def create_family_layer(registry_data):
    connections = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    for family in registry_data['famID'].unique():
        # Filter rows where 'famID' has the current value
        subset = registry_data[registry_data['famID'] == family]
        # Check if each row has a value greater than or equal to 0 in the 'your_column' column
        if len(subset)> 1: 
            #will there be an option to check which year, we are working on

            #work on child-parent relationship 
            #parents = subset[(subset['Barn18plus'] > 0) | (subset['Barn16_17'] >0 ) | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )].any(axis=1)
            parents = subset[(subset['Barn18plus']>0) |  (subset['Barn16_17'] >0 )  | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )]
            #print(parents)
            if len(parents)> 1:
                output = find_parent_child_relationship(subset)

                connections = pd.concat([connections, output])

            #work on the partner relationship
            relationships = find_relationships(subset)
            connections = pd.concat([connections, relationships])
            

        
    #sibling relationship
    dfs_to_concat = find_siblings(connections)
    connections = pd.concat([connections] + [dfs_to_concat], ignore_index=True)

    #grandparent/ aunts/uncles / niece .. /cousin relationship

 
    #grandparents_connections = find_grandparents_aunts(connections)
    #connections = pd.concat([connections] + [grandparents_connections], ignore_index=True)

    #why so weird format
    #cousine_connections = find_cousines(connections)
    #connections = pd.concat([connections] + [cousine_connections], ignore_index=True)
    

    connections.to_csv('network.csv')
    return connections

create_family_layer(registry_data_one_year)

