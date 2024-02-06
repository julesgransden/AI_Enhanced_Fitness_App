import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
import numpy as np


def DisplaySingleBarInfo(df, dateCol, dataCol):
    # Define plot size
    plt.figure(figsize=(12, 8))

    # Parse dates using the appropriate format
    df[dateCol] = pd.to_datetime(df[dateCol], format='%d/%m')  

    # Plot data
    plt.bar(df[dateCol], df[dataCol], color='orange', linewidth=3)

    plt.xlabel('Date', fontsize=14, fontweight='bold')
    if dataCol == "TotalSteps":
        plt.ylabel("Steps", fontsize=14, fontweight='bold')
    elif dataCol == "TotalDistance":
        plt.ylabel("Distance (miles)", fontsize=14, fontweight='bold')
    else:
        plt.ylabel(dataCol, fontsize=14, fontweight='bold')

    # Customize x-axis ticks to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))  
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  

    # Set the x-axis limits to start and end exactly where the data starts and ends
    plt.xlim(df[dateCol].min(), df[dateCol].max())

    # Rotate the x-axis labels for better visibility
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=14)

    # Adjust layout to prevent clipping of labels
    plt.tight_layout()  
    
    #Add average
    plt.axhline(y=np.nanmean(df[dataCol]), color='red', linestyle='--', linewidth=3, alpha = 0.4, label='Avg')
    
    plt.legend()

    plt.show()
    
def DisplayMultipleBarInfo(df, StartCol, EndCol, bar_width=0.35, bar_offset=0.1):
    # Assuming the second column contains the dates, adjust if needed
    date_column = df.columns[0]

    plt.figure(figsize=(12, 8))

    # Parse dates using the appropriate format
    df[date_column] = pd.to_datetime(df[date_column], format='%d/%m')  

    # Plot data side by side
    for i, column in enumerate(df.columns[StartCol:EndCol]):
        # Calculate x positions for bars
        x_positions = mdates.date2num(df[date_column]) + i * (bar_width + bar_offset)
        plt.bar(x_positions, df[column], width=bar_width, label=column)

    plt.xlabel('Date', fontsize=14, fontweight='bold')
    if df.columns[StartCol] == "VeryActiveMinutes":
        plt.ylabel("Time (minutes)", fontsize=14, fontweight='bold')
    elif df.columns[StartCol] == "TotalTimeAsleep":
        plt.ylabel("Time (hours)", fontsize=14, fontweight='bold')

    # Make the minor ticks and gridlines show.
    plt.minorticks_on()

    # Customize x-axis ticks to show dates nicely
    plt.xticks(rotation=45, fontsize=12)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))

    plt.yticks(fontsize=14)

    # Show the legend
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
    
def DisplayCaloriesRelationship(curr):
    #first: Calories vs Steps vs SedentaryMinutes

    rel = curr[['Calories','TotalSteps', 'SedentaryMinutes']].copy()
    rel = rel[(rel != 0).any(axis=1)]


    plt.figure(figsize=(12, 8))  # Set figure size before plotting

    # Set x-axis label
    plt.xlabel('Calories', fontsize=14)

    # Scatter plot with the first y-axis on the left (Steps)
    scatter1 = plt.scatter(rel.iloc[:, 0], rel.iloc[:, 1], color='red', label='Steps')
    plt.ylabel('Daily Steps', fontsize=14)

    # Fit linear regression to Steps data
    steps_x = rel.iloc[:, 0].values.reshape(-1, 1)
    steps_y = rel.iloc[:, 1].values
    steps_model = LinearRegression().fit(steps_x, steps_y)
    steps_trendline = steps_model.predict(steps_x)
    plt.plot(rel.iloc[:, 0], steps_trendline, color='red', alpha = 0.3)

    # Create a twin Axes sharing the x-axis, which will have the second y-axis on the right (Distance)
    ax2 = plt.gca().twinx()
    scatter2 = plt.scatter(rel.iloc[:, 0], rel.iloc[:, 2], color='blue', label='Time Sedentary')
    plt.ylabel('Time Sedentary (minutes)', fontsize=14)

    # Fit linear regression to Distance data
    distance_x = rel.iloc[:, 0].values.reshape(-1, 1)
    distance_y = rel.iloc[:, 2].values
    distance_model = LinearRegression().fit(distance_x, distance_y)
    distance_trendline = distance_model.predict(distance_x)
    plt.plot(rel.iloc[:, 0], distance_trendline, color='blue', alpha = 0.3)

    # Manually create the legend with both scatter plots and trendlines
    plt.legend(handles=[scatter1, scatter2], loc='upper left')

    plt.show()

