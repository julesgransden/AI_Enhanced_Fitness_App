import mysql.connector as sql
import pandas as pd
from ViewData import OrganiseData

db = sql.connect(
    host="localhost",
    user="root",
    password="Beliveau1!",
    database="giraffe"
)


def uploadUserDatatoDB(userID,username,password,name,age,gender,height,weight):
    
    cursor = db.cursor()
    sql = f" INSERT INTO persoInfo VALUES('{userID}','{username}','{password}','{name}',{age},'{gender}',{height},{weight});"
    cursor.execute(sql)
    db.commit()

def uploadInjurytoDB(userID,date, Description):
    
    cursor = db.cursor()
    sql = f" INSERT INTO injury_history (user_id, injury_date, injury_description) VALUES('{userID}','{date}','{Description}');"
    cursor.execute(sql)
    db.commit()
    
def addInjuryRecovery(injuryID, recovery):
    cursor = db.cursor()
    sql = f" UPDATE injury_history SET recovery = '{recovery}' WHERE injury_id = '{injuryID}'"
    cursor.execute(sql)
    db.commit()

def uploadHealthData(userID):
    
    Unorganised = "/Users/julesgransden/Desktop/Perso Projects/HealthFitnessApp/Code/FitDB/dailyActivity_merged.csv"
    DailyActivity = "/Users/julesgransden/Desktop/Perso Projects/HealthFitnessApp/Code/DailyActivity"
    SleepActivity = "/Users/julesgransden/Desktop/Perso Projects/HealthFitnessApp/Code/DailySLeep"
    users = {"1503960366": 1, "3977333714":12, "4702921684":19, "5553957443":20, "5577150313":21, "6962181067":25, "8378563200":30}
    #returns user health data as dataframe
    df = OrganiseData(users[userID], Unorganised, DailyActivity, SleepActivity)
    df.to_csv("he.csv")
    
    for index,row in df.iterrows():
        cursor = db.cursor()
        sql = "INSERT INTO health_data (user_id, activity_date, TotalSteps, TotalDistance, VeryActiveMinutes, FairlyActiveMinutes, LightlyActiveMinutes, SedentaryMinutes, Calories, TotalTimeAsleep, TotalTimeInBed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (userID, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        cursor.execute(sql, values)
        db.commit()


    