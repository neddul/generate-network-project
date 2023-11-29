import random
import pandas as pd
import variable_functions.generate_geographical_variables as ggv

numbers = [str(x) for x in range(10)]
CfarNumbers = set([])
def generate_CfarNr_LISA(): #Will generate an arbitrary unique 8 digit number
    while True:
        CfarNr_LISA = ""
        for _ in range(8):
            CfarNr_LISA = CfarNr_LISA + numbers[random.randint(0, 9)]
        if CfarNr_LISA not in CfarNumbers:
            CfarNumbers.add(CfarNr_LISA)
            return CfarNr_LISA

# for _ in range(10000):
#     a = generate_CfarNr_LISA()
# print(CfarNumbers)

AstNumbers = set([])
def generate_AstNr_LISA(): #Gives a number to specify what job the person has, like a contractor, teacher, accountant etc
    not_allowed_number = ["00000"]
    generate_new_AstNr = random.randint(1,100)
    if generate_new_AstNr > 95: #5% of people have a number in these lines
        special_numbers = ["99980","99981","99982","99983","99984","99985","99986","99987","99988","99989","99990","99991","99992","99993","99994","99996","99998","99999"]
        return special_numbers[random.randint(0,len(special_numbers)-1)]
    else:
        if generate_new_AstNr > 50 and len(AstNumbers)>0:
            jobs = list(AstNumbers)
            return jobs[random.randint(0, len(jobs)-1)]
        else: 
            while True:
                AstNr_LISA = ""
                for _ in range(5):
                    AstNr_LISA = AstNr_LISA + numbers[random.randint(0, 9)]
                if AstNr_LISA not in AstNumbers and AstNr_LISA not in not_allowed_number:
                    AstNumbers.add(AstNr_LISA)
                    return AstNr_LISA

# for _ in range(10000):
#     a = generate_AstNr_LISA()
# print(AstNumbers)    

PeOrgNumbers = set([])

def generate_PeOrgNr(personnummer):
    number = random.randint(0,10000)
    existing_job_numbers = list(PeOrgNumbers)
    if number > 87: #The person is a selfstarter and the organisation number is the person's personnumber
        PeOrgNumbers.add(personnummer[2:])
        return personnummer[2:]

    elif number > 60 and len(existing_job_numbers) > 0: # Use an existing job number 
        return existing_job_numbers[random.randint(0, len(existing_job_numbers)-1)]
    else: #Generate a new job
        while True:
            PeOrgNr = ""
            for _ in range(6):
                PeOrgNr = PeOrgNr + numbers[random.randint(0, 9)]
            PeOrgNr = PeOrgNr +"-"
            for _ in range(4):
                PeOrgNr = PeOrgNr + numbers[random.randint(0, 9)]
            if PeOrgNr not in PeOrgNumbers:
                PeOrgNumbers.add(PeOrgNr)
                return PeOrgNr

# for _ in range(10000):
#     a = generate_PeOrgNr()
# print()    

def generate_company(personnummer, kommunnamn, lansnamn, prefix="", yrkstallning="", no_income=False):
    if no_income:
        work_data = {
                        f'{prefix}PeOrgNr'   : [None],
                        f'{prefix}CfarNr'    : [None],
                        f'{prefix}AstNr'     : [None],
                        f'{prefix}AstKommun' : [None],
                        f'{prefix}AstLan'    : [None],
                        f'{prefix}YrkStalln' : [None],
                        }     
        work_data = pd.DataFrame.from_dict(work_data)

    else:
        PeOrgNr = generate_PeOrgNr(personnummer)
        Cfar_Nr = generate_CfarNr_LISA()
        AstNr = generate_AstNr_LISA()
        work_data = {
                        f'{prefix}PeOrgNr'   : [PeOrgNr],
                        f'{prefix}CfarNr'    : [Cfar_Nr],
                        f'{prefix}AstNr'     : [AstNr],
                        f'{prefix}AstKommun' : [kommunnamn],
                        f'{prefix}AstLan'    : [lansnamn],
                        f'{prefix}YrkStalln' : [yrkstallning],
                        }     
        work_data = pd.DataFrame.from_dict(work_data)
    return work_data

