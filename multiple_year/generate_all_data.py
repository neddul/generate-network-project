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
            return str(deathday.strftime('%Y%m%d'))
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
    years = age.years
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

def generate_demographic(PersonNr, sample_year, birthdaymom='19820102-8936', birthdaydad='19790102-8936'):
    FodelseAr = fodelse_ar(PersonNr)
    DodDatum = dod_datum() # People can only have died during the sample year and not earlier
    InvUtvLand, Status = get_status()
    if DodDatum == None:
        Alder = alder(PersonNr, sample_year)
        InvUtvManad = inv_ut_manad(Status,PersonNr, sample_year)
    else:
        Alder = alder(PersonNr, sample_year, DodDatum)
        InvUtvManad = inv_ut_manad(Status,PersonNr, sample_year, DodDatum)
    
    me   = fodelse_landnamn()
    mom  = fodelse_landnamn()
    dad  = fodelse_landnamn()

    demographic_data = {
        'FodelseAr'             : FodelseAr,
        'DodDatum'              : DodDatum,
        'Alder'                 : Alder,          #2019 is the last year
        'Kon'                   : kon(PersonNr),
        'InvUtvLand'            : InvUtvLand,
        'InvUtvManad'           : InvUtvManad,
        'PostTyp'               : Status,
        'FodelseLandnamn'       : me,
        'FodelseTidMor'         : fodelse_tid(birthdaymom), #Arbitrary needs to be fixed
        'FodelseLandnamnMor'    : mom,
        'FodelseTidFar'         : fodelse_tid(birthdaydad), #Arbitrary needs to be fixed
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

def generate_employment_statuses(amount,sample_year):
    #1 = Gainfully employed according to the limit, 16-74 years 
    #5 = Not gainfully employed according to the limit, but with control information from employer or business income during the year 
    #6 = Not gainfully employed, without control information from employer or business income during the year 
    #7 = Gainfully employed, 15 years
    SyssStat = []
    for i in range(amount):  
        if sample_year <= 2003:
            status = [1, 5, 6]
            probabilities = [0.6, 0.2, 0.2]
        elif sample_year <= 2011:
            status = [1, 5, 6]
            probabilities = [0.7, 0.2, 0.1]
        else:
            status = [1, 5, 6, 7]
            probabilities = [0.69, 0.2, 0.1, 0.01]
        employ = random.choices(status, probabilities)[0]
        SyssStat.append(employ)

    return SyssStat


def generate_workingtime(SyssStat):
    #1 = 0 hours, 2 = 1 – 15 hours, 3 = 16 – 19 hours, 4 = 20 – 34 hours, 5 = 35 – w hours, 9 = Uppgift
    ArbTid = []
    for s in SyssStat:
        if s == 1 or s == 7 or s == 5:
            status = [1,2,3,4,5,9]
            probabilities = [0.05, 0.1, 0.15, 0.2, 0.4, 0.1]
            time = random.choices(status, probabilities)[0]
            ArbTid.append(time)
        else:
            ArbTid.append(" ")
    return ArbTid 


def generate_job(ArbTid):
    #0 = Persons without control duties 1 = Sailors 
    #2 = Employees (excl. seamen) 4 = Entrepreneurs 5 = Entrepreneurs in own AB
    YrkStalln = []
    for i in ArbTid:
        if i == " ":
            YrkStalln.append(" ")
        else:
            status = [0,1,2,4,5]
            probabilities = [0.1, 0.2, 0.49, 0.2, 0.01]
            job = random.choices(status, probabilities)[0]
            YrkStalln.append(job)
    return YrkStalln


def generate_income(ArbTid):
    mean=1000
    std_dev=500
    KU1lnk = []
    KU2lnk = []
    KU3lnk = []

    for i in ArbTid:
        if i == " ":  
            KU1lnk.append(0)
            KU2lnk.append(0)
            KU3lnk.append(0)
        else:
            # Generate incomes from a normal distribution with the specified mean and standard deviation
            ku1 = max(0, int(np.random.normal(mean, std_dev)))
            ku2 = max(0, int(np.random.normal(mean, std_dev)))
            ku3 = max(0, int(np.random.normal(mean, std_dev)))
            
            # Ensure KU1lnk > KU2lnk > KU3lnk
            KU1lnk.append(max(ku1, ku2, ku3))
            generate_ku2 = random.random() < 0.5
            if generate_ku2:
                KU2lnk.append(sorted([ku1, ku2, ku3])[1])
                generate_ku3 = random.random() < 0.1
                if generate_ku3:
                    KU3lnk.append(min(ku1, ku2, ku3))
                else:
                    KU3lnk.append(0)
            else:
                KU2lnk.append(0)
                KU3lnk.append(0)
            
    return KU1lnk, KU2lnk, KU3lnk


def generate_total_incomes(KU1lnk, KU2lnk, KU3lnk):
    
    median_income = 2753
    sigma = 0.6  # Adjust as needed for desired skewness
    
    mu = np.log(median_income) - 0.5 * sigma**2
    
    incomes = np.random.lognormal(mean=mu, sigma=sigma, size=len(KU1lnk))
    incomes = np.clip(incomes, 0, 1014000)
    incomes = incomes.astype(int) 
    Raks_SummaInk = []
    for i in range(0,len(incomes)):
        if incomes[i] < KU1lnk[i]+KU2lnk[i]+KU3lnk[i]:
            Raks_SummaInk.append(KU1lnk[i]+KU2lnk[i]+KU3lnk[i])
        else:
            Raks_SummaInk.append(incomes[i])
                   
    return Raks_SummaInk


def generate_labor_connection(YrkStalln):
    Raks_EtablGrad = []
    for i in YrkStalln:
        if i != 2:
            Raks_EtablGrad.append('NULL')
        else:
            Raks_EtablGrad.append(random.choice([0, 1]))
            
    return Raks_EtablGrad   


def generate_Forvink(Raks_SummaInk):
    Raks_Forvink = []
    for i in Raks_SummaInk:
        if i > 10000:
            Raks_Forvink.append(i)
        else:
            Raks_Forvink.append(0)
    return Raks_Forvink


def generate_main_labor_connection(YrkStalln):
    Raks_Huvudanknytning = []
    for i in YrkStalln:
        if i == 2:
            status = [1,2,3,4]
            probabilities = [0.5,0.2,0.1,0.2]
            connection = random.choices(status, probabilities)[0]
            Raks_Huvudanknytning.append(connection)          
        elif i == 0:
            Raks_Huvudanknytning.append(7)
        else:
            Raks_Huvudanknytning.append(random.choice([5, 6]))
                
    return Raks_Huvudanknytning 


def generate_economic(sample_year,amount=1):
    SyssStat = generate_employment_statuses(amount,sample_year)
    ArbTid = generate_workingtime(SyssStat)
    YrkStalln = generate_job(ArbTid)
    KU1lnk, KU2lnk, KU3lnk = generate_income(ArbTid)
    Raks_SummaInk = generate_total_incomes(KU1lnk,KU2lnk, KU3lnk)
    Raks_EtablGrad = generate_labor_connection(YrkStalln)
    Raks_Forvink = generate_Forvink(Raks_SummaInk)
    Raks_Huvudanknytning = generate_main_labor_connection(YrkStalln)

    employment_data = {
        'SyssStat'              : SyssStat[0],
        'ArbTid'                : ArbTid[0],
        'YrkStalln'             : YrkStalln[0],
        'KU1lnk'                : KU1lnk[0],
        'KU2lnk'                : KU2lnk[0],
        'KU3lnk'                : KU3lnk[0],
        'Raks_SummaInk'         : Raks_SummaInk[0],
        'Raks_Huvudanknytning'  : Raks_Huvudanknytning[0],
        'Raks_EtablGrad'        : Raks_EtablGrad[0],
        'Raks_Forvink'          : Raks_Forvink[0]
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


import random
import string
import pandas as pd

def random_sampler(start, end, number):
    output = []
    for _ in range(number):
        output.append(random.randint(start, end))
        
    return output

generate_education_utbildning = pd.read_csv("data/utbildning_cleaner.csv")

def generate_education(amount=1): 
    Sun2000niva_old = random_sampler(10000,99999, amount)
    indexes = random_sampler(0,len(generate_education_utbildning)-1, amount)
    SUN2000Grp = []
    SUN2000Inr = []
    SUN2000Niva = []
    alphabet = string.ascii_lowercase
    for i in range(len(indexes)):
        index = indexes[i]
        SUN2000Grp.append(generate_education_utbildning.at[index, 'Utbildningsgrupper 2020'])
        options_inr = generate_education_utbildning.at[index, 'Inriktningskoder SUN 2020']
        if isinstance(options_inr , int):
            random_letters = random.choice(alphabet)
            if options_inr <100: 
                options_inr=options_inr+100
            SUN2000Inr.append(str(options_inr)+ random_letters)
        else: 
            options = [item.strip() for item in options_inr.split(',')]
            SUN2000Inr.append(random.choice(options))
        options_niv = generate_education_utbildning.at[index, 'Nivåkoder SUN 2020']
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

    education = {
            'Sun2000niva_old'   : Sun2000niva_old[0],
            'SUN2000niva'       : SUN2000Niva[0],
            'SUN2000Inr'        : SUN2000Inr[0],
            'SUN2000Grp'        : SUN2000Grp[0],
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
import pandas as pd
import datetime
numbers = [str(x) for x in range(10)]
def get_date(start_date = '19250101', stop_date='20191231'):
    # datetime for start date
    start = datetime.date.fromisoformat(start_date)

    # datetime for stop date
    stop = datetime.date.fromisoformat(stop_date)

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
    date = date.isoformat().replace('-','')
    return date


taken_social_security_numbers = {'0'}
def person_nummer_creation(sample_year, start_date="19250101", stop_year="", gender=3):        
    if stop_year == "":
        end_date = str(sample_year-16) #People need to be atleast 16 to legally live alone in Sweden
        end_date = end_date + "1231"
    else:
        end_date = stop_year
 
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

def update_kid_categories(my_dict, kid_info_dict, sample_year):
    for k,v in kid_info_dict.items():
        k = int(k)
        if v > 3:
            print("Update dict")
            print(v)
            print(my_dict)
        if k >= 0 and k < 4:
            for _ in range(v):
                my_dict['Barn0_3'] +=1
        elif k > 3 and k < 7:
            for _ in range(v):
                my_dict['Barn4_6'] +=1
        elif k > 6 and k < 11:
            for _ in range(v):
                my_dict['Barn7_10'] +=1
        elif k > 10 and k < 16:
            for _ in range(v):
                my_dict['Barn11_15'] +=1
        elif k > 15 and k < 18:
            for _ in range(v):
                my_dict['Barn16_17'] +=1

    if sample_year <= 2004:
        for k,v in kid_info_dict.items():
            k = int(k)
            if v > 3:
                print("Update dict")
                print(v)
                print(kid_info_dict)
            if k > 17: #Barn18plus
                for _ in range(v):
                    my_dict['Barn18plus'] += 1
    else:
        for k,v in kid_info_dict.items():
            k = int(k)

            if k > 17 and k < 20: #Barn18_19
                for _ in range(v):
                    my_dict['Barn18plus'] += 1
            elif k > 19: #Barn20plus
                for _ in range(v):
                    my_dict['Barn20plus'] += 1
    return my_dict



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
        max_age = person_age - 15
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
                print(number_of_kids)
                # print("--------------------------------------")
                # barn = update_kid_categories(barn, barn['kid_info'], sample_year)
                # print(barn)
                barn['kid_info'][k] = 3
                # barn = update_kid_categories(barn, barn['kid_info'], sample_year)
                # print(barn)

        
        update_kid_categories(barn, barn['kid_info'], sample_year)
            
    return barn


def make_kid_family_frame(PersonNr, FamId, is_Kid, sample_year):
    kids = create_children(sample_year, PersonNr, is_kid=is_Kid)
    utbildning = generate_education()
    data = merge_dictionaries(kids, utbildning)
    data['PersonNr'] = PersonNr
    data['FamId'] = FamId
    return data


def create_kids_data(sample_year, FamId, kids_info):
    kids_list = [[],[],[],[]]
    
    for k,v in kids_info['kid_info'].items():
        if int(k) > 15 and int(k) < 18: #Barn16_17
            for _ in range(v):
                kids_list[0].append(v)
    if sample_year <= 2004:
        for k,v in kids_info['kid_info'].items():
            if int(k) > 17: #Barn18plus
                for _ in range(v):
                    kids_list[2].append(v)
    else:
        for k,v in kids_info['kid_info'].items():
            if int(k) > 17 and int(k) < 20: #Barn18_19
                for _ in range(v):
                    kids_list[1].append(v)
            elif int(k) > 19:
                for _ in range(v):
                    kids_list[3].append(v)
    

    kids_list = [sorted([num for num in sublist]) for sublist in kids_list] # Removes all occurances of -1000
    
    kids_in_range = kids_list[:2]    #Barn16_17 and Barn18_19
    kids_plus = kids_list[2:]

    #Barn16-17
    all_kids = []

    # ---------------------- ONLY FOR MAXIMUM OF 3 kids per group

    kids_in_range = kids_list[:2]    #Barn16_17 and Barn18_19
    kids_plus = kids_list[2:]

    #Barn16-17
    all_kids = []

    #Barn16_17 and Barn18_19
    for kids in kids_in_range:
        if len(kids) == 1:
            year_born = sample_year - kids[0]
            kid = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
            all_kids.append(make_kid_family_frame(kid, FamId, is_Kid=True, sample_year=sample_year))
        
        elif len(kids) == 2:
            age1, age2 = kids[0], kids[1]
            if age1 == age2: #Twins
                year_born = sample_year - age1
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
                kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
            else:
                year_born = sample_year - age2
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0630") # First kid born jan - june year 1
                kid2 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0401", stop_year=f"{year_born+1}1231") # Second kid born atleast 10 months later
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
                else: # First kid born alone, other 2 kids are twins
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kids born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=kid2[:8], stop_year=kid2[:8])
            else: # First kid born alone, other 2 kids are twins
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
                    year_born1 = sample_year - age1
                    year_born2 = sample_year - age2
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231")
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231")
                else: # Within 1 years of each other 20 21
                    year_born = sample_year - age2
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born+1}0401", stop_year=f"{year_born+1}1231") # Second kid born atleast 10 months later

        elif len(kids) == 3:
            age1, age2, age3 = kids[0], kids[1], kids[2]
            if age1 == age2 and age2 == age3: #Triplets 20 20 20
                year_born = sample_year - age1
                kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}1231")
                kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                kid3 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])

            elif age1 == age2 and age2 != age3: #The 2 youngest are twins oldest is singlet 
                if age3 - age1 > 1: #More than 1 year apart 20 20 22
                    year_born1 = sample_year - age1
                    year_born2 = sample_year - age3
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231")
                    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231")
                else: #Within 1 year apart 20 20 21
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kids born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=kid2[:8], stop_year=kid2[:8])

            elif age1 != age2 and age2 == age3: #The 2 oldest are twins youngest is singlet 
                if age3 - age1 > 1: #More than 1 year apart 20 22 22
                    year_born1 = sample_year - age1
                    year_born2 = sample_year - age3
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231")
                    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231")
                else: #Within 1 year apart 20 21 21
                    year_born1 = sample_year - age3
                    year_born2 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}0630") # First kids born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=kid1[:8], stop_year=kid1[:8])
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Third kid born atleast 10 months later

            elif age2 - age1 < 2: 
                if age3 - age2 < 2: # 20 21 22
                    year_born = sample_year-age3
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born}0101", stop_year=f"{year_born}0210") # First kid born jan - feb year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born}1201", stop_year=f"{year_born+1}0130") # Second kid born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born+1}1101", stop_year=f"{year_born+1}1231") # Third kid born atleast 10 months later
                else: # 20 21 23
                    year_born3 = sample_year - age3
                    year_born2 = sample_year - age2
                    year_born1 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}0630") # Second kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born1}0401", stop_year=f"{year_born1}1231") # Third kid born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born3}0101", stop_year=f"{year_born3}1231") # First kid born whenever
            else:
                if age3 - age2 < 2: #20 22 23
                    year_born3 = sample_year - age3
                    year_born2 = sample_year - age2
                    year_born1 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born3}0101", stop_year=f"{year_born3}0630") # First kid born jan - june year 1
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0401", stop_year=f"{year_born2}1231") # Second kid born atleast 10 months later
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231") # Third kid born whenever
                else: # 20 22 24
                    year_born3 = sample_year - age3
                    year_born2 = sample_year - age2
                    year_born1 = sample_year - age1
                    kid1 = person_nummer_creation(sample_year, start_date=f"{year_born1}0101", stop_year=f"{year_born1}1231") # Third kid born whenever
                    kid2 = person_nummer_creation(sample_year, start_date=f"{year_born2}0101", stop_year=f"{year_born2}1231") # Third kid born whenever
                    kid3 = person_nummer_creation(sample_year, start_date=f"{year_born3}0101", stop_year=f"{year_born3}1231") # Third kid born whenever
            all_kids.append(make_kid_family_frame(kid1, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid2, FamId, is_Kid=True, sample_year=sample_year))
            all_kids.append(make_kid_family_frame(kid3, FamId, is_Kid=True, sample_year=sample_year))

    return all_kids


