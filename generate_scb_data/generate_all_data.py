def merge_dictionaries(dictionary1, dictionary2):
    dictionary1.update(dictionary2)
    return dictionary1

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# ---------------------------------- DEMOGRAPHICAL VARIABLES --------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# ## Variable Generation
# #### 1. FodelseAr
# This is the birth year it is extracted from the personnummer
#extract first 4 values of personnummer to get the age
def fodelse_ar(personnummer):
    return personnummer[:4]

# #### 2. DodDatum
# Date of death (year,month,day)
import random
from datetime import timedelta


#generate date of death by adding random number of days to the birthday
def dod_datum(sample_year=None):
    if sample_year == None:
        return None
    else:
        if random.randint(1,100) <= 5:
            start = datetime.datetime(sample_year, 1, 1)
            min_days = 1 #minimum number of days to be added to birthday
            max_days = (datetime.datetime(sample_year, 12, 31) - start).days #maximum number of days to be added to birthday (using end of previous year)
            random_days = random.randint(min_days, max_days)
            deathday = start + timedelta(days=random_days)
            deathday = deathday.isoformat().replace('-','')
            return str(deathday)[:8]
        else:
            return None

# #### 3. Alder
# This is the age and can be calculated from birth year in personnummer.
import dateutil.relativedelta
import datetime

#calcuate age using birthday from personnummer
def alder(personnummer, sample_year, death_date=None):
    if death_date == None:        
        today = datetime.datetime(sample_year, 12, 31)
    else:
        today = datetime.date.fromisoformat(death_date)

    birthday = datetime.date.fromisoformat(personnummer[:8])
    age = dateutil.relativedelta.relativedelta(today, birthday)
    years = int(age.years)
    return years

# #### 4. Kon: 
# Sex (Male/Female) - based on 2022 statistics 10.52 million people, 5.3 million men & 5.22 million women so assign 50.38% of the values as M and 49.62% as F.
def kon(personnummer):
    secondlast_digit = int(personnummer[-2])
    woman = [0,2,4,6,8] 
    if secondlast_digit in woman:
        return 2
    else:
        return 1


# #### 5. InvUtvLand: 
# In the case of immigration, the information refers to the country from which the person emigrated and in the case of emigration, the country to which the person immigrates.
# In 2022 - 50,592 people emigrated from Sweden. (about 0.5% of the population)
# In 2022 - 102,436 people immigrated to Sweden. (about 1% of the population)

def get_status(): #indicate whether it is emmigration or immigration, to be used in inv_utv_manad and post_typ

    def inv_utv_land():
        countries = ['India', 'Poland', 'Germany', 'Syria', 'Pakistan', 'Iran', 'Afghanistan', 'Turkey', 'Romania', 'China', 'Iraq', 'Finland', 'USA', 'Russia', 'Netherlands', 'Brazil', 'Denmark', 'UK', 'Italy']
        prob = random.random()

        if prob < 0.005:
            inv_utv = random.choice(countries)
            status = 'Utv' # migrated from Sweden
        elif prob < 0.01:
            inv_utv = random.choice(countries)
            status = 'Inv' # migrated to Sweden
        else:
            inv_utv = None
            status = None

        return inv_utv, status
    
    return inv_utv_land()


# #### 6. InvUtvManad: 
# Year and month for immigration to Sweden and year and month for emigration from Sweden.
def inv_ut_manad(status,personnummer, sample_year, death_date=None):
    if status != None:
        year, month = int(personnummer[:4]), int(personnummer[4:6])
        date = datetime.datetime(year, month, 1)
        min_days = 1 #minimum number of days to be added to birthday
        if death_date == None: 
            max_days = (datetime.datetime(sample_year, 12, 31) - date).days #maximum number of days to be added to birthday (using end of previous year)
        else:
            
            max_days = (datetime.datetime(int(death_date[:4]), 12, 31) - date).days #maximum number of days to be added to birthday (using end of previous year)
            
        random_days = random.randint(min_days, max_days)
        inv_ut_manad = date + timedelta(days=random_days)
        
        return inv_ut_manad.strftime('%Y-%m')
    else:
        return None


# #### 8. FodelseLandnamn
# SCB 2022 list - Sweden, India, Poland, Germany, Syria, Pakistan, Iran, Afghanistan, Turkey, Romania, China, Iraq, Finland, USA, Russia, Netherlands, Brazil, Denmark, UK, Italy, Other 
# Foreign-born citizens make up 20.4% of the population (Syria, Iraq, Finland, Poland, Iran)
# Foreign-background (foreign-born (20.4%) and born in Sweden with both parents born outside of Sweden(6.5%)) make up 26.9%
# Swedish-background (one foreign-born parent) - 7.8%

def fodelse_landnamn(): #birth country of everyone residing in Sweden

    countries = ['India', 'Poland', 'Germany', 'Syria', 'Pakistan', 'Iran', 'Afghanistan', 'Turkey', 'Romania', 'China', 'Iraq', 'Finland', 'USA', 'Russia', 'Netherlands', 'Brazil', 'Denmark', 'UK', 'Italy']
    probability_sweden = 79.60
    random_number = random.uniform(0, 100)
    
    if random_number <= probability_sweden:
        selected_country = 'Sweden'
    else:
        selected_country = random.choice(countries)
    return selected_country

# #### 9. FodelseTid
def fodelse_tid(personnummer):
    return personnummer[:8]


# #### 13. UtlSVBackg
# 1. Person with a foreign background: 11 Born abroad, 12 Domestically born with two foreign-born parents
# 2. Person with Swedish background: 21 Domestic born with one domestic and one foreign-born parent, 22 Domestic born with two domestic-born parents
# When information about the parent's country of birth is missing, the following applies:
# - For a person who was born in Sweden, the parent is assumed to be born in Sweden
# - For a person who was born abroad, the parent is assumed to be born abroad
def utl_sv_bakg(fodelselandnamn, fodelselandnamnfar, fodelselandnamnmor):
    if not fodelselandnamn == 'Sweden' and not fodelselandnamnfar == 'Sweden' and not fodelselandnamnmor == 'Sweden':
        return 11
    elif fodelselandnamn == 'Sweden' and not fodelselandnamnfar == 'Sweden' and not fodelselandnamnmor == 'Sweden':
        return 12
    elif fodelselandnamn == 'Sweden' and fodelselandnamnfar == 'Sweden' and  fodelselandnamnmor == 'Sweden':
        return 22
    else:
        return 21

def generate_demographic(PersonNr, sample_year, birthdaymom="", birthdaydad="", mom_country="", dad_country=""):
    FodelseAr = fodelse_ar(PersonNr)
    DodDatum = dod_datum() # People can only have died during the sample year and not earlier
    InvUtvLand, Status = get_status()
    if DodDatum == None:
        Alder = alder(PersonNr, sample_year)
        InvUtvManad = inv_ut_manad(Status,PersonNr, sample_year)
    else:
        Alder = alder(PersonNr, sample_year, DodDatum)
        InvUtvManad = inv_ut_manad(Status,PersonNr, sample_year, DodDatum)

    if birthdaymom == "": birthdaymom = '19820102-8936' #Default value
    if birthdaydad == "": birthdaydad = '19790102-8936' #Default value
    
    if mom_country == "": mom  = fodelse_landnamn()
    else: mom = mom_country

    if dad_country == "": dad  = fodelse_landnamn()
    else: dad = dad_country
        
    me   = fodelse_landnamn()

    demographic_data = {
        'FodelseAr'             : FodelseAr,
        'DodDatum'              : DodDatum,
        'Alder'                 : Alder,          
        'Kon'                   : kon(PersonNr),
        'InvUtvLand'            : InvUtvLand,
        'InvUtvManad'           : InvUtvManad,
        'PostTyp'               : Status,
        'FodelseLandnamn'       : me,
        'FodelseTidMor'         : fodelse_tid(birthdaymom), 
        'FodelseLandnamnMor'    : mom,
        'FodelseTidFar'         : fodelse_tid(birthdaydad), 
        'FodelseLandnamnFar'    : dad,
        'UtlSvBakg'             : utl_sv_bakg(me,dad,mom) 
                       }
    return demographic_data

















































# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# ------------------------------------ ECONOMICAL VARIABLES ---------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------


import random
import pandas as pd
import numpy as np

def generate_employment_statuses(sample_year):
    #1 = Gainfully employed according to the limit, 16-74 years 
    #5 = Not gainfully employed according to the limit, but with control information from employer or business income during the year 
    #6 = Not gainfully employed, without control information from employer or business income during the year 
    #7 = Gainfully employed, 15 years
    if sample_year <= 2003:
        status = [1, 5, 6]
        probabilities = [0.6, 0.2, 0.2]
    elif sample_year <= 2011:
        status = [1, 5, 6]
        probabilities = [0.7, 0.2, 0.1]
    else:
        status = [1, 5, 6, 7]
        probabilities = [0.69, 0.2, 0.1, 0.01]
    return random.choices(status, probabilities)[0]


def generate_workingtime(SyssStat): #How many work hours/week
    #1 = 0 hours, 2 = 1 – 15 hours, 3 = 16 – 19 hours, 4 = 20 – 34 hours, 5 = 35 – w hours, 9 = Uppgift
    if SyssStat == 1 or SyssStat == 7 or SyssStat == 5:
        status = [2,3,4,5,9]
        probabilities = [0.1, 0.15, 0.25, 0.45, 0.05]
        ArbTid = random.choices(status, probabilities)[0]
    else:
        ArbTid = 1
    return ArbTid 


def generate_job(ArbTid): #What kind of work the person is involved in
    #0 = Persons without control duties 
    #1 = Sailors 
    #2 = Employees (excl. seamen) 
    #4 = Entrepreneurs 
    #5 = Entrepreneurs in own AB
    if ArbTid == 1:
        YrkStalln = 0
    else:
        status = [1,2,4,5]
        probabilities = [0.05, 0.7, 0.2, 0.05]
        YrkStalln = random.choices(status, probabilities)[0]
    return YrkStalln


def generate_income(ArbTid): #How much money each() work place generates
    mean=1000
    std_dev=500
    KU1lnk, KU2lnk, KU3lnk = 0,0,0

    if ArbTid != 1:  #The person has some income
        # Generate incomes from a normal distribution with the specified mean and standard deviation
        random_number = random.random()
        if random_number < 0.1: # The person will have 3 sources of income
            incomes = [ max(0, int(np.random.normal(mean, std_dev))), 
                        max(0, int(np.random.normal(mean, std_dev))),
                        max(0, int(np.random.normal(mean, std_dev)))]
            incomes = sorted(incomes)
            KU1lnk = incomes[0]
            KU2lnk = incomes[1]
            KU3lnk = incomes[2]
        elif random_number < 0.5: #The person will have 2 sources of income
            incomes = [ max(0, int(np.random.normal(mean, std_dev))), 
                        max(0, int(np.random.normal(mean, std_dev)))]
            incomes = sorted(incomes)
            KU1lnk = incomes[0]
            KU2lnk = incomes[1]
        else: # The person has 1 source of income
            KU1lnk = max(0, int(np.random.normal(mean, std_dev)))
    return KU1lnk, KU2lnk, KU3lnk


def generate_total_incomes(KU1lnk, KU2lnk, KU3lnk): #Total income from work and other allowances, such as CSN or "bostadsbidrag"
    total_income = KU1lnk+KU2lnk+KU3lnk
    if total_income > 0: #You have some income
        extra_income = random.randint(0, int(total_income*0.2)) #You could have up to 20% of your normal income as extra
    else: #You have no income, you could be living from some kind of allowance, like CSN
        extra_income = random.randint(100, 1500) #Up to 15.000 SEK per month 

    Raks_SummaInk = total_income + extra_income
    return Raks_SummaInk


def generate_labor_connection(YrkStalln): # How well the person is connected to the market
    if YrkStalln == 0:
        Raks_EtablGrad = 'NULL'
    else:
        Raks_EtablGrad = 0 if random.random() > 0.5 else 1
    return Raks_EtablGrad   


def generate_Forvink(KU1lnk, KU2lnk, KU3lnk):
    Raks_Forvink = KU1lnk+KU2lnk+KU3lnk
    return Raks_Forvink

#Work ties should be used here
def generate_main_labor_connection(YrkStalln):
    #1 Full time employed
    #2 Newly hired
    #3 Fired
    #4 Part time employed
    #5 Combination
    #6 Entrepreneur
    #7 Unemployed
    Raks_Huvudanknytning = None
    if YrkStalln == 0:
        Raks_Huvudanknytning = 7
    else:
        if 0 < YrkStalln < 4:
            status = [1,2,3,4]
            probabilities = [0.5,0.2,0.1,0.2]
            Raks_Huvudanknytning = random.choices(status, probabilities)[0]
        else:
            Raks_Huvudanknytning = 5 if random.random() > 0.5 else 6
                
    return Raks_Huvudanknytning 


def generate_economic(sample_year, is_kid=False):
    if is_kid:
        employment_data = {
        'SyssStat'              : 6, #Not working 
        'ArbTid'                : 1, #1 - 0 hours worked/week
        'YrkStalln'             : 0, #0 - No information about workplace (have no work)
        'KU1lnk'                : 0, #Biggest source of income
        'KU2lnk'                : 0, #Second biggest source of income
        'KU3lnk'                : 0, #Third biggest source of income
        'Raks_SummaInk'         : 100, #1000kr/per month for kids in highschool during school season
        'Raks_Huvudanknytning'  : 7, #Which title, full time employed, newly hired etc, 7 = Without work
        'Raks_EtablGrad'        : 'NULL', #How well connected the person is to the market, 0 well established, 1 poorly established, NULL don't know
        'Raks_Forvink'          : 0 #Income from work
                        }   
    else:
        SyssStat = generate_employment_statuses(sample_year)
        ArbTid = generate_workingtime(SyssStat)
        YrkStalln = generate_job(ArbTid)
        KU1lnk, KU2lnk, KU3lnk = generate_income(ArbTid)
        Raks_SummaInk = generate_total_incomes(KU1lnk,KU2lnk, KU3lnk)
        Raks_EtablGrad = generate_labor_connection(YrkStalln)
        Raks_Forvink = generate_Forvink(KU1lnk, KU2lnk, KU3lnk)
        Raks_Huvudanknytning = generate_main_labor_connection(YrkStalln)

        employment_data = {
            'SyssStat'              : SyssStat,
            'ArbTid'                : ArbTid,
            'YrkStalln'             : YrkStalln,
            'KU1lnk'                : KU1lnk,
            'KU2lnk'                : KU2lnk,
            'KU3lnk'                : KU3lnk,
            'Raks_SummaInk'         : Raks_SummaInk,
            'Raks_Huvudanknytning'  : Raks_Huvudanknytning,
            'Raks_EtablGrad'        : Raks_EtablGrad,
            'Raks_Forvink'          : Raks_Forvink
                            }    
    return employment_data

















































# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# ----------------------------------- EDUCATIONAL VARIABLES ---------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------


import csv
def utbildning_csv_to_dict(file_path):
    # Open the CSV file
    file_path = file_path + ".csv"
    with open(file_path, 'r') as csv_file:
        # Create a CSV reader with DictReader
        csv_reader = csv.DictReader(csv_file)
        # Convert the CSV data into a list of dictionaries
        education_list = list(csv_reader)
    for item in education_list:
        item['Inriktningskoder_SUN_2020'] = item['Inriktningskoder_SUN_2020'].split(', ')
        item['Nivakoder_SUN_2020'] = item['Nivakoder_SUN_2020'].split(', ')
    return education_list

possible_educations_by_length = ["resources/utbildning3yearsorless", "resources/utbildning5yearsorless", "resources/utbildning6yearsorless"]
all_educations = [utbildning_csv_to_dict(k) for k in possible_educations_by_length]


import random
def generate_education(sample_year, PersonNr, Kommun, is_kid=False): 
    age = sample_year - int(PersonNr[:4])
    if is_kid or age < 17: #Kid will have elementary school education at most
        education = {
            'Sun2000niva_old'   : 2,
            'SUN2000niva'       : "2",
            'SUN2000Inr'        : "010a" if random.random() > 0.5 else "010x",
            'SUN2000Grp'        : "Grundskoleutbildning och motsvarande",
            'ExamAr'            : sample_year, #You graduate elementary at the age of 15/16 in sweden (depending on which part of the year you're born)
            'ExamKommun'        : Kommun                                       
        }
        return education
    if age > 24: #The person could have any education in the list
        examAge = age-24
        education = all_educations[2]
    elif age > 23: #The person could have any education that requires 5 years or less
        examAge = age-23
        education = all_educations[1]
    else: #The person has the an education that requires 3 years or less after elementary
        examAge = age-18
        education = all_educations[0] 

    random_number = int(random.random() * 10000000)

    number_of_educations = len(education)
    my_education = education[random_number % number_of_educations]
    

    codes = my_education['Nivakoder_SUN_2020']
    number_of_codes = len(my_education['Nivakoder_SUN_2020'])

    level = codes[random_number % number_of_codes]
    Sun2000niva_old = int(level[0])
    
    SUN2000Niva = level
    SUN2000Grp = my_education['Utbildningsgrupper_2020']
    
    
    number_of_specials = len(my_education['Inriktningskoder_SUN_2020'])
    specials = my_education['Inriktningskoder_SUN_2020']
    speciality_code = specials[random_number % number_of_specials]
    SUN2000Inr = speciality_code
    if sample_year - (sample_year-examAge) < 1:
        ExamAr = sample_year
    else:
        ExamAr = random.randint(sample_year-(examAge),sample_year)

    #FANID IS PARTNER SIBLING 

    #FIND PARENT CHILD and find relationsships

    education = {
            'Sun2000niva_old'   : Sun2000niva_old,
            'SUN2000niva'       : SUN2000Niva,
            'SUN2000Inr'        : SUN2000Inr,
            'SUN2000Grp'        : SUN2000Grp,
            'ExamAr'            : ExamAr,
            'ExamKommun'        : Kommun
    }
    return education

















































# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# ----------------------------------- FAMILY VARIABLES --------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------


import random
numbers = [str(x) for x in range(10)]
def get_date(start_date = '19250101', stop_date='20191231'):
    # datetime for start date
    start = datetime.date.fromisoformat(start_date)

    # datetime for stop date
    stop = datetime.date.fromisoformat(stop_date)

    max_days = (stop - start).days
    # take random amount of days after the starting date
    days_after_start = random.randint(0, max_days)

    date = start + datetime.timedelta(days = days_after_start)
    date = date.isoformat().replace('-','')
    return date


taken_social_security_numbers = {'0'}
def person_nummer_creation(sample_year, start_date=None, stop_year="", gender=3):        
    if stop_year == "":
        end_date = str(sample_year-15) #People need to be atleast 15 to legally live alone in Sweden
        end_date = end_date + "1231"
    else:
        end_date = stop_year
    if start_date == None:
        start_date = f"{sample_year-90}0101" #A person can be up to 90 years old when they are first selected in the first year of data creation
 
    while True:
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
            last_4 = str(random.randint(10000, 99999))[1:]
        
        birthdate = get_date(start_date, end_date)
        social_security_number = birthdate + "-" + last_4
        if social_security_number not in taken_social_security_numbers:
            taken_social_security_numbers.add(social_security_number)
            return social_security_number

def update_kid_categories(parent_dict, kid_info_dict, sample_year): #Updates the keys before csv creation incase people was 15 and is now 16 etc
    parent_dict['Barn0_3'], parent_dict['Barn4_6'], parent_dict['Barn7_10'], parent_dict['Barn11_15'] = 0,0,0,0
    parent_dict['Barn16_17'], parent_dict['Barn18plus'], parent_dict['Barn18_19'], parent_dict['Barn20plus'] = 0,0,0,0
    for k,v in kid_info_dict.items():
        kid_age = int(k)
        number_of_kids = v
        if kid_age >= 0 and kid_age < 4:
            for _ in range(number_of_kids):
                parent_dict['Barn0_3'] +=1
        elif kid_age > 3 and kid_age < 7:
            for _ in range(number_of_kids):
                parent_dict['Barn4_6'] +=1
        elif kid_age > 6 and kid_age < 11:
            for _ in range(number_of_kids):
                parent_dict['Barn7_10'] +=1
        elif kid_age > 10 and kid_age < 16:
            for _ in range(number_of_kids):
                parent_dict['Barn11_15'] +=1
        elif kid_age > 15 and kid_age < 18: #Barn16_17
            for _ in range(number_of_kids):
                parent_dict['Barn16_17'] +=1
        elif sample_year <= 2004 and kid_age > 17: #Barn18plus
            for _ in range(number_of_kids):
                parent_dict['Barn18plus'] += 1
        elif sample_year > 2004 and kid_age > 17 and kid_age < 20: #Barn18_19
            for _ in range(number_of_kids):
                parent_dict['Barn18_19'] += 1
        elif sample_year > 2004 and kid_age > 19: #Barn20plus
            for _ in range(number_of_kids):
                parent_dict['Barn20plus'] += 1


