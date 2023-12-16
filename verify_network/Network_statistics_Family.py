import pandas as pd

#read in data


#data read in 
data = pd.read_csv("network_produced_csvs/network_100k.csv")


#basic relationship counts 

relation_ship_counts = data["connection"].value_counts()

print("This is how many connections we have per category.")
print(relation_ship_counts)


#maximum amount of children

# Use value_counts to count unique values
parents = data[data["connection"] == "parent of"]
value_counts = parents["personNr1"].value_counts()

max_count = value_counts.max()
print("most above 15/16 year old children a person has living at home")
print(max_count)

#number of connection per person

filtered_data = data[data["connection"] != "child of"] #as relationship goes both ways
#partners both ways (maybe that is why there is so many --> need to check again)

personnr1= pd.concat([filtered_data['personNr1'], filtered_data['personNr2']], ignore_index=True)
#print(personnr1)
value_counts = personnr1.value_counts()

max_count = value_counts.max()

print("This is the maximum of connections of one person in the network")
print(max_count)


distribution = value_counts.value_counts()


print("This is the distribution of connections among the network, when counting the parent/child connection as one connection")
print(distribution)



