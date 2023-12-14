import random
import pandas as pd

from datetime import date, timedelta
import datetime
numbers = [str(x) for x in range(10)]

taken_social_security_numbers = {'0'}

def get_date(start_date = '19250101', stop_date='20230101'):
    # datetime for start date
    start_year = int(start_date[:4])
    start_month = int(start_date[4:6])
    start_day = int(start_date[6:8])
    start = datetime.datetime(start_year, start_month, start_day)

    # datetime for stop date
    stop_year = int(stop_date[:4])
    stop_month = int(stop_date[4:6])
    stop_day = int(stop_date[6:8])
    stop = datetime.datetime(stop_year, stop_month, stop_day)

    # take random amount of days after the starting date
    max_days = (stop - start).days
    mean = max_days/2
    std = max_days/3
    days_after_start = random.gauss(mean, std)

    # check if the gauss distribution picked a date outside of the range
    if days_after_start > max_days:
        days_after_start = max_days
    elif days_after_start < 0:
        days_after_start = 0

    date = start + datetime.timedelta(days = days_after_start)
    date_as_string = (str(date.year).rjust(4) + str(date.month).rjust(2) + str(date.day).rjust(2)).replace(' ','0')
    date_as_string = date_as_string + "-"
    return date_as_string

# for _ in range(100):
#     print(get_date())

def person_nummer_creation(sample_year, start_date="19250101", stop_year="", gender=3, existing_list=""):        
    if stop_year == "":
        end_date = str(sample_year-16) #People need to be atleast 16 to legally live alone in Sweden
        end_date = end_date + "1231"
        # possible_birthdays  = birth_dates(start_date, end_date)
    else:
        end_date = stop_year
        # possible_birthdays  = birth_dates(start_date, stop_year)
 
    # mean = len(possible_birthdays) / 2
    # std_dev = len(possible_birthdays) / 3
    
    social_security_number = '0'
    while social_security_number in taken_social_security_numbers:
        #not perfect for now
        if gender == 2: # Girl
            last_4 = random.choices(numbers, k=2)
            digits = ["0", "2", "4", "6", "8"]
            last_4 = last_4 + random.choice(digits)
            last_4 = last_4 + random.choice(numbers)
        elif gender == 1: # Guy
            last_4 = random.choices(numbers, k=2)
            digits = ["1", "3", "5", "7", "9"]
            last_4 = last_4 + random.choice(digits)
            last_4 = last_4 + random.choice(numbers)
        else: # Guy or girl
            last_4 = random.choices(numbers, k=4)
        # birthday = choose_item_with_normal_distribution(possible_birthdays, mean, std_dev)
        # birthdate = birthday.strftime("%Y%m%d-")
        birthdate = get_date(start_date, end_date)
        social_security_number = birthdate
        for d in last_4:
            social_security_number += d

    taken_social_security_numbers.add(social_security_number)
    return social_security_number

