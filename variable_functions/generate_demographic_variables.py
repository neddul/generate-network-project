# ## Variable Generation
# #### 1. FodelseAr
# This is the birth year it is extracted from the personnummer


#extract first 4 values of personnummer to get the age
def fodelse_ar(personnummer):
    return personnummer[:4]


# #### 2. DodDatum
# Date of death (year,month,day)
import random
from datetime import datetime, timedelta

today = datetime.now()

#generate date of death by adding random number of days to the birthday
def dod_datum(personnummer, end_year=2019):
    if random.randint(1,100) <= 5:
        year, month, day = int(personnummer[:4]), int(personnummer[4:6]), int(personnummer[6:8])
        birthday = datetime(year, month, day)
        min_days = 1 #minimum number of days to be added to birthday
        max_days = (datetime(end_year, 12, 31) - birthday).days #maximum number of days to be added to birthday (using end of previous year)
        random_days = random.randint(min_days, max_days)
        deathday = birthday + timedelta(days=random_days)
        return str(deathday.strftime('%Y%m%d'))
    else:
        return None

# #### 3. Alder
# This is the age and can be calculated from birth year in personnummer.
import dateutil.relativedelta

#calcuate age using birthday from personnummer
def alder(personnummer, death_date):
    if death_date == None:        
        today = datetime(2019, 12, 1)
    else:
        year, month, day = int(death_date[:4]), int(death_date[4:6]), int(death_date[6:8])
        today = datetime(year, month, day)

    year, month, day = int(personnummer[:4]), int(personnummer[4:6]), int(personnummer[6:8])
    birthday = datetime(year, month, day)
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
def inv_utv_land():
    countries = ['Sweden', 'India', 'Poland', 'Germany', 'Syria', 'Pakistan', 'Iran', 'Afghanistan', 'Turkey', 'Romania', 'China', 'Iraq', 'Finland', 'USA', 'Russia', 'Netherlands', 'Brazil', 'Denmark', 'UK', 'Italy']
    random_country = random.choice(countries)
    return random_country  

# #### 6. InvUtvManad: 
# Year and month for immigration to Sweden and year and month for emigration from Sweden.
def inv_ut_manad(personnummer, end_year):
    year, month = int(personnummer[:4]), int(personnummer[4:6])
    date = datetime(year, month, 1)
    min_days = 1 #minimum number of days to be added to birthday
    if end_year == None: 
        max_days = (datetime(2019, 12, 31) - date).days #maximum number of days to be added to birthday (using end of previous year)
    else:
        max_days = (datetime(int(end_year[:4]), 12, 31) - date).days #maximum number of days to be added to birthday (using end of previous year)
        
    random_days = random.randint(min_days, max_days)
    inv_ut_manad = date + timedelta(days=random_days)
    return inv_ut_manad.strftime('%Y-%m')

# #### 7. PostTyp
def post_typ(): #either immigration or emmigration
    values = ['Inv', 'Utv']
    return random.choice(values)


# #### 8. FodelseLandnamn
# SCB 2022 list - Sweden, India, Poland, Germany, Syria, Pakistan, Iran, Afghanistan, Turkey, Romania, China, Iraq, Finland, USA, Russia, Netherlands, Brazil, Denmark, UK, Italy, Other 
def fodelse_landnamn():
    countries = ['Sweden', 'India', 'Poland', 'Germany', 'Syria', 'Pakistan', 'Iran', 'Afghanistan', 'Turkey', 'Romania', 'China', 'Iraq', 'Finland', 'USA', 'Russia', 'Netherlands', 'Brazil', 'Denmark', 'UK', 'Italy']
    random_country = random.choice(countries)
    return random_country

# #### 9. FodelseTidMor
def fodelse_tid(personnummer):
    year, month, day = int(personnummer[:4]), int(personnummer[4:6]), int(personnummer[6:8])
    birthday = datetime(year, month, day)
    return birthday.date()


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

import pandas as pd

def generate_demographic(PersonNr):
    FodelseAr = fodelse_ar(PersonNr)
    DodDatum = dod_datum(PersonNr)
    if not type(DodDatum) == None:
        Alder = alder(PersonNr, DodDatum)
        InvUtvManad = inv_ut_manad(PersonNr, DodDatum)
    else:
        Alder = alder(PersonNr)
        InvUtvManad = inv_ut_manad(PersonNr)
    
    me   = fodelse_landnamn()
    mom  = fodelse_landnamn()
    dad  = fodelse_landnamn()

    demographic_data = {
        'FodelseAr'             : [FodelseAr],
        'DodDatum'              : [DodDatum],
        'Alder'                 : [Alder],          #2019 is the last year
        'Kon'                   : [kon(PersonNr)],
        'InvUtvLand'            : [inv_utv_land()],
        'InvUtvManad'           : [InvUtvManad],
        'PostTyp'               : [post_typ()],
        'FodelseLandnamn'       : [me],
        'FodelseTidMor'         : [fodelse_tid('198201028936')], #Arbitrary needs to be fixed
        'FodelseLandnamnMor'    : [mom],
        'FodelseTidFar'         : [fodelse_tid('197901028936')], #Arbitrary needs to be fixed
        'FodelseLandnamnFar'    : [dad],
        'UtlSvBakg'             : [utl_sv_bakg(me,dad,mom)] 
                       }
    return pd.DataFrame.from_dict(demographic_data)
