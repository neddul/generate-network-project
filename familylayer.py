import pandas as pd
from itertools import combinations
from tqdm import tqdm

small_testdata = pd.read_csv("100k_rows.csv")
#small_testdata = pd.read_csv("pretty_good_family_data.csv")
#def create_inner_family_relationships():

def find_parent_child_relationship(subset):
    parent_relationships = []
    #also checking for 15, as some 15 year olds have been present in the data
    #parents = subset[(subset['Barn18plus']>0) | (subset['Barn11_15']>0) | (subset['Barn16_17'] >0 )  | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )]

    #probably a more elegant way to do this, but this is to make sure we match parent with a child in a right age group

    #could maybe be stored outside of this
    age_conditions_parents = [
    ('parents_18plus', subset['Barn18plus'] > 0),
    ('parents11_15', subset['Barn11_15'] > 0),
    ('parents16_17', subset['Barn16_17'] > 0),
    ('parents18_19', subset['Barn18_19'] > 0),
    ('parents_20plus', subset['Barn20plus'] > 0),
]
    #children = subset[subset['Alder'] >= 15]
    age_conditions_children = [
    ('children_18plus', subset['Alder'] >= 18),
    ('children11_15', subset['Alder'].between(11, 15)),
    ('children16_17', subset['Alder'].between(16, 17)),
    ('children18_19', subset['Alder'].between(18, 19)),
    ('children_20plus', subset['Alder'] >= 20),
]
    #to create siblings
    dfs_to_concat = []
    for (parent_label, parent_condition), (children_label, children_condition) in zip(age_conditions_parents, age_conditions_children):
        parents = subset[parent_condition]
        children = subset[children_condition]
        if not children.empty and not parents.empty:
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

            if not current_connections.empty:
                siblings_possible = (((current_connections['personNr1'] == person1) & (current_connections['personNr2'] == person2) & (current_connections['connection'] == "siblings")) | ((current_connections['personNr1'] == person2) & (current_connections['personNr2'] == person1) & (current_connections['connection'] == "siblings")) ).any()
            else:
                siblings_possible=False
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
    for _, parent_row in tqdm(parent_rows.iterrows(), total=len(parent_rows), desc="Finding Grandparents, aunts, uncles"):
        # Find rows where 'Personnr1' in the original dataframe matches 'personNr2' in the current row
        matching_rows = parent_rows[parent_rows['personNr2'] == parent_row['personNr1']]
        
        matching_rows_auntsuncles_1 = sibling_rows[(sibling_rows['personNr2'] == parent_row['personNr1']) ]
        matching_rows_auntsuncles_2 = sibling_rows[(sibling_rows['personNr1'] == parent_row['personNr1'])]
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
        
        
        if not matching_rows_auntsuncles_1.empty:
            for _, matching_row in matching_rows_auntsuncles_1.iterrows():

        #aunts and uncles

        #issue we dont know if in this case it should be person nr 1 or 2 

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
    for _, aunt_uncle_row in tqdm(aunt_uncle_rows.iterrows(), total=len(aunt_uncle_rows), desc="Finding cousins"):
        matching_rows = parent_rows[parent_rows['personNr1'] == aunt_uncle_row['personNr1']]
        
        for _, matching_row in matching_rows.iterrows():

            existing_cousin = cousines[
                ((cousines['personNr1'] == matching_row['personNr2']) & (cousines['personNr2'] == aunt_uncle_row['personNr2'])) |
                ((cousines['personNr1'] == aunt_uncle_row['personNr2']) & (cousines['personNr2'] == matching_row['personNr2']))
            ]
            if existing_cousin.empty:
                cousines = cousines.append({
                    'personNr1': matching_row['personNr2'],
                    'personNr2': aunt_uncle_row['personNr2'],
                    'connection': "cousins"
                }, ignore_index=True)
            
    return cousines

def create_family_layer(registry_data):
    connections = pd.DataFrame(columns=['personNr1', 'personNr2', 'connection'])
    for family in tqdm(registry_data['FamId'].unique(), desc="Processing families"):
        # Filter rows where 'famID' has the current value and reduce data to only the needed columns for this case
        subset = registry_data[registry_data['FamId'] == family][['PersonNr', 'Barn18plus', 'Barn11_15', 'Barn16_17', 'Barn18_19', 'Barn20plus', 'Alder' ]]
        # Check if each row has a value greater than or equal to 0 in the 'your_column' column
        if len(subset)> 1: 
            #will there be an option to check which year, we are working on

            #work on child-parent relationship 
            #parents = subset[(subset['Barn18plus'] > 0) | (subset['Barn16_17'] >0 ) | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )].any(axis=1)
            parents = subset[(subset['Barn18plus']>0) | (subset['Barn11_15']>0) |  (subset['Barn16_17'] >0 )  | (subset['Barn18_19'] > 0) | (subset['Barn20plus'] >0 )]
            output = []
            if len(parents)> 0:
                output = find_parent_child_relationship(subset)

                connections = pd.concat([connections, output])

            #work on the partner relationship --> we are using the output here to reduce the running time
            relationships = find_relationships(subset, pd.DataFrame(output))
            connections = pd.concat([connections, relationships])
            

        
    #sibling relationship
    #dfs_to_concat = find_siblings(connections)
    #if not dfs_to_concat.empty:
    #    connections = pd.concat([connections] + [dfs_to_concat], ignore_index=True)

    #grandparent/ aunts/uncles / niece .. /cousin relationship

    #can add progress bars here --> but rather quick
    grandparents_connections = find_grandparents_aunts(connections)
    if not grandparents_connections.empty:
        connections = pd.concat([connections] + [grandparents_connections], ignore_index=True)


    cousine_connections = find_cousines(connections)
    if not cousine_connections.empty:
        connections = pd.concat([connections] + [cousine_connections], ignore_index=True)
    

    connections.to_csv('network_100k.csv')
    return connections

create_family_layer(small_testdata)




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
# run code on more data(?)
# optimizing and correcting code for one year  --> check barns age speficially ) --> fix mistake on data , double saving of some connections
# expanding code for 30 years


#some people categorized as simpling when they are partners --> issue living together with grandparents

#how to handle death data -> how is it in the real data 
#check edge cases -->


#first step tomorrow: fix check childrens age --> probably fixes the other mistakes


#suggestions Matteo: 

#variable name configuration file
# preprocessing for the possible variables in the year


# only use recently created siblings in the loob --> maybe not optimal for using more years, but for one year should reduce time by a good bit
#double check if first check is length to make it faster