def create_children(sample_year, PersonNr, is_kid=False):
    barn = {
            'Barn0_3'       : 0,
            'Barn4_6'       : 0,
            'Barn7_10'      : 0,
            'Barn11_15'     : 0,
            'Barn16_17'     : 0,
            'Barn18plus'    : 0,
            'Barn18_19'     : 0,
            'Barn20plus'    : 0,
            'kid_info'      : {}
               }
    if is_kid:
        return barn

    #roughly 68% of households are childless 
    # https://www.scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/statistiknyhet/befolkningsstatistik-helaret-20222/
    if random.randint(1,100) > 65:
        mean = 1.81  # Mean of the normal distribution 
        stddev = 1.3  # Standard deviation of the normal distribution
        number_of_kids = int(random.gauss(mean, stddev))
        if number_of_kids < 1:
            number_of_kids = 1

        person_age = int(sample_year) - int(PersonNr[:4])
        min_age = (person_age - 60) if person_age > 60 else 0 #Max age to get newborns is 60
        max_age = person_age - 14
        for _ in range(number_of_kids):
            kid_age = random.randint(min_age, max_age)
            kid_age_t = (kid_age - min_age) / ((max_age - min_age))
            kid_age_t = kid_age_t * kid_age_t
            kid_age = int(kid_age_t * (max_age - min_age) + min_age)
            if kid_age in barn['kid_info']:
                barn['kid_info'][kid_age] +=1
            else:
                barn['kid_info'][kid_age] = 1
        for k, v in barn['kid_info'].items(): #No more than 3 kids per age
            if v > 3:
                barn['kid_info'][k] = 3
            
    return barn


def make_kid_family_frame(PersonNr, FamId, is_Kid, sample_year): #Used for kids that just turned 15 and have special work/economic
    kids = create_children(sample_year, PersonNr, is_kid=is_Kid)
    data = kids
    data['PersonNr'] = PersonNr
    data['FamId'] = FamId
    data['spouse'] = dict()
    data['my_kids_living_at_home'] = dict()
    return data


def make_twins(age, sample_year):
    year_born = sample_year - age
    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
    return [kid1, kid2]

def make_triplets(age, sample_year):
    year_born = sample_year - age
    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
    kid3 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
    return [kid1, kid2, kid3]


def create_kids_data(sample_year, FamId, kids_info):
    kids_list = [[],[],[],[],[]]
    for k,v in kids_info['kid_info'].items():
        kid_age = k
        number_of_kids = v
        if kid_age > 15 and kid_age < 18: #Barn16_17
            for _ in range(number_of_kids):
                kids_list[0].append(kid_age)
        elif sample_year <= 2004 and kid_age > 17: #Barn18plus
            for _ in range(number_of_kids):
                kids_list[2].append(kid_age)
        elif sample_year > 2004 and kid_age > 17 and kid_age < 20: #Barn18_19
            for _ in range(number_of_kids):
                kids_list[1].append(kid_age)
        elif sample_year > 2004 and kid_age > 19: #Barn20plus
            for _ in range(number_of_kids):
                kids_list[3].append(kid_age)
        elif kid_age == 15: #Barn 15
            for _ in range(number_of_kids):
                kids_list[4].append(kid_age)

    kids_list = [sorted([num for num in sublist]) for sublist in kids_list] # Sorts the kids by age for each group
    kids_in_range = kids_list[:2]       #Barn16_17 and Barn18_19
    kids_plus = kids_list[2:4]           #Barn18plus and Barn20plus
    kids_15 = kids_list[-1] #Barn 15
    
    all_kids = []
    if len(kids_15) == 1:
        kid_age = kids_15[0]
        year_born = sample_year - kid_age
        kid = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
        all_kids.append(make_kid_family_frame(kid, FamId, is_Kid=True, sample_year=sample_year))
    elif len(kids_15) == 2:
        kid_age = kids_15[0]
        kid_numbers = make_twins(kid_age, sample_year)
        for kid_number in kid_numbers:
            all_kids.append(make_kid_family_frame(kid_number, FamId, is_Kid=True, sample_year=sample_year))
    elif len(kids_15) == 3:
        kid_age = kids_15[0]
        kid_numbers = make_triplets(kid_age, sample_year)
        for kid_number in kid_numbers:
            all_kids.append(make_kid_family_frame(kid_number, FamId, is_Kid=True, sample_year=sample_year))



    #Barn16_17 and Barn18_19
    for kids in kids_in_range:
        if len(kids) == 1:
            kid_age = kids[0]
            year_born = sample_year - kid_age
            kid = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
            all_kids.append(make_kid_family_frame(kid, FamId, is_Kid=True, sample_year=sample_year))
        
        elif len(kids) == 2:
            age1, age2 = kids[0], kids[1]
            if age1 == age2: #Twins 16 16
                year_born = sample_year - age1
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
                kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
            else: # 16 17
                year_born1 = sample_year - age2
                year_born2 = sample_year - age1
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kid born jan - june year 1
                kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kid born atleast 10 months later
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year))
        
        elif len(kids) == 3:
            age1, age2, age3 = kids[0], kids[1], kids[2]
            if age1 == age2:
                if age2 == age3: #Triplets
                    year_born = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
                    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                    kid3 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                else: # First kid born alone, other 2 kids are twins 16 16 17
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kids born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=kid2[:8], stop_year=kid2[:8])
            else: # First kids are twins other is single 16 17 17
                year_born1 = sample_year - age3
                year_born2 = sample_year - age1
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kids born jan - june year 1
                kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                kid3 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kid born atleast 10 months later
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid3, FamId, is_Kid=True, sample_year=sample_year))


    #Barn18plus and Barn20plus
    for kids in kids_plus:
        if len(kids) == 1: # 22
            year_born = sample_year - kids[0]
            kid = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
            all_kids.append(make_kid_family_frame(kid, FamId, is_Kid=True, sample_year=sample_year))
        
        elif len(kids) == 2:
            age1, age2 = kids[0], kids[1]
            if age1 == age2: #Twins 22 22
                year_born = sample_year - age1
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
                kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
            else:
                if age2 - age1 > 1: # More than 1 year apart from each other 20 22
                    year_born1 = sample_year - age2
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231")
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231")
                else: # Within 1 years of each other 20 21
                    year_born1 = sample_year - age2
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kid born atleast 10 months later
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year))

        elif len(kids) == 3:
            age1, age2, age3 = kids[0], kids[1], kids[2]
            if age1 == age2 and age2 == age3: #Triplets 20 20 20
                year_born = sample_year - age1
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
                kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                kid3 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])

            elif age1 == age2: #The 2 youngest are twins oldest is singlet 
                if age3 - age1 > 1: #More than 1 year apart 20 20 22
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231")
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231")
                    kid3 = person_nummer_creation(sample_year, start_date=kid2[:8], stop_year=kid2[:8])
                else: #Within 1 year apart 20 20 21
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kids born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=kid2[:8], stop_year=kid2[:8])

            elif age2 == age3: #The 2 oldest are twins youngest is singlet 
                if age3 - age1 > 1: #More than 1 year apart 20 22 22
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231")
                    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231")
                else: #Within 1 year apart 20 21 21
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kids born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Third kid born atleast 10 months later

            elif age2 - age1 == 1: 
                if age3 - age2 == 1: # 20 21 22
                    year_born1 = sample_year-age3
                    year_born2 = sample_year-age2
                    year_born3 = sample_year-age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0210") # First kid born jan - feb year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}0210") # Second kid born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born3}0101", stop_year=f"{year_born3}1231") # Third kid born atleast 10 months later
                else: # 20 21 23
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age2
                    year_born3 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231") # Second kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}0630") # Third kid born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born3}0401", stop_year=f"{year_born3}1231") # First kid born whenever
            else:
                if age3 - age2 == 1: #20 22 23
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age2
                    year_born3 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kid born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born3}0101", stop_year=f"{year_born3}1231") # Third kid born whenever
                else: # 20 22 24
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age2
                    year_born3 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231") # Third kid born whenever
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231") # Third kid born whenever
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born3}0101", stop_year=f"{year_born3}1231") # Third kid born whenever
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid3, FamId, is_Kid=True, sample_year=sample_year))

    return all_kids

