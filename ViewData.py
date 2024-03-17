import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas_datareader.data as data
from sklearn.linear_model import LinearRegression
from pathlib import Path
import os

def OrganiseData(indiv, unorganizedCSVDataLocation, DailyDataCSVLocation, SleepDataCSVLocation):

    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(unorganizedCSVDataLocation)  # Replace 'your_dataset.csv' with the path to your dataset file

    # Assuming the column containing the ID numbers is named 'Id',split the dataset based on this column
    groups = df.groupby('Id')
    listofID = []
    # Iterate over each group and add it to the list which will store these group Ids
    for group_id, group_data in groups:
        listofID.append(group_id)

    #Enumerate this list into a dictionary so we can associate a number from 1-32 for each ID
    IndivToID = dict(enumerate(listofID))

    #Select Individual who's information we want to show (0-32)
    ID = IndivToID[int(indiv)-1] 


    #get the dailyactivity data sheet
    Activity_file_path = DailyDataCSVLocation +"/"+ str(ID) + ".csv"

    try:
        #get the dailySleep data sheet
        sleepData = True
        Sleep_file_path = SleepDataCSVLocation +"/"+ str(ID) + "_s.csv"
    except:
        sleepData = False
        print("No sleep Data for this individual!")


    Active = pd.read_csv(Activity_file_path)
    if sleepData: sleep = pd.read_csv(Sleep_file_path)


    #Lets build our current dataframe to hold this individuals useful data
    current = Active.drop(Active.columns[4:10], axis=1)
    current = current.drop(Active.columns[0], axis=1)

    sleep = sleep.drop(sleep.columns[2], axis =1)
    sleep = sleep.drop(sleep.columns[0], axis =1)

    # Convert the 'SleepDay' column to datetime format
    sleep['SleepDay'] = pd.to_datetime(sleep['SleepDay'])
    # Convert the 'SleepDay' column to '%m/%d' format
    sleep['SleepDay'] = sleep['SleepDay'].dt.strftime('%d/%m')

    #Now lets merge the two files and if there is no sleep info on a day fill in with '0'

    # Merge sleep information into activity DataFrame based on date
    merged_df = pd.merge(current, sleep, left_on='ActivityDate', right_on='SleepDay', how='left')

    # Drop the extra 'SleepDay' column
    merged_df.drop('SleepDay', axis=1, inplace=True)

    # Fill 0 values in sleep-related columns with empty strings
    sleep_columns = ['TotalMinutesAsleep', 'TotalTimeInBed']
    merged_df[sleep_columns] = merged_df[sleep_columns].fillna(0)

    curr = merged_df

    # Rename a the Date column
    curr.rename(columns={'ActivityDate': 'Date'}, inplace=True)

    # Convert sleep minutes into sleep hours
    curr['TotalMinutesAsleep'] = curr['TotalMinutesAsleep'] / 60
    curr['TotalTimeInBed'] = curr['TotalTimeInBed'] / 60

    #Rename these columns
    curr.rename(columns={'TotalMinutesAsleep': 'TotalTimeAsleep'}, inplace=True)
    
    return curr


