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



def generate_economic(amount,sample_year):
    SyssStat = generate_employment_statuses(amount,sample_year)
    ArbTid = generate_workingtime(SyssStat)
    YrkStalln = generate_job(ArbTid)
    KU1lnk, KU2lnk, KU3lnk = generate_income(ArbTid)
    Raks_SummaInk = generate_total_incomes(KU1lnk,KU2lnk, KU3lnk)
    Raks_EtablGrad = generate_labor_connection(YrkStalln)
    Raks_Forvink = generate_Forvink(Raks_SummaInk)
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
    data = pd.DataFrame.from_dict(employment_data)
    return data

#generate_demographic_economic(20,2019)