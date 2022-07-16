import pandas as pd
import numpy as np
import datetime
from datetime import date

#Setup the driver form 
def setupDf(df):
        df['Priority'] = 0
        df['Latest Date'] = 0
        for driver_index, driver in df.iterrows():
            df.at[driver_index, 'Latest Date'] = datetime.date(
                2002, 8, 22)
            if (driver['CL'] == 'Y'):
                df.at[driver_index, 'Priority'] = 1
            elif (driver['CL'] == 'N'):
                df.at[driver_index, 'Priority'] = 2
        df = df.sort_values(by='Latest Date')


#Return a simplified version of the driver form
def simplifyDf(df): 
        return df.copy()[['Name', 'Preferred Pickup', 'CL', 'NumSeats']]

#Combiine the weekly rides form and permanent rides form, remove any duplicates
def combineRiders(wrf, prf):
    rf = pd.concat([wrf, prf], ignore_index=True)
    rf['Timestamp'] = pd.to_datetime(rf['Timestamp'])
    rf['PhoneNum'] = rf['PhoneNum'].astype(int)
    rf.sort_values(by='Timestamp', axis=0, inplace=True)
    rf.drop_duplicates(inplace=True, subset='PhoneNum')
    rf = rf.sort_values(by='Pickup')
    return rf


#Colleges are assigned by relative location and driving convenience
sections = {
    'Upper UCSD' : ['Seventh', 'ERC', 'Marshall', 'Sixth'],
    'Lower UCSD' : ['Muir', 'Revelle'],
    'East UCSD' : ['Warren', 'Peepo Canyon'],
    'Regents' : ['Regents']
}

#Assigns drivers to riders
def assign(df, df_copy, rf):
    # Some Variables for Counting
    numRiders = len(df.index)
    needRide = 'false'

    #Creates Driver column for each rider (default 0)
    rf['Driver'] = 0

    #Assigns CL drivers with a preference first
    for rider_index, rider in rf.iterrows():
        for driver_index, driver in df_copy.iterrows():
            if (df.at[driver_index, 'Priority'] == 1) and (driver['NumSeats'] > 0) and not (driver['Preferred Pickup'] is np.NaN) and (rider['Pickup'] in sections[driver['Preferred Pickup']]):
                rf.at[rider_index, 'Driver'] = driver['Name']
                df_copy.at[driver_index, 'NumSeats'] -= 1
                df.at[driver_index, 'Latest Date'] = date.today()
                numRiders-=1
                break

    #Assign CL drivers without a preference
    for rider_index, rider in rf.iterrows():
        for driver_index, driver in df_copy.iterrows():
            noDriver = rf.at[rider_index, 'Driver'] == 0
            priorityOne = df.at[driver_index, 'Priority'] 
            hasSeats = driver['NumSeats'] > 0
            if noDriver and priorityOne and hasSeats :
                rf.at[rider_index, 'Driver'] = driver['Name']
                df_copy.at[driver_index, 'NumSeats'] -= 1
                df.at[driver_index, 'Latest Date'] = date.today()
                numRiders-=1 
                break
                
    #Check if all riders have a driver 
    for rider_index, rider in rf.iterrows():
        if(rf.at[rider_index, 'Driver'] == 0):
            needRide = 'true'
            
    #Assign Non-CL drivers with a preference
    if(needRide == 'true'):
        for rider_index, rider in rf.iterrows():
            for driver_index, driver in df_copy.iterrows():
                if (df.at[driver_index, 'Priority'] == 2) and (driver['NumSeats'] > 0) and not (driver['Preferred Pickup'] is np.NaN) and (rider['Pickup'] in sections[driver['Preferred Pickup']]):
                    rf.at[rider_index, 'Driver'] = driver['Name']
                    df_copy.at[driver_index, 'NumSeats'] -= 1
                    df.at[driver_index, 'Latest Date'] = date.today()
                    numRiders-=1
                    break

    #Assign CL drivers without a preference
    if(needRide == 'true'): 
        for rider_index, rider in rf.iterrows():
            for driver_index, driver in df_copy.iterrows():
                if (df.at[driver_index, 'Priority'] == 2) and (rf.at[rider_index, 'Driver'] == 0) and (driver['NumSeats'] > 0):
                    rf.at[rider_index, 'Driver'] = driver['Name']
                    df_copy.at[driver_index, 'NumSeats'] -= 1
                    df.at[driver_index, 'Latest Date'] = date.today()
                    numRiders-=1
                    break

# export the select columns of the riders dataframe to a CSV file
def getAssignments(rf):
    rf.to_csv("assignments.csv", index=False, columns=['Name', 'Pickup', 'Driver'])
    
# export the riders data fram to a CSV file
def getDrivers(df):
    df.to_csv("drivers.csv", index=False)