import math
def create_spouse(FamId, kids_info, sample_year):
    spouse_age = sample_year - int(FamId[:4])
    partner_age = math.ceil((spouse_age/2) + 7) #The spouse will follow half your age + 7 rule
    if partner_age < 15:
        partner_age = 15
    PersonNr = person_nummer_creation(1,start_date=FamId[:8], stop_year=f"{sample_year-partner_age}1231")
    spouse = kids_info
    spouse['PersonNr'] = PersonNr
    spouse['FamId'] = FamId
    return spouse


def generate_family(sample_year): #Creates a household
    PersonNr = person_nummer_creation(sample_year) #What social security number does the person have
    kids_info = create_children(sample_year, PersonNr) #Does the person have kids
    kid_info = kids_info['kid_info']    
    data = kids_info
    data['PersonNr'] = PersonNr
    data['FamId'] = PersonNr
    data['kid_info'] = kid_info
    #Default will have no kids living at home and no spouse
    data['my_kids_living_at_home'] = dict()
    data['spouse'] = dict()
    family_dicts = [data]


    kids_frames = create_kids_data(sample_year, PersonNr, kids_info) #Creates data for people living at home age > 15
    if len(kids_frames) == 0:
        if random.randint(1,100) > 60: # Probability someone is living alone
            spouse = create_spouse(PersonNr, kids_info, sample_year)
            family_dicts.append(spouse)
            #The spouses will know about each other and share dictionary of people living at home
            spouse['kid_info'] = kid_info
            spouse['spouse'] = data
            data['spouse'] = spouse
            spouse['my_kids_living_at_home'] = data['my_kids_living_at_home']
    else:
        for kid in kids_frames:
            data['my_kids_living_at_home'][kid['PersonNr']] = kid
        family_dicts = family_dicts + kids_frames
        min_family_size = 0
        family_size = random.randint(min_family_size, len(kids_frames)+1) #Bigger family, more likley there's a spouse in the household
        if family_size > 1:
            spouse = create_spouse(PersonNr, kids_info, sample_year)
            #The spouses will know about each other and share dictionary of people living at home
            spouse['kid_info'] = kid_info
            spouse['spouse'] = data
            data['spouse'] = spouse
            spouse['my_kids_living_at_home'] = data['my_kids_living_at_home']
            family_dicts.append(spouse)
    
    return family_dicts

















































# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# ----------------------------------- GEOGRAPHICAL VARIABLES --------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------


import random
import json
scbinternal_fastlopnr = {}
scbinternal_fastlopnr_values = set([])


with open('resources/county_dict.json', 'r') as json_file:
    counties_with_municipals = json.load(json_file)


with open('resources/tatorter_in_municipals_dict.json', 'r') as json_file:
    tatorter_in_municipals = json.load(json_file)


with open('resources/forsamling_dict.json', 'r') as json_file:
    forsamlingar_in_municipals = json.load(json_file)


with open('resources/district_codes_from_Forsamling_dict.json', 'r') as json_file:
    districtcodes_from_Forsamling = json.load(json_file)


def generate_syntethic_FastBet(municipal_name):
    tatorter = tatorter_in_municipals[municipal_name]
    tatort = tatorter[random.randint(0, len(tatorter)-1)] #Chooses randomly which "Tätort" the person lives in of the ones available to that municipal
    number = random.randrange(1000000, 400000000)
    FastBetNr = str(int(str(number)[1:4]))
    last3 = str(int(str(number)[4:]))
    if int(FastBetNr)/4 > 30: #It is quite likely that there are numbers followed by the first one
        FastBetNr += ":" + last3

    FastBet = f"{municipal_name} {tatort} {number}"
    return FastBet


def generate_synthetic_FastLopNr(FastBet):
    if FastBet in scbinternal_fastlopnr: #If there are people in the same new FastBet then they should have the same FastLopNr as well
        return scbinternal_fastlopnr[FastBet]
    else:
        while True:
            FastLopNr = random.randrange(100_0000_000, 9_999_999_999) # Limited to 100 million households
            FastLopNr = str(FastLopNr)[1:]
            if FastLopNr not in scbinternal_fastlopnr_values:
                scbinternal_fastlopnr_values.add(FastLopNr)
                scbinternal_fastlopnr[FastBet] = FastLopNr
                return FastLopNr


def generate_synthetic_Distriktskod(Forsamling):
    possible_districts = districtcodes_from_Forsamling[Forsamling]
    return possible_districts[random.randint(0, len(possible_districts)-1)]


def generate_county():
    counties = list(counties_with_municipals.keys())
    Lan = counties[random.randint(0, len(counties)-1)] #Chooses a random Lan to begin with
    return Lan


def generate_municipal(Lan):
    municipals = counties_with_municipals[Lan]
    Kommun = municipals[random.randint(0, len(municipals)-1)] #Chooses a random Kommun in that county
    return Kommun


def generate_forsamling(Kommun):
    forsamlingar = forsamlingar_in_municipals[Kommun]
    Forsamling = forsamlingar[random.randint(0, len(forsamlingar)-1)] #Chooses a random municipal in that county
    return Forsamling


def generate_geographical():
    Lan                 = generate_county()
    Kommun              = generate_municipal(Lan)
    Forsamling          = generate_forsamling(Kommun)
    Distriktskod        = generate_synthetic_Distriktskod(Forsamling) #Chooses a random district_code based on the Forsamling
    FastBet             = generate_syntethic_FastBet(Kommun) #Generates a random Fastighetsbeteckning based on municipal and places to live in that municipal
    FastLopNr           = generate_synthetic_FastLopNr(FastBet) #Generates a random FastLopNr that is unique to that FastBet or returns the already existing if the FastBet already exists
    geographical_data   = {
                            'Lan'           : Lan,
                            'Kommun'        : Kommun,
                            'Forsamling'    : Forsamling,
                            'Distriktskod'  : Distriktskod,
                            'FastLopNr'     : FastLopNr,
                            'FastBet'       : FastBet
                          }
    return geographical_data

















































# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# --------------------------------- WORKING TIES VARIABLES ----------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------


CfarNumbers = {}
CfarNumbers_values = set()
def generate_CfarNr_LISA(PeOrgNr): #Will generate an arbitrary unique 8 digit number
    if PeOrgNr in CfarNumbers:
        return CfarNumbers[PeOrgNr]
    else:
        while True:
            CfarNr_LISA = str(random.randint(100_000_000, 999_999_999))
            if CfarNr_LISA not in CfarNumbers_values:
                CfarNumbers_values.add(CfarNr_LISA)
                CfarNumbers[PeOrgNr] = CfarNr_LISA
                return CfarNr_LISA

#Numbers taken from SCB, from year 2000 and onward it's pretty stable at 5.1%
AstNr_percentages_by_year = {
                            1990: 0.107, 1991: 0.093, 1992: 0.097, 
                            1993: 0.090, 1994: 0.080, 1995: 0.076,
                            1996: 0.070, 1997: 0.075, 1998: 0.069,
                            1999: 0.050}