def create_children(sample_year, PersonNr, is_kid=False):
    barn = {
        'Barn0_3' : [0],
        'Barn4_6' : [0],
        'Barn7_10' : [0],
        'Barn11_15' : [0],
        'Barn16_17' : [0],
    }
    if sample_year < 2005:
        barn['Barn18plus'] = [0]
    else: 
        barn['Barn18_19'] = [0]
        barn['Barn20plus'] = [0]
    #roughly 68% of households are childless 
    # https://www.scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/statistiknyhet/befolkningsstatistik-helaret-20222/
    keys = list(barn.keys())
    if random.randint(1,100) > 65:
        mean = 1.81  # Mean of the normal distribution 
        stddev = 1.3  # Standard deviation of the normal distribution
        number_of_kids = int(random.gauss(mean, stddev))
        if number_of_kids < 1:
            number_of_kids = 1

        for _ in range(number_of_kids):
            person_age = int(sample_year) - int(PersonNr[:4])
            min_age = (person_age - 60) if person_age > 60 else 0 #Max age to get newborns is 60
            max_age = person_age - 15
            kid_age = random.randint(min_age, max_age)
            kid_age_t = (kid_age - min_age) / ((max_age - min_age))
            kid_age_t = kid_age_t * kid_age_t
            kid_age = int(kid_age_t * (max_age - min_age) + min_age)
            if kid_age <= 3:
                barn['Barn0_3'][0] +=1
            elif kid_age < 7:
                barn['Barn4_6'][0] +=1
            elif kid_age < 11:
                barn['Barn7_10'][0] +=1
            elif kid_age < 16:
                barn['Barn11_15'][0] +=1
            elif kid_age < 18:
                barn['Barn16_17'][0] +=1
            elif 'Barn18plus' in keys and kid_age >= 18:
                barn['Barn18plus'][0] += 1
            elif not 'Barn18plus' in keys and kid_age < 20:
                barn['Barn18_19'][0] +=1
            elif not 'Barn18plus' in keys and kid_age >= 20:
                barn['Barn20plus'][0] +=1
        
        for key in keys: #No more than 3 kids per category
            if barn[key][0] > 3:
                barn[key][0] = 3

    if 'Barn18plus' in keys:
        barn = {
            'Barn0_3'       : barn['Barn0_3'],
            'Barn4_6'       : barn['Barn4_6'],
            'Barn7_10'      : barn['Barn7_10'],
            'Barn11_15'     : barn['Barn11_15'],
            'Barn16_17'     : barn['Barn16_17'],
            'Barn18plus'    : barn['Barn18plus'],
            'Barn18_19'     : [None],
            'Barn20plus'    : [None]
               }
    else:
        barn = {
            'Barn0_3'       : barn['Barn0_3'],
            'Barn4_6'       : barn['Barn4_6'],
            'Barn7_10'      : barn['Barn7_10'],
            'Barn11_15'     : barn['Barn11_15'],
            'Barn16_17'     : barn['Barn16_17'],
            'Barn18plus'    : [None],
            'Barn18_19'     : barn['Barn18_19'],
            'Barn20plus'    : barn['Barn20plus']
               }
    if is_kid and 'Barn18plus' in keys:
        barn = {
            'Barn0_3'       : [0],
            'Barn4_6'       : [0],
            'Barn7_10'      : [0],
            'Barn11_15'     : [0],
            'Barn16_17'     : [0],
            'Barn18plus'    : [0],
            'Barn18_19'     : [None],
            'Barn20plus'    : [None]
               }
    if is_kid and not 'Barn18plus' in keys:
        barn = {
            'Barn0_3'       : [0],
            'Barn4_6'       : [0],
            'Barn7_10'      : [0],
            'Barn11_15'     : [0],
            'Barn16_17'     : [0],
            'Barn18plus'    : [None],
            'Barn18_19'     : [0],
            'Barn20plus'    : [0]
               }
    return pd.DataFrame.from_dict(barn)

from generate_educational_variables import generate_education

def make_kid_family_frame(PersonNr, FamId, is_Kid, sample_year, utbildning=""):
    kids = create_children(sample_year, PersonNr, is_kid=is_Kid)
    utbildning = generate_education(1, utbildning)
    data = pd.DataFrame()
    data = utbildning.join(kids)
    data['PersonNr'] = PersonNr
    data['FamId'] = FamId
    return data