def create_spouse(FamId, kids_info):
    spouse_age = int(FamId[:4]) + 7 #The spouse will be as old as the partner or at most 7 years younger
    PersonNr = person_nummer_creation(1,start_date=FamId[:8], stop_year=f"{spouse_age}1231")
    utbildning = generate_education()
    spouse = merge_dictionaries(utbildning, kids_info)
    spouse['PersonNr'] = PersonNr
    spouse['FamId'] = FamId
    return spouse


def generate_family(sample_year):
    PersonNr = person_nummer_creation(sample_year)
    kids_info = create_children(sample_year, PersonNr)
    utbildning = generate_education()
    data = merge_dictionaries(utbildning, kids_info)
    data['PersonNr'] = PersonNr
    data['FamId'] = PersonNr
    family_dicts = [data]

    kids_frames = create_kids_data(sample_year, PersonNr, kids_info) 
    if len(kids_frames) == 0:
        if random.randint(1,100) > 60: # Probability someone is living alone
            spouse = create_spouse(PersonNr, kids_info.copy())
            family_dicts.append(spouse)
    else:
        family_dicts = family_dicts + kids_frames
        min_family_size = 0
        family_size = random.randint(min_family_size, len(kids_frames)+1) #Bigger family, more likley there's a spouse in the household
        if family_size > 1:
            spouse = create_spouse(PersonNr, kids_info.copy())
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
import pandas as pd
import json
scbinternal_fastlopnr = {}
scbinternal_fastlopnr_values = set([])


