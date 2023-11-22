import random
import numpy as np
import pandas as pd

already_existing_personnumbers = {'0'}

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
        number = '0'
        while number in already_existing_personnumbers:
            #not perfect for now
            rand_num = random.randint(1000, 9999) 
            num_string = str(rand_num)
            current = res[i]
            current_string = current.strftime("%Y%m%d-")
            number = current_string + num_string
            
        # printing 
        already_existing_personnumbers.add(number)
        person_nummer.append(number)
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
    barn0_3 = []
    barn4_6 = []
    barn7_10 = []
    barn11_15 = []
    barn16_17 = []
    barn18plus= []
    barn18_19 = []
    barn20plus = []
    if sample_year < 2005:
        options = ["barn0_3", "barn4_6", "barn7_10", "barn11_15", "barn16_17", "barn18plus"]
    else: 
        options = ["barn0_3", "barn4_6", "barn7_10", "barn11_15", "barn16_17", "barn18_19", "barn20plus"]
    for i in range(len(discretized_samples)):
        count = discretized_samples[i]
        barn0_3.append(0)
        barn4_6.append(0)
        barn7_10.append(0)
        barn11_15.append(0)
        barn16_17.append(0)
        barn18plus.append(0)
        barn18_19.append(0)
        barn20plus.append(0)
        if count >0:
            children = random.choices(options, k= count)
            #make sure people dont have too many children
            for c in children:
                if c == "barn0_3": 
                    barn0_3[-1] += 1
                elif c == "barn4_6":
                    barn4_6[-1] += 1
                elif c == "barn7_10":
                    barn7_10[-1] += 1
                elif c == "barn11_15":
                    barn11_15[-1] += 1
                elif c == "barn16_17":
                    barn16_17[-1] += 1
                elif c == "barn18plus":
                    barn18plus[-1] += 1
                elif c == "barn18_19":
                    barn18_19[-1] += 1
                elif c=="barn20plus":
                    barn20plus[-1] += 1   
                    
    return pd.DataFrame(list(zip(barn0_3, barn4_6, barn7_10, barn11_15, barn16_17, barn18plus, barn18_19, barn20plus)), 
                        columns=["barn0_3", "barn4_6", "barn7_10", "barn11_15", "barn16_17", "barn18plus", "barn18_19", "barn20plus"])

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

from datetime import date, timedelta, datetime

from variable_functions.generate_educational_variables import generate_education

def generate_family(year,amount):
 
    PersonNr= person_nummer_creation(amount, year) 
    children = create_children(amount, year)

    utbildning = generate_education(amount) 
    # famID = create_famID(PersonNr)
    registry_data = pd.DataFrame()


    registry_data = utbildning.join(children)
    registry_data['PersonNr'] = PersonNr 
    registry_data['famID'] = PersonNr #FIX ME


    return registry_data