def generate_work(personnummer, county, economicstatus, yrkstallning):
    Kommun = ggv.generate_municipal(county)
    if economicstatus[0] > 0:
        Kommun = ggv.generate_municipal(county)
        prefix_working_ties1 = generate_company(personnummer, Kommun, county, prefix="KU1", yrkstallning="1") #Yrkstallning hardcoded needs FIX
    else:
        prefix_working_ties1 = generate_company(personnummer, Kommun, county, prefix="KU1", yrkstallning="1", no_income=True) #Yrkstallning hardcoded needs FIX

    if economicstatus[1] > 0:
        Kommun = ggv.generate_municipal(county)
        prefix_working_ties2 = generate_company(personnummer, Kommun, county, prefix="KU2", yrkstallning="1") #Yrkstallning hardcoded needs FIX
    else:
        prefix_working_ties2 = generate_company(personnummer, Kommun, county, prefix="KU2", yrkstallning="1", no_income=True) #Yrkstallning hardcoded needs FIX
    if economicstatus[2] > 0:
        Kommun = ggv.generate_municipal(county)
        prefix_working_ties3 = generate_company(personnummer, Kommun, county, prefix="KU3", yrkstallning="1") #Yrkstallning hardcoded needs FIX
    else:
        prefix_working_ties3 = generate_company(personnummer, Kommun, county, prefix="KU3", yrkstallning="1", no_income=True) #Yrkstallning hardcoded needs FIX
    
    biggest_income = economicstatus.index(max(economicstatus))
    

    if biggest_income == 0:
        biggest_data = {
            'CfarNr_LISA' : [prefix_working_ties1.loc[0, 'KU1CfarNr']],
            'ArbstId' : [str(prefix_working_ties1.loc[0, 'KU1CfarNr'])+str(prefix_working_ties1.loc[0, 'KU1AstNr'])+str(prefix_working_ties1.loc[0, 'KU1AstKommun'])+str(prefix_working_ties1.loc[0, 'KU1PeOrgNr'])],
            'AstNr_LISA' : [prefix_working_ties1.loc[0, 'KU1AstNr']],
            'AstKommun' : [prefix_working_ties1.loc[0, 'KU1AstKommun']],
            'AstLan' : [prefix_working_ties1.loc[0, 'KU1AstLan']]
        }
    elif biggest_income == 1:
        biggest_data = {
            'CfarNr_LISA' : [prefix_working_ties2.loc[0, 'KU2CfarNr']],
            'ArbstId' : [str(prefix_working_ties2.loc[0, 'KU2CfarNr'])+str(prefix_working_ties2.loc[0, 'KU2AstNr'])+str(prefix_working_ties2.loc[0, 'KU2AstKommun'])+str(prefix_working_ties2.loc[0, 'KU2PeOrgNr'])],
            'AstNr_LISA' : [prefix_working_ties2.loc[0, 'KU2AstNr']],
            'AstKommun' : [prefix_working_ties2.loc[0, 'KU2AstKommun']],
            'AstLan' : [prefix_working_ties2.loc[0, 'KU2AstLan']]
        }
    else:
        biggest_data = {
            'CfarNr_LISA' : [prefix_working_ties3.loc[0, 'KU3CfarNr']],
            'ArbstId' : [str(prefix_working_ties3.loc[0, 'KU3CfarNr'])+str(prefix_working_ties3.loc[0, 'KU3AstNr'])+str(prefix_working_ties3.loc[0, 'KU3AstKommun'])+str(prefix_working_ties3.loc[0, 'KU3PeOrgNr'])],
            'AstNr_LISA' : [prefix_working_ties3.loc[0, 'KU3AstNr']],
            'AstKommun' : [prefix_working_ties3.loc[0, 'KU3AstKommun']],
            'AstLan' : [prefix_working_ties3.loc[0, 'KU3AstLan']]
        }

    working_data = pd.concat([pd.DataFrame.from_dict(biggest_data), prefix_working_ties1, prefix_working_ties2, prefix_working_ties3], axis=1)
    return working_data