with open('data/county_dict.json', 'r') as json_file:
    counties_with_municipals = json.load(json_file)


with open('data/tatorter_in_municipals_dict.json', 'r') as json_file:
    tatorter_in_municipals = json.load(json_file)


with open('data/forsamling_dict.json', 'r') as json_file:
    forsamlingar_in_municipals = json.load(json_file)


with open('data/district_codes_from_Forsamling_dict.json', 'r') as json_file:
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
            FastLopNr = random.randrange(1000000000, 9999999999) # Limited to 100k households
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
CfarNumbers_values = set([])
def generate_CfarNr_LISA(PeOrgNr): #Will generate an arbitrary unique 8 digit number
    if PeOrgNr in CfarNumbers:
        return CfarNumbers[PeOrgNr]
    else:
        while True:
            CfarNr_LISA = str(random.randint(100000000, 999999999))
            if CfarNr_LISA not in CfarNumbers_values:
                CfarNumbers_values.add(CfarNr_LISA)
                CfarNumbers[PeOrgNr] = CfarNr_LISA
                return CfarNr_LISA


AstNumbers = set([])
def generate_AstNr_LISA(): #Gives a number to specify what job the person has, like a contractor, teacher, accountant etc
    generate_new_AstNr = random.randint(1,100)
    if generate_new_AstNr > 95: #5% of people have a number in these lines
        special_numbers = ["99980","99981","99982","99983","99984","99985","99986","99987","99988","99989","99990","99991","99992","99993","99994","99996","99998","99999"]
        return special_numbers[random.randint(0,len(special_numbers)-1)]
    else:
        AstNr_LISA = str(random.randint(100001, 999979))[1:]
        AstNumbers.add(AstNr_LISA)
        return AstNr_LISA


