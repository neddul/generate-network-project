import random
import pandas as pd
import json
from datetime import date, timedelta, datetime
import numpy as np
import string
import dateutil.relativedelta

def person_nummer_creation(amount, sample_year): 
    test_date1, test_date2 = date(1900, 1, 1), date(sample_year-16, 1, 1)
    res_dates = [test_date1]
 
    # loop to get each date till end date
    while test_date1 != test_date2:
        test_date1 += timedelta(days=1)
        res_dates.append(test_date1)
    res = random.choices(res_dates, k=amount)

    person_nummer = []
    for i in range(amount):
        #not perfect for now
        rand_num = random.randint(1000, 9999) 
        num_string = str(rand_num)
        current = res[i]
        current_string = current.strftime("%Y%m%d-")
        person_nummer.append(current_string + num_string)
    # printing 
    return person_nummer


def create_children(amount, sample_year):
    

    #distribution of children: #amount of children per person

    mean = 1.16  # Mean of the normal distribution -- lower than what is given as it most likely is not an actual normal
    stddev = 3  # Standard deviation of the normal distribution
    lower_bound = 0.0  # Minimum value (never below 0)

    # Generate num_samples samples from a standard normal distribution
    samples = np.random.normal(loc=mean, scale=stddev, size=amount)

    # Discretize the samples by rounding to the nearest integer
    discretized_samples = np.round(samples).astype(int)
    #no samples below 0
    discretized_samples[discretized_samples < 0] = 0
    #create variables
    Barn0_3 = []
    Barn4_6 = []
    Barn7_10 = []
    Barn11_15 = []
    Barn16_17 = []
    Barn18plus= []
    Barn18_19 = []
    Barn20plus = []
    if sample_year < 2005:
        options = ["barn0_3", "barn4_6", "barn7_10", "barn11_15", "barn16_17", "barn18plus"]
    else: 
        options = ["barn0_3", "barn4_6", "barn7_10", "barn11_15", "barn16_17", "barn18_19", "barn20plus"]
    for i in range(len(discretized_samples)):
        count = discretized_samples[i]
        Barn0_3.append(0)
        Barn4_6.append(0)
        Barn7_10.append(0)
        Barn11_15.append(0)
        Barn16_17.append(0)
        Barn18plus.append(0)
        Barn18_19.append(0)
        Barn20plus.append(0)
        if count >0:
            children = random.choices(options, k= count)
            #make sure people dont have too many children
            for c in children:
                if c == "barn0_3": 
                    Barn0_3[-1] += 1
                elif c == "barn4_6":
                    Barn4_6[-1] += 1
                elif c == "barn7_10":
                    Barn7_10[-1] += 1
                elif c == "barn11_15":
                    Barn11_15[-1] += 1
                elif c == "barn16_17":
                    Barn16_17[-1] += 1
                elif c == "barn18plus":
                    Barn18plus[-1] += 1
                elif c == "barn18_19":
                    Barn18_19[-1] += 1
                elif c=="barn20plus":
                    Barn20plus[-1] += 1
                    
    return pd.DataFrame(list(zip(Barn0_3, Barn4_6, Barn7_10, Barn11_15, Barn16_17, Barn18plus, Barn18_19, Barn20plus)), 
                        columns=["Barn0_3", "Barn4_6", "Barn7_10", "Barn11_15", "Barn16_17", "Barn18plus", "Barn18_19", "Barn20plus"])
def create_date_object(date_string):
    date_format = "%Y%m%d"
    date_object = datetime.strptime(date_string[:8], date_format)

    return date_object


#shuffle group --> currently not taking into account where they live --> we should do 
#everyone is their own family
def create_famID(person_nummer): 
    
    # Define the minimum and maximum group size
    min_group_size = 1
    max_group_size = 4

    # Shuffle the list randomly
    #random.shuffle(person_nummer)

    # Create random groups with random group sizes
    groups = []
    famID= []
    while person_nummer:
        group_size = random.randint(min_group_size, max_group_size)
        group = person_nummer[:group_size]
        person_nummer = person_nummer[group_size:]
        groups.append(group)

    for group in groups: 
            
        birthdays = [create_date_object(date) for date in group]
        oldest = birthdays.index(min(birthdays))
        for i in range(len(birthdays)):
            famID.append(group[oldest])
    return famID



def random_sampler(start, end, number):
    output = []
    for k in range(number):
        output.append(random.randint(start, end))
        
    return output

def create_utbildning(amount): 
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
        if isinstance(options_niv, int) and options_niv>100:
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

def fodelse_ar(personnummer):
    fodelse_ar = []
    for i in personnummer:
        fodelse_ar.append(i[:4])
    return fodelse_ar

def alder(PersonNr, sample_year):
    ages = []
    for personnummer in PersonNr: 
        today = datetime(sample_year, 11, 1)
        year, month, day = int(personnummer[:4]), int(personnummer[4:6]), int(personnummer[6:8])
        birthday = datetime(year, month, day)
        age = dateutil.relativedelta.relativedelta(today, birthday)
        ages.append(age.years)
    return ages

def create_registration_data(year,amount):
 
    PersonNr= person_nummer_creation(amount, year)
    children = create_children(amount, year)
    #print(data.head())
    utbildning = create_utbildning(amount)
    famID = create_famID(PersonNr)
    FodelseAr = fodelse_ar(PersonNr)
    alder_all = alder(PersonNr, year)
    #registry_data_1 = data.join(utbildning)
    registry_data = utbildning.join(children)
    registry_data['PersonNr'] = PersonNr
    registry_data['famID'] = famID
    registry_data['FodesleAr'] = FodelseAr
    registry_data['Alder'] =alder_all

    return registry_data

registration_data = create_registration_data(1990, 10000)
registration_data.to_csv('testdatanew.csv')
print(registration_data.head())