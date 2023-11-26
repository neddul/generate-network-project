import pandas as pd
from itertools import combinations

small_testdata = pd.read_csv("30_people_data.csv")


def find_parent_child_relationship(subset):
    parent_relationships = []
    parents = subset[(subset['Barn18plus']>0) |  (subset['Barn16_17'] >0 )  | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )]
    #not checking if the children is actually fitting the exact category
    children = subset[subset['Alder'] >= 16]
    print(children)
    #to create siblings
    dfs_to_concat = []
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
                #print(eligible_children)
                if len(eligible_children)>1:
                    personNr2_list = eligible_children['PersonNr'].tolist()
                    personNr2_list = sorted(personNr2_list)

                    if len(personNr2_list) == 2:
                        # If length is 2, create a single row with 'siblings' as the connection
                        row_data = pd.DataFrame([{'personNr1': personNr2_list[0], 'personNr2': personNr2_list[1], 'connection': 'siblings'}])
                        dfs_to_concat.extend([pd.DataFrame(row_data)])
                        
                    elif len(personNr2_list) > 2:
                        # If length is greater than 2, create rows for all combinations
                        for pair in combinations(personNr2_list, 2):
                            row_data = pd.DataFrame([{'personNr1': pair[0], 'personNr2': pair[1], 'connection': 'siblings'}])
                            dfs_to_concat.extend([pd.DataFrame(row_data)])
                   
                

    if parent_relationships:
        # Concatenate all DataFrames in the list
        parent_relationships = pd.concat(parent_relationships, ignore_index=True)
        if dfs_to_concat:

            dfs_to_concat = pd.DataFrame(pd.concat(dfs_to_concat).drop_duplicates(ignore_index=True))

            parent_relationships = pd.concat([parent_relationships, dfs_to_concat], ignore_index=True)
    else:
        # Create an empty DataFrame
        parent_relationships = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])

            
    return parent_relationships


def find_relationships(subset, current_connections):
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

            #checking if they might be siblings 
            siblings_possible = (((current_connections['personNr1'] == person1) & (current_connections['personNr2'] == person2) & (current_connections['connection'] == "siblings")) | ((current_connections['personNr1'] == person2) & (current_connections['personNr2'] == person1) & (current_connections['connection'] == "siblings")) ).any()
            #add check for amount of children (?)
            if age_difference <= 13 and siblings_possible==False:
                row_data = pd.DataFrame([{'personNr1':person1 , 'personNr2': person2, 'connection': "partner of"}])
                couple_relationships = pd.concat([couple_relationships, row_data])
               
    return couple_relationships

def find_grandparents_aunts(family_connections):
    
    #make this without warnings --> change append to concat 
    
    grandparents_list = []
    parent_rows = family_connections[family_connections['connection'] == 'parent of']
    sibling_rows = family_connections[family_connections['connection'] == 'siblings']
    for _, parent_row in parent_rows.iterrows():
        # Find rows where 'Personnr1' in the original dataframe matches 'personNr2' in the current row
        matching_rows = parent_rows[parent_rows['personNr2'] == parent_row['personNr1']]
        
        matching_rows_auntsuncles = sibling_rows[(sibling_rows['personNr2'] == parent_row['personNr1']) |(sibling_rows['personNr1'] == parent_row['personNr1'])]
        # Iterate through matching rows and add to the result dataframe
        if not matching_rows.empty:
            for _, matching_row in matching_rows.iterrows():

                grandparents_list.append({
                    'personNr1': matching_row['personNr1'],
                    'personNr2': parent_row['personNr2'],
                    'connection': "grandparent of"
                })
                grandparents_list.append({
                    'personNr1': parent_row['personNr2'],
                    'personNr2': matching_row['personNr1'],
                    'connection': "grandchild of"
                })
        
        
        if not matching_rows_auntsuncles.empty:
            for _, matching_row in matching_rows_auntsuncles.iterrows():

        #aunts and uncles
                grandparents_list.append({
                    'personNr1': matching_row['personNr1'],
                    'personNr2': parent_row['personNr2'],
                    'connection': "aunt/uncle of"
                })
                grandparents_list.append({
                    'personNr1': parent_row['personNr2'],
                    'personNr2': matching_row['personNr1'],
                    'connection': "niece/newphew of"
                })

    return   pd.DataFrame(grandparents_list, columns=['personNr1', 'personNr2', 'connection'])
            
    

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

def find_cousines(family_connections):
    cousines= pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    aunt_uncle_rows = family_connections[family_connections['connection'] == 'aunt/uncle of']
    parent_rows = family_connections[family_connections['connection'] == 'parent of']
    
    aunt_uncle_rows = aunt_uncle_rows.reset_index(drop=True)
    parent_rows = parent_rows.reset_index(drop=True)
    for _, aunt_uncle_row in aunt_uncle_rows.iterrows():
        matching_rows = parent_rows[parent_rows['personNr1'] == aunt_uncle_row['personNr1']]
        
        for _, matching_row in matching_rows.iterrows():
            cousines = cousines.append({
                'personNr1': matching_row['personNr2'],
                'personNr2': aunt_uncle_row['personNr2'],
                'connection': "cousins"
            }, ignore_index=True)
            
    return cousines

def create_family_layer(registry_data):
    connections = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    for family in registry_data['FamId'].unique():
        # Filter rows where 'famID' has the current value
        subset = registry_data[registry_data['FamId'] == family]
        # Check if each row has a value greater than or equal to 0 in the 'your_column' column
        print(subset)
        if len(subset)> 1: 
            #will there be an option to check which year, we are working on

            #work on child-parent relationship 
            #parents = subset[(subset['Barn18plus'] > 0) | (subset['Barn16_17'] >0 ) | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )].any(axis=1)
            parents = subset[(subset['Barn18plus']>0) |  (subset['Barn16_17'] >0 )  | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )]
            print(parents)
            if len(parents)> 0:
                output = find_parent_child_relationship(subset)

                connections = pd.concat([connections, output])

            #work on the partner relationship
            relationships = find_relationships(subset, connections)
            connections = pd.concat([connections, relationships])
            

        
    #sibling relationship
    #dfs_to_concat = find_siblings(connections)
    #if not dfs_to_concat.empty:
    #    connections = pd.concat([connections] + [dfs_to_concat], ignore_index=True)

    #grandparent/ aunts/uncles / niece .. /cousin relationship

    
    grandparents_connections = find_grandparents_aunts(connections)
    if not grandparents_connections.empty:
        connections = pd.concat([connections] + [grandparents_connections], ignore_index=True)


    cousine_connections = find_cousines(connections)
    if not cousine_connections.empty:
        connections = pd.concat([connections] + [cousine_connections], ignore_index=True)
    

    connections.to_csv('network.csv')
    return connections

create_family_layer(small_testdata)