PeOrgNumbers = []
def generate_PeOrgNr(personnummer): # 000000-0000 - 999999-9999
    number = random.randint(0,100)
    if number > 87: #The person is a selfstarter and the organisation number is the person's personnumber
        PeOrgNumbers.append(personnummer[2:])
        return personnummer[2:]
    number = random.randint(0, len(PeOrgNumbers)-1 if len(PeOrgNumbers) > 0 else 0)

    if number > 50: # Use an existing job number 
        existing_job_numbers = PeOrgNumbers
        return existing_job_numbers[random.randint(0, len(existing_job_numbers)-1)]
    else: #Generate a new job or accidentaly choose already existing
        PeOrgNr = str(random.randint(10000000000, 99999999999))
        PeOrgNr = PeOrgNr[1:7] + "-" + PeOrgNr[7:]
        PeOrgNumbers.append(PeOrgNr)
        return PeOrgNr


def generate_company(personnummer, kommunnamn, lansnamn, prefix="", yrkstallning="", no_income=False):
    if no_income:
        work_data = {
                        f'{prefix}PeOrgNr'   : "-",
                        f'{prefix}CfarNr'    : "-",
                        f'{prefix}AstNr'     : "-",
                        f'{prefix}AstKommun' : "0000",
                        f'{prefix}AstLan'    : "00",
                        f'{prefix}YrkStalln' : "-",
                        }     
    else:
        PeOrgNr = generate_PeOrgNr(personnummer)
        Cfar_Nr = generate_CfarNr_LISA(PeOrgNr)
        AstNr = generate_AstNr_LISA()
        work_data = {
                        f'{prefix}PeOrgNr'   : PeOrgNr,
                        f'{prefix}CfarNr'    : Cfar_Nr,
                        f'{prefix}AstNr'     : AstNr,
                        f'{prefix}AstKommun' : kommunnamn,
                        f'{prefix}AstLan'    : lansnamn,
                        f'{prefix}YrkStalln' : yrkstallning,
                        }     
    return work_data


