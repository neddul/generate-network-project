import pandas as pd

#dataformat needs to be fixed --> read in check everything
network = pd.read_csv("final_network/final_network2019.csv")

filtered_df = network[(network['personNr1'] == "19930715-4898") | (network['personNr2'] == "19930715-4898")]



print(filtered_df)

#relation_ship_counts = filtered_df["connection"].value_counts()

print("This is how many connections we have per category.")
#print(relation_ship_counts)

connection_detail = filtered_df[(filtered_df["connection"]=="cousins") | (filtered_df["connection"]=="siblings") |(filtered_df["connection"]=="partner of")]

print(connection_detail)


connections = connection_detail[["personNr1", "personNr2", "connection"]].astype(str)
print(filtered_df[(filtered_df.duplicated(subset=['personNr1', 'personNr2']))])
# Filter the DataFrame
connections = connections[~((connections.duplicated(subset=['personNr1', 'personNr2'])) & (connections['connection'] == 'partner of'))]

# Display the result
print(connections)
#partner development --> one can only be partner to one person in the household


#sibling always outnumbers partners --> drop those rows --> make partners also order so it is dropable --> especially with half siblings

#weird age differences make weird constellations --> double check again --> how to make family checks

#the group me seems to stop working .. 


#definitely partner sibing drop
