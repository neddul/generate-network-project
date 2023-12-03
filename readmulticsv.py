import pandas as pd
import os
def directory_of_csv_to_df(path="multiple_year/synthetic_scb_data_1990"):
    data = []
    folder_path = path
    csv_list = os.listdir(folder_path)
    print(f"{0}/{len(csv_list)}")
    i = 0
    for filename in csv_list:
        if (i+1) % 25 == 0:
            print(f"{i+1}/{len(csv_list)}")
        
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            t = pd.read_csv(file_path)
            data.append(t)
        i+=1
    if len(data) > 0:
        return pd.concat(data)
    else:
        return pd.DataFrame()

            
if __name__ == "__main__":
    path = "multiple_year/synthetic_scb_data_1990" # Give the relative path to the directory of all the csv files from where this python file is
    a = directory_of_csv_to_df(path)
    print(len(a)) # Prints the number of rows of the resulting dictionary


