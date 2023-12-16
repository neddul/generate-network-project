import pandas as pd
import os
def directory_of_csv_to_df(folder_path="multiple_year/synthetic_scb_data_1990"):
    data = []
    csv_list = os.listdir(folder_path)
    number_of_csvs = len(csv_list)
    i = 1
    print(f"{i}/{number_of_csvs}")
    for filename in csv_list:
        if i % 5 == 0:
            print(f"{i}/{number_of_csvs}")
        
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            t = pd.read_csv(file_path)
            data.append(t)
        i+=1
    if len(data) > 0:
        return pd.concat(data)
    else:
        print(f"Directory \"{folder_path}\" had no csv-files")
        return pd.DataFrame()


def directory_to_list_of_df(folder_path="multiple_year/synthetic_scb_data"):
    data = []
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")

    #Gets all the sub folders from the parent directory
    sub_directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    subdirectories_len = len(sub_directories)
    i = 1
    for sub_directory in sub_directories:
        print(f"Directory {i}/{subdirectories_len}")
        sub_directory_path = os.path.join(folder_path, sub_directory)
        data.append(directory_of_csv_to_df(sub_directory_path))
        i+=1

    return data

g = directory_to_list_of_df()


            
if __name__ == "__main__":
    #Reading single directory of csvs
    path = "multiple_year/synthetic_scb_data/synthetic_scb_data_1990" # Give the relative path to the directory of all the csv files from where this python file is
    a = directory_of_csv_to_df(path)
    print(len(a)) # Prints the number of rows of the resulting dictionary

    #Reading directory of directories of csvs
    folder_path="multiple_year/synthetic_scb_data" # Give the relative path to the parent directory that contains all the directories
    b = directory_to_list_of_df(folder_path)
    print(len(b)) # Prints the number of dataframes made from all the directories