def create_kids_data(sample_year, FamId, kids, utbildning):

    no_kids = [kids.loc[0, 'Barn16_17'], kids.loc[0, 'Barn18plus'], kids.loc[0, 'Barn18_19'], kids.loc[0, 'Barn20plus']]
    no_kids = [0 if item is None else item for item in no_kids]
    # print(no_kids)
    #Barn16-17
    all_kids = []

    if no_kids[0] == 2: 
        if random.randint(1,100) > 95: #Twins
            age = random.randint(16,17)
            year_born = sample_year-age
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
            kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
        else: #One kid is 16, the other is 17
            year_born = sample_year-17
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0630") # First kid born jan - june year 1
            kid2 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0401", stop_year=f"{year_born+1}1231") # Second kid born atleast 10 months later
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
    elif no_kids[0] == 3: 
        if random.randint(1,100) > 40: #Twins
            age = random.randint(16,17)
            if age == 16:
                year_born = sample_year-age
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-1}0101", stop_year=f"{year_born-1}0630") # First kid born jan - june year 1    
                twin1 = person_nummer_creation(sample_year, start_date=f"{year_born}0401", stop_year=f"{year_born}1231") #Twins born atleast 10 months later
                twin2 = person_nummer_creation(sample_year, start_date=twin1[:8], stop_year=twin1[:8])
            else:
                year_born = sample_year-age
                twin1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0430") #Twins born jan - june
                twin2 = person_nummer_creation(sample_year, start_date=twin1[:8], stop_year=twin1[:8])
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0401", stop_year=f"{year_born+1}1231") # Third kid born atleast 10 months later

            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(twin1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(twin2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        else: #One kid is 16, the other is 17
            age = 17
            year_born = sample_year-age
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0210") # First kid born jan - feb year 1
            kid2 = person_nummer_creation(sample_year, start_date=f"{year_born}1201", stop_year=f"{year_born+1}0130") # Second kid born atleast 10 months later
            kid3 = person_nummer_creation(sample_year, start_date=f"{year_born+1}1101", stop_year=f"{year_born+1}1231") # Third kid born atleast 10 months later

            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(kid3, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        
    elif no_kids[0] == 1:
        age = 17
        year_born = sample_year-age
        kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born+1}1231") # Single kid can be born any date as long as they are 16-17
        
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))

    #Barn18plus Make better
    if no_kids[1] == 1:
        age = 18
        year_born = sample_year-age
        kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-7}0101", stop_year=f"{year_born}1231") # Single kid can be ages 18-25
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        
    elif no_kids[1] == 2:
        age = 18
        year_born = sample_year-age
        kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-1}0101", stop_year=f"{year_born}0330") # Single kid can be born any date as long as they are 16-17
        kid2 = person_nummer_creation(sample_year, start_date=f"{year_born-3}0101", stop_year=f"{year_born-2}0330") # Single kid can be born any date as long as they are 16-17
        
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))

    elif no_kids[1] == 3:
        if random.randint(1,100) > 95: #Twins
            twin_age = random.randint(18,23)
            if twin_age < 20: # Twins are youngest
                year_born = sample_year-twin_age
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-3}0101", stop_year=f"{year_born-2}0630") # First kid born earlier than twins 
                twin1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231") #Twins born jan - dec 1.5 years later
                twin2 = person_nummer_creation(sample_year, start_date=twin1[:8], stop_year=twin1[:8])
            else:
                year_born = sample_year-twin_age
                twin1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231") #Twins born atleast 10 months later
                twin2 = person_nummer_creation(sample_year, start_date=twin1[:8], stop_year=twin1[:8])
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0601", stop_year=f"{year_born+2}1231") # First kid born jan - june year 1    
            
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(twin1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(twin2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        else:
            year_born = sample_year-18
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-1}0101", stop_year=f"{year_born}1231") # First kid born earlier than twins 
            kid2 = person_nummer_creation(sample_year, start_date=f"{year_born-3}0101", stop_year=f"{year_born-2}1231") # First kid born earlier than twins 
            kid3 = person_nummer_creation(sample_year, start_date=f"{year_born-5}0101", stop_year=f"{year_born-4}1231") # First kid born earlier than twins 

            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(kid3, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))

    
    #Barn18_19
    if no_kids[2] == 2: 
        if random.randint(1,100) > 95: #Twins
            age = random.randint(18,19)
            year_born = sample_year-age
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
            kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])

        else: #One kid is 16, the other is 17
            year_born = sample_year-19
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0630") # First kid born jan - june year 1
            kid2 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0401", stop_year=f"{year_born+1}1231") # Second kid born atleast 10 months later
        
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
    elif no_kids[2] == 3: 
        if random.randint(1,100) > 40: #Twins
            age = random.randint(18,19)
            if age == 18:
                year_born = sample_year-age
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-1}0101", stop_year=f"{year_born-1}0630") # First kid born jan - june year 1    
                twin1 = person_nummer_creation(sample_year, start_date=f"{year_born}0401", stop_year=f"{year_born}1231") #Twins born atleast 10 months later
                twin2 = person_nummer_creation(sample_year, start_date=twin1[:8], stop_year=twin1[:8])
            else:
                year_born = sample_year-age
                twin1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0430") #Twins born jan - june
                twin2 = person_nummer_creation(sample_year, start_date=twin1[:8], stop_year=twin1[:8])
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0401", stop_year=f"{year_born+1}1231") # Third kid born atleast 10 months later    
            
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(twin1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(twin2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        else: #One kid is 18, the other is 19
            age = 19
            year_born = sample_year-age
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0210") # First kid born jan - feb year 1
            kid2 = person_nummer_creation(sample_year, start_date=f"{year_born}1201", stop_year=f"{year_born+1}0130") # Second kid born atleast 10 months later
            kid3 = person_nummer_creation(sample_year, start_date=f"{year_born+1}1101", stop_year=f"{year_born+1}1231") # Third kid born atleast 10 months later
            
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
            all_kids.append(make_kid_family_frame(kid3, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))

    elif no_kids[2] == 1:
        age = 19
        year_born = sample_year-age
        kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born+1}1231") # Single kid can be born any date as long as they are 16-17
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))

    #Barn20plus Make better
    if no_kids[3] == 1:
        age = 20
        year_born = sample_year-age
        kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-6}0101", stop_year=f"{year_born}1231") # Possible ages is 20-26
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        
    elif no_kids[3] == 2:
        age = 20
        year_born = sample_year-age
        kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-1}0101", stop_year=f"{year_born}0330") # Single kid can be born any date as long as they are 16-17
        kid2 = person_nummer_creation(sample_year, start_date=f"{year_born-3}0101", stop_year=f"{year_born-2}0330") # Single kid can be born any date as long as they are 16-17
        
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
    elif no_kids[3] == 3:
        if random.randint(1,100) > 95: #Twins
            twin_age = random.randint(20,25)
            if twin_age < 22: # Twins are youngest
                year_born = sample_year-twin_age
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-3}0101", stop_year=f"{year_born-2}0630") # First kid born earlier than twins 
                kid2 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231") #Twins born jan - dec 1.5 years later
                kid3 = person_nummer_creation(sample_year, start_date=kid2[:8], stop_year=kid2[:8])
            else:
                year_born = sample_year-twin_age
                kid2 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231") #Twins born atleast 10 months later
                kid3 = person_nummer_creation(sample_year, start_date=kid2[:8], stop_year=kid2[:8])
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0601", stop_year=f"{year_born+2}1231") # First kid born jan - june year 1    
            
        else:
            year_born = sample_year-20
            kid1 = person_nummer_creation(sample_year, start_date=f"{year_born-1}0101", stop_year=f"{year_born}1231") # First kid born earlier than twins 
            kid2 = person_nummer_creation(sample_year, start_date=f"{year_born-3}0101", stop_year=f"{year_born-2}1231") # First kid born earlier than twins 
            kid3 = person_nummer_creation(sample_year, start_date=f"{year_born-5}0101", stop_year=f"{year_born-4}1231") # First kid born earlier than twins 
        
        all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
        all_kids.append(make_kid_family_frame(kid3, FamId, is_Kid=True, sample_year=sample_year, utbildning=utbildning))
    if len(all_kids) > 0:
        return pd.concat(all_kids)
    else:
        big_kids = pd.DataFrame(columns=['Barn0_3', 'Barn4_6', 'Barn7_10', 'Barn11_15', 'Barn16_17', 'Barn18plus', 'Barn18_19', 'Barn20plus', 'PersonNr', 'FamId'])
        return big_kids       