AstNumbers = set()
def generate_AstNr_LISA(YrkStalln, sample_year): #Gives a number to specify what job the person has, like a contractor, teacher, accountant etc
    if YrkStalln == 1: #The person is a sailor
        return "99993"
    percentage = 0.051
    if 1989 < sample_year < 2000:
        percentage = AstNr_percentages_by_year[sample_year]
    
    random_number = random.random()
    if random_number < percentage and YrkStalln > 2: #5% of people have a number in these lines
        special_numbers = ["99980","99981","99982","99983","99984","99985","99986","99987","99988","99989","99990","99991","99992","99994","99996","99998","99999"]
        return special_numbers[random.randint(0,len(special_numbers)-1)]
    
    number_of_jobs = len(AstNumbers)
    if number_of_jobs > 0: # Chance to use an already existing number
        if random_number < number_of_jobs / (number_of_jobs + 100):
            AstNr_LISA = AstNumbers.pop() #Takes random item in the set
            AstNumbers.add(AstNr_LISA) #Put it back in
            return AstNr_LISA
    #Create new AstNr
    AstNr_LISA = str(random.randint(100001, 999979))[1:]
    AstNumbers.add(AstNr_LISA)
    return AstNr_LISA


PeOrgNumbers = set()
def generate_PeOrgNr(personnummer, YrkStalln): # 000000-0000 - 999999-9999
    if YrkStalln == 5: #The person is an Entrepreneur in own AB and the organisation number is the person's personnumber
        PeOrgNumbers.add(personnummer[2:])
        return personnummer[2:]
    
    number_of_jobs = len(PeOrgNumbers)
    random_number = random.random()
    if number_of_jobs > 0: # Chance to use an already existing number
        if random_number < number_of_jobs / (number_of_jobs + 100):
            PeOrgNr = PeOrgNumbers.pop() #Takes random item in the set
            PeOrgNumbers.add(PeOrgNr) #Put it back in
            return PeOrgNr

    #Generate a new job or accidentaly choose an already existing
    PeOrgNr = str(random.randint(10000000000, 99999999999))
    PeOrgNr = PeOrgNr[1:7] + "-" + PeOrgNr[7:]
    PeOrgNumbers.add(PeOrgNr)
    return PeOrgNr


def generate_company(personnummer, kommunnamn, lansnamn, sample_year, prefix="", YrkStalln="", no_income=False):
    #If you have no income, then you will not be working for a company either
    if no_income:
        work_data = {
                    f'{prefix}PeOrgNr'   : "-",
                    f'{prefix}CfarNr'    : "-",
                    f'{prefix}AstNr'     : "-",
                    f'{prefix}AstKommun' : "0000",
                    f'{prefix}AstLan'    : "00",
                    f'{prefix}YrkStalln' : "0",
                    }     
    else:
        PeOrgNr = generate_PeOrgNr(personnummer, YrkStalln)
        Cfar_Nr = generate_CfarNr_LISA(PeOrgNr)
        AstNr = generate_AstNr_LISA(YrkStalln, sample_year)
        if  1 < YrkStalln < 5:
            YrkStalln = 2 if random.random() > 0.8 else 4 #Most people are employes

        work_data = {
                    f'{prefix}PeOrgNr'   : PeOrgNr,
                    f'{prefix}CfarNr'    : Cfar_Nr,
                    f'{prefix}AstNr'     : AstNr,
                    f'{prefix}AstKommun' : kommunnamn,
                    f'{prefix}AstLan'    : lansnamn,
                    f'{prefix}YrkStalln' : YrkStalln,
                    }     
    return work_data

def generate_work(personnummer, county, economicstatus, sample_year, YrkStalln, is_kid=False):
    #Generates which municipal(s) the person works in based on county
    Kommun = generate_municipal(county)
    
    #If it is a newly turned 15 year old, they will have no workplace(s)
    if is_kid:
        prefix_working_ties1 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU1", YrkStalln="0", no_income=True) #Yrkstallning hardcoded needs FIX
        prefix_working_ties2 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU2", YrkStalln="0", no_income=True) #Yrkstallning hardcoded needs FIX
        prefix_working_ties3 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU3", YrkStalln="0", no_income=True) #Yrkstallning hardcoded needs FIX
        biggest_data = {
            'CfarNr_LISA' : prefix_working_ties1['KU1CfarNr'],
            'ArbstId' : (prefix_working_ties1['KU1CfarNr'])+(prefix_working_ties1['KU1AstNr'])+(prefix_working_ties1['KU1AstKommun'])+(prefix_working_ties1['KU1PeOrgNr']),
            'AstNr_LISA' : prefix_working_ties1['KU1AstNr'],
            'AstKommun' : prefix_working_ties1['KU1AstKommun'],
            'AstLan' : prefix_working_ties1['KU1AstLan']
        }
    else:
        if economicstatus[0] > 0:
            Kommun = generate_municipal(county)
            prefix_working_ties1 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU1", YrkStalln=YrkStalln) #Yrkstallning hardcoded needs FIX
        else:
            prefix_working_ties1 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU1", YrkStalln="0", no_income=True) #Yrkstallning hardcoded needs FIX

        if economicstatus[1] > 0:
            Kommun = generate_municipal(county)
            prefix_working_ties2 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU2", YrkStalln=YrkStalln) #Yrkstallning hardcoded needs FIX
        else:
            prefix_working_ties2 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU2", YrkStalln="0", no_income=True) #Yrkstallning hardcoded needs FIX
        if economicstatus[2] > 0:
            Kommun = generate_municipal(county)
            prefix_working_ties3 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU3", YrkStalln=YrkStalln) #Yrkstallning hardcoded needs FIX
        else:
            prefix_working_ties3 = generate_company(personnummer, Kommun, county, sample_year, prefix="KU3", YrkStalln="0", no_income=True) #Yrkstallning hardcoded needs FIX

        #KU1 will never be lower than KU2 and KU3
        biggest_data = {
            'CfarNr_LISA' : prefix_working_ties1['KU1CfarNr'],
            'ArbstId' : (prefix_working_ties1['KU1CfarNr'])+(prefix_working_ties1['KU1AstNr'])+(prefix_working_ties1['KU1AstKommun'])+(prefix_working_ties1['KU1PeOrgNr']),
            'AstNr_LISA' : prefix_working_ties1['KU1AstNr'],
            'AstKommun' : prefix_working_ties1['KU1AstKommun'],
            'AstLan' : prefix_working_ties1['KU1AstLan']
        }
      
    working_data = merge_dictionaries(merge_dictionaries(merge_dictionaries(biggest_data, prefix_working_ties1), prefix_working_ties2), prefix_working_ties3)
    return working_data

















































# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------- GENERATE ALL DATA ----------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
def generate_household(sample_year=2019):
    family_members = generate_family(sample_year) #Generat the people living there

    Geographical = generate_geographical() #Where are they living
    Lan = Geographical['Lan']
    data = []
    for member in family_members:
        PersonNr = member['PersonNr']
        Utbildning = generate_education(sample_year, PersonNr, Geographical['Kommun']) #Every person in the house will have graduated from the same Kommun

        Demographic = generate_demographic(PersonNr, sample_year) #Demographic data, where they are born, when parents were born etc
        Economic = generate_economic(sample_year) #What kind of income does the person have

        income = [Economic['KU1lnk'], Economic['KU2lnk'], Economic['KU3lnk']]
        Work = generate_work(PersonNr, Lan, income, sample_year, Economic['YrkStalln'], is_kid=False) #Where, if the person works, does the person work

        t = merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(member, Utbildning),Geographical), Demographic), Economic), Work) #Turn it all into a single dictionary
        data.append(t)    
    return data