def generate_work(personnummer, county, economicstatus):
    Kommun = generate_municipal(county)
    if economicstatus[0] > 0:
        Kommun = generate_municipal(county)
        prefix_working_ties1 = generate_company(personnummer, Kommun, county, prefix="KU1", yrkstallning="1") #Yrkstallning hardcoded needs FIX
    else:
        prefix_working_ties1 = generate_company(personnummer, Kommun, county, prefix="KU1", yrkstallning="1", no_income=True) #Yrkstallning hardcoded needs FIX

    if economicstatus[1] > 0:
        Kommun = generate_municipal(county)
        prefix_working_ties2 = generate_company(personnummer, Kommun, county, prefix="KU2", yrkstallning="1") #Yrkstallning hardcoded needs FIX
    else:
        prefix_working_ties2 = generate_company(personnummer, Kommun, county, prefix="KU2", yrkstallning="1", no_income=True) #Yrkstallning hardcoded needs FIX
    if economicstatus[2] > 0:
        Kommun = generate_municipal(county)
        prefix_working_ties3 = generate_company(personnummer, Kommun, county, prefix="KU3", yrkstallning="1") #Yrkstallning hardcoded needs FIX
    else:
        prefix_working_ties3 = generate_company(personnummer, Kommun, county, prefix="KU3", yrkstallning="1", no_income=True) #Yrkstallning hardcoded needs FIX
    
    biggest_income = economicstatus.index(max(economicstatus))
    

    if biggest_income == 0:
        biggest_data = {
            'CfarNr_LISA' : prefix_working_ties1['KU1CfarNr'],
            'ArbstId' : (prefix_working_ties1['KU1CfarNr'])+(prefix_working_ties1['KU1AstNr'])+(prefix_working_ties1['KU1AstKommun'])+(prefix_working_ties1['KU1PeOrgNr']),
            'AstNr_LISA' : prefix_working_ties1['KU1AstNr'],
            'AstKommun' : prefix_working_ties1['KU1AstKommun'],
            'AstLan' : prefix_working_ties1['KU1AstLan']
        }
    elif biggest_income == 1:
        biggest_data = {
            'CfarNr_LISA' : prefix_working_ties2['KU2CfarNr'],
            'ArbstId' : (prefix_working_ties2['KU2CfarNr'])+(prefix_working_ties2['KU2AstNr'])+(prefix_working_ties2['KU2AstKommun'])+(prefix_working_ties2['KU2PeOrgNr']),
            'AstNr_LISA' : prefix_working_ties2['KU2AstNr'],
            'AstKommun' : prefix_working_ties2['KU2AstKommun'],
            'AstLan' : prefix_working_ties2['KU2AstLan']
        }
    else:
        biggest_data = {
            'CfarNr_LISA' : prefix_working_ties3['KU3CfarNr'],
            'ArbstId' : (prefix_working_ties3['KU3CfarNr'])+(prefix_working_ties3['KU3AstNr'])+(prefix_working_ties3['KU3AstKommun'])+(prefix_working_ties3['KU3PeOrgNr']),
            'AstNr_LISA' : prefix_working_ties3['KU3AstNr'],
            'AstKommun' : prefix_working_ties3['KU3AstKommun'],
            'AstLan' : prefix_working_ties3['KU3AstLan']
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
def generate_person(sample_year=2019):
    family_members = generate_family(sample_year)
    Geographical = generate_geographical()
    Lan = Geographical['Lan']
    data = []
    for member in family_members:
        
        PersonNr = member['PersonNr']

        Demographic = generate_demographic(PersonNr, sample_year)
        Economic = generate_economic(sample_year)

        income = [Economic['KU1lnk'], Economic['KU2lnk'], Economic['KU3lnk']]
        Work = generate_work(PersonNr, Lan, income)

        t = merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(member,Geographical), Demographic), Economic), Work)
        data.append(t)    

    return data