def create_spouse(FamId, kids_info, utbildning):
    spouse_age = int(FamId[:4]) + 7 #The spouse will be as old as the partner or at most 7 years younger
    PersonNr = person_nummer_creation(1, start_date=FamId[:8], stop_year=f"{spouse_age}1231")
    utbildning = generate_education(1, utbildning)
    data = pd.DataFrame()
    data = utbildning.join(kids_info)
    data['PersonNr'] = PersonNr
    data['FamId'] = FamId
    return data

def create_family(personnummer, sample_year, utbildning):
    kids_info = create_children(sample_year, personnummer)
    kids_frames = create_kids_data(sample_year, personnummer, kids_info, utbildning) #dataframe
    #columns=['Barn0_3', 'Barn4_6', 'Barn7_10', 'Barn11_15', 'Barn16_17', 'Barn18plus', 'Barn18_19', 'Barn20plus', 'PersonNr', 'FamId']
    data = pd.DataFrame()
    if len(kids_frames) == 0:
        if random.randint(1,100) > 60: # Probability someone is living alone
            spouse = create_spouse(personnummer, kids_info, utbildning)
        else:
            spouse = None
    else:
        min_family_size = 0
        family_size = random.randint(min_family_size, len(kids_frames)+1) #Bigger family, more likley there's a spouse in the household
        if family_size > 1:
            spouse = create_spouse(personnummer, kids_info, utbildning)
        else:
            spouse = None
    utbildning = generate_education(1, utbildning)
    data = utbildning.join(kids_info)
    data['PersonNr'] = personnummer
    data['FamId'] = personnummer
    if type(spouse) == None:
        data = pd.concat([data, kids_frames])
    else:
        data = pd.concat([data, spouse, kids_frames])
    return data



def generate_family(sample_year, utbildning):
    family_data = pd.DataFrame(columns=['PersonNr','Barn0_3', 'Barn4_6', 'Barn7_10', 'Barn11_15', 'Barn16_17', 'Barn18plus', 'Barn18_19', 'Barn20plus', 'FamId'])
    # birthdates = birth_dates(stopyear=sample_year)
    PersonNr = person_nummer_creation(sample_year)
    family_data = pd.concat([family_data, create_family(PersonNr, sample_year, utbildning)])
    return family_data