def DisplaySleepTimeRelationship(curr):
    #we miust initially create a sub dataframe and give it our data we want to plot
    #We also will add the fairly active and very active minutes to give us a better representation of this persons
    #active time that day
    slp =  curr[['TotalTimeAsleep', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'TotalSteps']].copy()
    slp = slp[slp['TotalTimeAsleep'] != 0]
    slp['ActiveMinutes'] = slp['VeryActiveMinutes'] + slp['FairlyActiveMinutes']
    slp.drop('VeryActiveMinutes', axis =1, inplace =True)
    slp.drop('FairlyActiveMinutes', axis =1, inplace =True)
    
    plt.figure(figsize=(12, 8))  # Set figure size before plotting


    # Set x-axis label
    plt.xlabel('Time Asleep (hours)', fontsize=14)


    # Scatter plot with the first y-axis on the left (Steps)
    scatter1 = plt.scatter(slp.iloc[:, 0], slp.iloc[:, 1], color='red', label='Steps')
    plt.ylabel('Daily Steps', fontsize=14)

    # Fit linear regression to Steps data
    steps_x = slp.iloc[:, 0].values.reshape(-1, 1)
    steps_y = slp.iloc[:, 1].values
    steps_model = LinearRegression().fit(steps_x, steps_y)
    steps_trendline = steps_model.predict(steps_x)
    plt.plot(slp.iloc[:, 0], steps_trendline, color='red', alpha = 0.3)

    # Create a twin Axes sharing the x-axis, which will have the second y-axis on the right (Distance)
    ax2 = plt.gca().twinx()
    scatter2 = plt.scatter(slp.iloc[:, 0], slp.iloc[:, 2], color='blue', label='Active Time')
    plt.ylabel('Active Minutes', fontsize=14)

    # Fit linear regression to Distance data
    distance_x = slp.iloc[:, 0].values.reshape(-1, 1)
    distance_y = slp.iloc[:, 2].values
    distance_model = LinearRegression().fit(distance_x, distance_y)
    distance_trendline = distance_model.predict(distance_x)
    plt.plot(slp.iloc[:, 0], distance_trendline, color='blue', alpha = 0.3)


    # Manually create the legend with both scatter plots and trendlines
    plt.legend(handles=[scatter1, scatter2], loc='upper left')

    plt.show()

def DisplayTimeToFallAsleepRelationship(curr):
    #we miust initially create a sub dataframe and give it our data we want to plot
    #We also will add the fairly active and very active minutes to give us a better representation of this persons
    #active time that day
    slp =  curr[['TotalTimeAsleep','TotalTimeInBed', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'TotalSteps']].copy()
    slp = slp[slp['TotalTimeAsleep'] != 0]
    slp['ActiveMinutes'] = slp['VeryActiveMinutes'] + slp['FairlyActiveMinutes']
    slp['TimeToFallAsleep'] = slp['TotalTimeInBed'] - slp['TotalTimeAsleep']
    slp.drop(['VeryActiveMinutes', 'FairlyActiveMinutes','TotalTimeAsleep','TotalTimeInBed',], axis =1, inplace =True)
    # Extract the 'TimeToFallAsleep' column
    time_to_fall_asleep = slp.pop('TimeToFallAsleep')

    # Insert the 'TimeToFallAsleep' column at position 0
    slp.insert(0, 'TimeToFallAsleep', time_to_fall_asleep)

    plt.figure(figsize=(12, 8))  # Set figure size before plotting


    # Set x-axis label
    plt.xlabel('Time to fall Asleep (hours)', fontsize=14)


    # Scatter plot with the first y-axis on the left (Steps)
    scatter1 = plt.scatter(slp.iloc[:, 0], slp.iloc[:, 1], color='red', label='Steps')
    plt.ylabel('Daily Steps', fontsize=14)

    # Fit linear regression to Steps data
    steps_x = slp.iloc[:, 0].values.reshape(-1, 1)
    steps_y = slp.iloc[:, 1].values
    steps_model = LinearRegression().fit(steps_x, steps_y)
    steps_trendline = steps_model.predict(steps_x)
    plt.plot(slp.iloc[:, 0], steps_trendline, color='red', alpha = 0.3)

    # Create a twin Axes sharing the x-axis, which will have the second y-axis on the right (Distance)
    ax2 = plt.gca().twinx()
    scatter2 = plt.scatter(slp.iloc[:, 0], slp.iloc[:, 2], color='blue', label='Active Time')
    plt.ylabel('Active Minutes', fontsize=14)

    # Fit linear regression to Distance data
    distance_x = slp.iloc[:, 0].values.reshape(-1, 1)
    distance_y = slp.iloc[:, 2].values
    distance_model = LinearRegression().fit(distance_x, distance_y)
    distance_trendline = distance_model.predict(distance_x)
    plt.plot(slp.iloc[:, 0], distance_trendline, color='blue', alpha = 0.3)


    # Manually create the legend with both scatter plots and trendlines
    plt.legend(handles=[scatter1, scatter2], loc='upper left')

    plt.show()