from itertools import chain
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
    data: list of dictionaries
        list of dictionaries with data for all variables.

    """
    people = []
    print(f"{0}/{amount}")
    for i in range(amount):
        if (i+1) % 10000 == 0:
            print(f"{i+1}/{amount}")
        household = generate_person(sample_year)
        people.append(household)

    data = list(chain(*people)) #Flattens list     
    return data


import pandas as pd
def generate_data_frame(data):
    kid_info_dicts = []
    for d in data:
        kid_info_dicts.append(d.pop('kid_info'))

    dataframe = pd.DataFrame(data, columns=[  
                                    'PersonNr', 'Lan', 'Kommun', 'Forsamling', 'Distriktskod', 'FastLopNr', 'FastBet',
                                    'Barn0_3', 'Barn4_6', 'Barn7_10', 'Barn11_15', 'Barn16_17',
                                    'Barn18plus', 'Barn18_19', 'Barn20plus', 'FamId', 
                                    'Sun2000niva_old','SUN2000niva', 'SUN2000Inr', 'SUN2000Grp',
                                    'CfarNr_LISA', 'ArbstId', 'AstNr_LISA', 'AstKommun', 'AstLan',
                                    'KU1PeOrgNr', 'KU1CfarNr', 'KU1AstNr', 'KU1AstKommun', 'KU1AstLan',
                                    'KU1YrkStalln', 'KU2PeOrgNr', 'KU2CfarNr', 'KU2AstNr', 'KU2AstKommun',
                                    'KU2AstLan', 'KU2YrkStalln', 'KU3PeOrgNr', 'KU3CfarNr', 'KU3AstNr',
                                    'KU3AstKommun', 'KU3AstLan', 'KU3YrkStalln',
                                    'FodelseAr', 'DodDatum', 'Alder', 'Kon', 'InvUtvLand', 'InvUtvManad',
                                    'PostTyp', 'FodelseLandnamn', 'FodelseTidMor', 'FodelseLandnamnMor',
                                    'FodelseTidFar', 'FodelseLandnamnFar', 'UtlSvBakg',
                                    'SyssStat', 'ArbTid', 'YrkStalln', 'KU1lnk', 'KU2lnk', 'KU3lnk',
                                    'Raks_SummaInk', 'Raks_Huvudanknytning', 'Raks_EtablGrad', 'Raks_Forvink'
                                 ])
    # Revert changes for specified keys
    for d,kid_info in zip(data, kid_info_dicts):
        d['kid_info'] = kid_info
    return dataframe

import os
def chunk_list(input_list, chunk_size=20000): 
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def dict_to_csvs(dict_data, sample_year=1990):
    sliced_dict_list = chunk_list(dict_data)
    folder_name = f"synthetic_scb_data_{sample_year}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    number_of_times = len(sliced_dict_list)
    print(f"{0}/{number_of_times}")
    i = 1
    for chunk in sliced_dict_list:
        if (i+1) % 15 == 0:
            print(f"{i+1}/{number_of_times}")
        data = generate_data_frame(chunk)
        data.to_csv(os.path.join(folder_name, f"{sample_year}_data_part{i}.csv"), index=False)
        i +=1
    
    return True



if __name__ == "__main__":
    sample_year = 1991
    number_of_households = 15000
    print(f"Creating data for {number_of_households} households for year {sample_year}")
    a = generate_data(number_of_households, sample_year)
    print("Turning data into csv(s)")
    dict_to_csvs(a, sample_year)
    print("Program finished")