def generate_data(amount, sample_year=2019): 
    """
    Parameters
    ----------
    amount : integer
        The amount of households you want to generate.
    
    sample_year : integer
        The year you want to pretend it is (different years may create different data).

    Returns
    -------
    data: dictionary
        Dictionary with the data for all people

    """
    data = {}
   
    print(f"{0}/{amount}")
    for i in range(amount):
        if (i+1) % 10000 == 0:
            print(f"{i+1}/{amount}")
        household = generate_household(sample_year)
        for person_in_household in household:
            PersonNr = person_in_household['PersonNr']
            data[PersonNr] = person_in_household  
    
    return data


def generate_data_frame(data, sample_year):
    for d in data:
        update_kid_categories(d, d['kid_info'], sample_year) #Updates kids categories from kid_info dictionary
    csv_columns =   [ #We will only use these keys in the dictionary when creating the dataframe
    'PersonNr', 'Lan', 'Kommun', 'Forsamling', 'Distriktskod',
    'FastLopNr', 'FastBet', 'Barn0_3', 'Barn4_6', 'Barn7_10',
    'Barn11_15', 'Barn16_17', 'Barn18plus', 'Barn18_19',
    'Barn20plus', 'FamId', 'Sun2000niva_old', 'SUN2000niva',
    'SUN2000Inr', 'SUN2000Grp', 'ExamAr', 'ExamKommun',
    'CfarNr_LISA', 'ArbstId', 'AstNr_LISA', 'AstKommun',
    'AstLan', 'KU1PeOrgNr', 'KU1CfarNr', 'KU1AstNr',
    'KU1AstKommun', 'KU1AstLan', 'KU1YrkStalln', 'KU2PeOrgNr',
    'KU2CfarNr', 'KU2AstNr', 'KU2AstKommun', 'KU2AstLan',
    'KU2YrkStalln', 'KU3PeOrgNr', 'KU3CfarNr', 'KU3AstNr',
    'KU3AstKommun', 'KU3AstLan', 'KU3YrkStalln', 'FodelseAr',
    'DodDatum', 'Alder', 'Kon', 'InvUtvLand', 'InvUtvManad',
    'PostTyp', 'FodelseLandnamn', 'FodelseTidMor',
    'FodelseLandnamnMor', 'FodelseTidFar',
    'FodelseLandnamnFar', 'UtlSvBakg', 'SyssStat', 'ArbTid',
    'YrkStalln', 'KU1lnk', 'KU2lnk', 'KU3lnk',
    'Raks_SummaInk', 'Raks_Huvudanknytning', 'Raks_EtablGrad',
    'Raks_Forvink']
    relevant_data = [{key: d[key] for key in csv_columns} for d in data] #Removes unwanted keys for csv creation
    return pd.DataFrame(relevant_data)

import os
def chunk_list(input_list, chunk_size=20000): 
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def dict_to_csvs(dict_data, sample_year=1990, chunk_csv = True):
    folder_name = "synthetic_scb_data"
    if not os.path.exists(folder_name):
        print(f"Creating folder to store the data called {folder_name}")
        os.makedirs(folder_name)

    sliced_dict_data = list(dict_data.values()) #Turns big dictionary (our datastructure) into list of just the values
    if chunk_csv:
        sliced_dict_data = chunk_list(sliced_dict_data)

    number_of_times = len(sliced_dict_data)
    update_frequency = int(number_of_times/10)+1 if int(number_of_times/10) > 0 else 2
    
    i = 1
    print(f"Creating {number_of_times} csv(s)")
    
    for chunk in sliced_dict_data:
        if i % update_frequency == 0:
            print(f"{i}/{number_of_times}")

        subfolder_name = f"synthetic_scb_data_{sample_year}"
        subfolder_path = os.path.join(folder_name, subfolder_name)

        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        data = generate_data_frame(chunk, sample_year)
        if number_of_times > 1:
            data.to_csv(os.path.join(subfolder_path, f"{sample_year}_data_part{i}.csv"), index=False)
        else:
            data.to_csv(os.path.join(subfolder_path, f"{sample_year}_data.csv"), index=False)

        i += 1
    
    return True

















































# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# ---------------------------------------- MULTIPLE YEAR ------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------


def age_people_one_year(dictionary_data, sample_year):
    visited_kid_data = set()
    for PersonNr, dict_data in dictionary_data.items():
        #If I am not already dead, check and see if I am going to die this year
        if dict_data['DodDatum'] == None: #Death date is 'None' which means the person is alive
            death_date = dod_datum(sample_year) #Every year the person can die
            if death_date == None: # The person did not die and we update the age
                dict_data['Alder'] += 1
            else:
                dict_data['DodDatum'] = death_date #If I died, update the death date

        #Make sure your kid data has not already been updated
        if PersonNr not in visited_kid_data:
            #Get kid ages information
            my_kid_info = dict_data['kid_info']
            if my_kid_info:
                #Save old values 
                old_values = [(k, v) for k, v in my_kid_info.items()]

                #Clear the dictionary
                my_kid_info.clear()
                
                #Fill the dictionary with new ages 
                for old_kid_ages,number_of_kids in old_values:
                    my_kid_info[old_kid_ages+1] = number_of_kids

                my_spouse = dict_data['spouse']
                if my_spouse: #Check if I have a spouse
                    #Adding the personnumber of my potential spouse so I won't update the kids from the spouse too
                    spouse_PersonNr = my_spouse['PersonNr']
                    visited_kid_data.add(spouse_PersonNr)


def kid_into_row(parent_dict, sample_year, number_of_kids):
    min_age_to_be_in_a_row = 15
    yearborn = sample_year - min_age_to_be_in_a_row

    PersonNr_kids = []
    if number_of_kids == 1:
        PersonNr_kid = person_nummer_creation(sample_year, start_date=f"{yearborn}0101", stop_year=f"{yearborn}1231")
        PersonNr_kids = PersonNr_kids + [PersonNr_kid]
    elif number_of_kids == 2:
        PersonNr_kids = PersonNr_kids + make_twins(min_age_to_be_in_a_row, sample_year) # Will create 2 social security numbers that twins could have
    else:
        PersonNr_kids = PersonNr_kids + make_triplets(min_age_to_be_in_a_row, sample_year) # Will create 2 social security numbers that triplets could have
    
    kid_dicts = []
    spouse = parent_dict['spouse']
    famid = parent_dict['FamId']
    parent1_birthdate = parent_dict['PersonNr']
    parent1_country = parent_dict['FodelseLandnamn']
    parent2_birthdate = ""
    parent2_country = ""
    if spouse:
        parent2_birthdate = spouse['PersonNr']
        parent2_country = spouse['FodelseLandnamn']
        
    #Generates all the data a person should have when they appear as a datapoint
    for PersonNr_kid in PersonNr_kids:
        kid_dict = make_kid_family_frame(PersonNr_kid, famid, is_Kid=True, sample_year=sample_year)
        #Newly turned 15 year olds will always live in the same place as the parent as a start
        kid_dict['Lan']             = parent_dict['Lan']
        kid_dict['Kommun']          = parent_dict['Kommun']
        kid_dict['FastBet']         = parent_dict['FastBet']
        kid_dict['FastLopNr']       = parent_dict['FastLopNr']
        kid_dict['Forsamling']      = parent_dict['Forsamling']
        kid_dict['Distriktskod']    = parent_dict['Distriktskod']

        Lan = kid_dict['Lan']
        
        Utbildning = generate_education(sample_year, PersonNr_kid, parent_dict['Kommun'], is_kid=True) #Kid will have its education in the same kommun as parents live

        #Using parent info, if they have any
        Demographic = generate_demographic(PersonNr_kid, sample_year, 
                                           birthdaymom=parent1_birthdate, birthdaydad=parent2_birthdate,
                                           mom_country=parent1_country, dad_country=parent2_country)
        #Will have no income other than CSN (about 1000kr a month) which is not considered KU1, KU2, KU3
        Economic = generate_economic(sample_year, is_kid=True)

        no_income = 1
        #Will have no workplace
        Work = generate_work(PersonNr_kid, Lan, no_income, sample_year, Economic['YrkStalln'], is_kid=True)
        
        t = merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(kid_dict, Utbildning), Demographic), Economic), Work)

        kid_dicts.append(t)    
    return kid_dicts

        
