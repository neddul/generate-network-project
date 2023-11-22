import random
import string
import pandas as pd

def random_sampler(start, end, number):
    output = []
    for _ in range(number):
        output.append(random.randint(start, end))
        
    return output

def generate_education(amount): 
    Sun2000niva_old = random_sampler(10000,99999, amount)
    utbildning = pd.read_excel("variable_data/utbildning_cleaner.xlsx")
    #utbildning = utbildning.dropna()
    indexes = random_sampler(0,len(utbildning)-1, amount)
    SUN2000Grp = []
    SUN2000Inr = []
    SUN2000Niva = []
    alphabet = string.ascii_lowercase
    for i in range(len(indexes)):
        index = indexes[i]
        SUN2000Grp.append(utbildning.at[index, 'Utbildningsgrupper 2020'])
        options_inr = utbildning.at[index, 'Inriktningskoder SUN 2020']
        if isinstance(options_inr , int):
            random_letters = random.choice(alphabet)
            if options_inr <100: 
                options_inr=options_inr+100
            SUN2000Inr.append(str(options_inr)+ random_letters)
        else: 
            options = [item.strip() for item in options_inr.split(',')]
            SUN2000Inr.append(random.choice(options))
        options_niv = utbildning.at[index, 'Nivåkoder SUN 2020']
        if isinstance(options_niv, int) and options_niv > 100:
            SUN2000Niva.append(options_niv)
        elif isinstance(options_niv, int):
            SUN2000Niva.append(options_niv*100)
        else: 
            options = [item.strip() for item in options_niv.split(',')]
            selection = random.choice(options)
            if  isinstance(selection, int) and selection <100:
                SUN2000Niva.append(selection*100)
            else: 
                    
                SUN2000Niva.append(selection)
    #examAr is missing as well 
    
    #examkommun is different 
    return pd.DataFrame(list(zip(Sun2000niva_old, SUN2000Niva, SUN2000Inr, SUN2000Grp)), 
                        columns=["Sun2000niva_old", "SUN2000Niva", "SUN2000Inr", "SUN2000Grp"])