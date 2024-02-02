# Health_Fitness_App
This app allows user to view health data collected from a fitbit wearable fitness device. With this information, and the use of openAI's public API, I was able to integrate daily health recommendations as well as, the option to generate a personalized workout based on your personal information, past health data and goals.

## Data 
I obtained this data from https://www.kaggle.com/datasets/arashnic/fitbit, which gathered a month of health and fitness information for more than 30 participants. I parsed and organized these files, which allowed me to present the individuals daily and monthly achievements and statistics. 
After performing a various sequence of operations as seen in ViewData.py, this is a sample of the dataframe obtained.

<img width="988" alt="Screen Shot 2024-02-02 at 6 12 00 PM" src="https://github.com/julesgransden/Health_Fitness_App/assets/78057184/eabcbe17-0d54-4911-9a1f-2fa3eaef118e">


## OpenAI
Using OpenAI's "GPT-3.5-Turbo" API, I was able to create personalized functions which allowed me to not only develope a AI that uses your health data to generate lifestyle recommendations, but also recommend workouts for our user. 