def turn_kid_into_row(dictionary_data, sample_year):
    visited_kid_data = set()
    young_adults = []
    for PersonNr, dict_data in dictionary_data.items():
        #Making sure I don't make kids into data for people sharing same kid_info
        if PersonNr not in visited_kid_data:
            my_kid_info = dict_data['kid_info']
            
            for kid_age, number_of_kids in my_kid_info.items():
                if kid_age == 15: #The kid will turn 16 and thus is added as their own row in the dataframe
                    kid_dicts = kid_into_row(dict_data, sample_year, number_of_kids)
                    young_adults = young_adults + kid_dicts
                    
                    kids_at_home_data = dict_data['my_kids_living_at_home']
                    #The newly made kids are added as items in the parent 'my_kids_living_at_home'
                    for kid in kid_dicts:
                        kid_PersonNr = kid['PersonNr']
                        kids_at_home_data[kid_PersonNr] = kid

            my_spouse = dict_data['spouse']
            if my_spouse: #Check if I have a spouse
                #Adding the personnumber of my potential spouse so I won't update the kids from the spouse too
                spouse_PersonNr = my_spouse['PersonNr']
                visited_kid_data.add(spouse_PersonNr)
    
    #All kids that turned 15 this year now have their data stored in the big dictionary with the rest of all other people
    for kid in young_adults:
        kid_PersonNr = kid['PersonNr']
        dictionary_data[kid_PersonNr] = kid


def get_babies(dictionary_data): #Gives each person to have some kids
    for k, dict_data in dictionary_data.items():
        my_kid_info = dict_data['kid_info'] #Dict with kid ages
                                    #Kids living at home can not have children
        if 0 not in my_kid_info and k == dict_data['FamId']:
            #No more than 5 kids living at home at a time
            if sum(my_kid_info.values()) < 5:
                if random.random() > 0.65 and random.randint(0, sum(my_kid_info.values())) < 3:
                    kid_probability = random.random()
                    if      kid_probability < 1/62500: kids = 3 #Probability to have triplets
                    elif    kid_probability < 1/250: kids = 2   #Probability to have twins
                    else:   kids = 1
                    my_kid_info[0] = kids       


def kids_move_out(dictionary_data, sample_year):
    #Only kids in 'my_kids_living_at_home' can move 
    for _, dict_data in dictionary_data.items():
        things_to_update = []
        my_kid_info = dict_data['kid_info']
        my_kids_living_at_home = dict_data['my_kids_living_at_home']
        if my_kids_living_at_home: #Checks if you have kids living at home or not
            for kid_PersonNr, kid_dict in my_kids_living_at_home.items():
                kid_age = kid_dict['Alder']
                is_dead = kid_dict['DodDatum']
                if is_dead == None:
                    if random.random() > 10/kid_age: #The older you get, the more likely you are to move out
                        kid_dict['FamId'] = kid_dict['PersonNr'] #New FamId
                        new_location = generate_geographical()  #New place to live
                        Utbildning = generate_education(sample_year, kid_dict['PersonNr'], new_location['Kommun']) #Kid will have its education in the same kommun as parents live
                        Economic = generate_economic(sample_year) #If you move out, you need some kind of income
                        income = [Economic['KU1lnk'], Economic['KU2lnk'], Economic['KU3lnk']]
                        Lan = new_location['Lan']
                        Work = generate_work(kid_dict['PersonNr'], Lan, income, sample_year, Economic['YrkStalln']) #Where, if the person works, does the person work
                        kid_dict = merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(kid_dict, Utbildning), new_location), Work), Economic)
                        things_to_update.append((kid_PersonNr, kid_age))
                        
        #Removing kids from parent info
        for (kid_PersonNr, kid_age) in things_to_update: 
            my_kids_living_at_home.pop(kid_PersonNr)
            my_kid_info[kid_age] -=1
            if my_kid_info[kid_age] < 1: #If there are no more kids of that age, remove the key
                my_kid_info.pop(kid_age)


def simulate_1_year(list_of_dictionaries, sample_year):
    age_people_one_year(list_of_dictionaries, sample_year)
    turn_kid_into_row(list_of_dictionaries, sample_year)
    get_babies(list_of_dictionaries)
    kids_move_out(list_of_dictionaries, sample_year)
    

def simulate_x_years(number_of_households, start_year, number_of_years_to_simulate, chunk_csv = True):
    """
    Parameters
    ----------
    number_of_households : integer
        The number_of_households of households you want to generate in the first year
    
    start_year : integer
        The year you want to pretend it is when the first data is generated.
    
    number_of_years_to_simuate : integer
        The number of years you want to simulate excluding the first year
        
    chunk_csv : Boolean
        Will split each csv file per year into chunks of up to 20_000 rows 
        to allow you to push the data to GitHub without reaching
        file size limit

    Returns : None
    -------
    The function does not return anything itself and instead
    calls upon dict_to_csvs which will in turn create a number
    of directories containing csv file(s) with data about
    some fake population in Sweden

    Example:
    simulate_x_years(1000, 1990, 30, chunk_csv = True)
    Will create a folder called "synthetic_scb_data" and
    create 30 subdirectories, each containing a number 
    of csv file(s) with some data for some fake 
    population in Sweden during each year
    """
    print(f"Creating data for {number_of_households} households in the year {start_year} - {start_year+number_of_years_to_simulate-1}")
    print(f"Creating start data for year {start_year}")
    data = generate_data(number_of_households, start_year)

    #Turning the first year of data into a csv
    dict_to_csvs(data, start_year, chunk_csv)

    if number_of_years_to_simulate > 0:
        starting_year_simulation = start_year+1
        stopping_year_simulation = start_year+number_of_years_to_simulate

        for year in range(starting_year_simulation, stopping_year_simulation): #Start year 1990, simulate year 1991 to 1991+years_to_simulate
            print("--------------------------")
            print(f"Simulating data for year {year}")
            simulate_1_year(data, year)          
            print("Turning data into csv(s)")
            dict_to_csvs(data, year, chunk_csv)
            print(f"Finished year {year}")    
    
        print("--------------------------")
        print("")
        print("Program finished")
    return None

households = 300
start_year = 1990
years_to_simulate = 30
chunk_csv = True

#How many households, starting year, number of csvs (years) ((including start year))
simulate_x_years(households, start_year, years_to_simulate, chunk_csv=True) 