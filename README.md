

# Health and Fitness App 🏋️‍♂️💪

## Overview
Welcome to our state-of-the-art health and fitness app! This app allows you to visualize your health data collected by your Fitbit device and provides various features to help you achieve your fitness goals.

## Data 
I obtained this data from https://www.kaggle.com/datasets/arashnic/fitbit, which gathered a month of health and fitness information for more than 30 participants. I parsed and organized these files, which allowed me to present the individuals daily and monthly achievements and statistics. 
After performing a various sequence of operations as seen in ViewData.py, this is a sample of the dataframe obtained.

<img width="988" alt="Screen Shot 2024-02-02 at 6 12 00 PM" src="https://github.com/julesgransden/Health_Fitness_App/assets/78057184/eabcbe17-0d54-4911-9a1f-2fa3eaef118e">


## Using OpenAI API

In this project, I have integrated OpenAI's powerful GPT-3.5-Turbo API to enhance the functionality of the health and fitness app. Specifically, I have utilized the API to provide personalized recommendations based on the user's daily health and fitness data, as well as to generate personalized workout plans.

#### Personalized Workout Plans

The function `Workout` takes various personal parameters such as age, gender, height, weight, availability of workout equipment, and fitness goals. It also considers the individual's health data from Fitbit, including average sleep time, daily steps, distance traveled, active time, and calories burned. Using these inputs, the function generates a personalized workout schedule tailored to the user's needs and past health data.

#### Health Recommendations

The `Recommendations` function analyzes the user's daily health and fitness data, including average sleep time, daily steps, distance traveled, active time, and calories burned. It then utilizes OpenAI's API to provide personalized health recommendations and lifestyle reviews based on this data. These recommendations aim to help the user assess their current lifestyle and make informed decisions to improve their overall health and well-being.

These integrations with OpenAI's API enhance the app's capabilities by providing personalized insights and recommendations based on the user's health data, contributing to a more comprehensive and tailored user experience.



## Features
- **Data Visualization**: Visualize your health data including steps taken, distance traveled, sleep patterns, calories burned, and activity levels.
- **AI Recommendations**: Get personalized recommendations and general health evaluations based on your health data using OpenAI's powerful GPT3.5-turbo API.
- **Personalized Workouts**: Create a personalized fitness regimen (workout schedule) based on your goals and personal details as well as your Fitbit data.
- **Monthly Activity Wrap-up**: Get a summary of your activity for the past month, including sleep, calories burned, distance traveled, steps taken, and activity levels.

## Getting Started
1. **Installation**: Clone this repository to your local machine.
2. **Setup**: Install the required dependencies using `pip install -r requirements.txt`.
3. **Run the App**: Execute the `streamlit run app.py` command to launch the app.
4. **Select Individual**: Start by selecting the individual whose information you want to retrieve.
5. **Explore**: Explore the different sections of the app, including home, health data, workouts, and monthly activity wrap-up.

## Usage
- **Home**: Learn about the app and select the individual whose data you want to view.
- **Health Data**: Visualize your health data and get personalized recommendations.
- **Workouts**: Input personal information to generate a personalized workout plan.
- **Monthly Activity Wrap-up**: View a summary of your activity for the past month.

## License
This project is licensed under the [MIT License](LICENSE).

