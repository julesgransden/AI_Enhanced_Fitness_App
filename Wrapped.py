
#Returns the daily average amount of sleep the individual is getting
def getAvgSleep(df):
    Totaldays = df.shape[0]
    sleep =df['TotalTimeAsleep'].sum()
    DailyAvgHours = sleep/Totaldays
    return DailyAvgHours

#Returns the total amount of sleep of an individual in the time interval where data was recorded
def getTotalSleep(df):
    sleep =df['TotalTimeAsleep'].sum()
    return sleep

#Returns the daily average amount of calories burned daily by the individual in question 
def getAvgCaloriesBurned(df):
    Totaldays = df.shape[0]
    TotCal =df['Calories'].sum()
    AvgCal = int(TotCal/Totaldays)
    return AvgCal

#Returns the total amount of calories burned in the time interval where data was recorded
def getTotalCaloriesBurned(df):
    TotCal =df['Calories'].sum()
    return TotCal

#Returns the total amount of steps in the time interval where data was recorded
def getTotalDistance(df):
    TotD =int(df['TotalDistance'].sum())
    return TotD

#Returns the daily average steps daily by the individual in question 
def getAvgDistance(df):
    Totaldays = df.shape[0]
    TotD =int(df['TotalDistance'].sum())
    AvgD = int(TotD/Totaldays)
    return AvgD

#Returns the total amount of steps in the time interval where data was recorded
def getTotalSteps(df):
    TotS =int(df['TotalSteps'].sum())
    return TotS

#Returns the daily average steps daily by the individual in question 
def getAvgSteps(df):
    Totaldays = df.shape[0]
    TotS =int(df['TotalSteps'].sum())
    AvgS = int(TotS/Totaldays)
    return AvgS

#Returns the total minutes spent active in the time interval where data was recorded
def getTotalActivity(df):
    TotAct =(df['VeryActiveMinutes'] + df['FairlyActiveMinutes']).sum()
    return TotAct

#Returns the daily average number of minutes spent active by the individual in question 
def getAvgActivity(df):
    Totaldays = df.shape[0]
    TotAct =(df['VeryActiveMinutes'] + df['FairlyActiveMinutes']).sum()
    AvgAct = int(TotAct/Totaldays)
    return AvgAct