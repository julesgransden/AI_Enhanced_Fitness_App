import streamlit as st
import pdfkit
from streamlit_option_menu import option_menu
from ViewData import *
from Displayfunctions import *
from WorkoutAI import *
from RecomendationAI import *
from Wrapped import *


def download_pdf(text_content, filename):
    pdfkit.from_string(text_content, filename)
    
    
st.set_option('deprecation.showPyplotGlobalUse', False)

#Let's define our data files
Unorganised = "/Users/julesgransden/Desktop/Perso Projects/HealthFitnessApp/Code/FitDB/dailyActivity_merged.csv"
DailyActivity = "/Users/julesgransden/Desktop/Perso Projects/HealthFitnessApp/Code/DailyActivity"
SleepActivity = "/Users/julesgransden/Desktop/Perso Projects/HealthFitnessApp/Code/DailySLeep"



# Initialize the session state
if 'selected_individual' not in st.session_state:
    st.session_state.selected_individual = None

st.sidebar.image('BeBetter.png')
    
st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: black;
        }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Health Data", "Workouts", "Wrapped"],
        icons=["house", "activity", "chat-right-heart", "person-arms-up"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.header('Welcome!', divider='grey')
    st.text("This is a new state-of-the-art health and fitness app.\nHere you can not only visualize your health data collected by your fitbit device,\nbut, also, utilize openAI's very powerful GPT3.5-turbo API to:\n- Provide you with a set of recommendations and general health evaluations based\n on your health data.\n- Create a personalized fitness regiment(workout schedule) based on your goals and\n personal details as well as your fitbit data!")
    st.text("Note: Since this is a demo version, you may not provide your own data.\nfitbit data from various individuals has been sourced and stored, for this purpose.")
    st.subheader('Start by selecting the individual who\'s information we will retrieve:')
    # Use session state to persist the selected individual
    st.session_state.selected_individual = st.slider("There are 32 individuals to pick from, Select one...", 1, 32, 1)
    st.write("Awesome! You selected individual number", st.session_state.selected_individual)
    #dataframe 
    
elif selected == "Health Data":
    indiv = int(st.session_state.selected_individual)
    df = OrganiseData(indiv, Unorganised, DailyActivity, SleepActivity)
    st.title("Your Data!")
    #get daily averages
    ASteps = getAvgSteps(df)
    ASleeps = getAvgSleep(df)
    ACals = getAvgCaloriesBurned(df)
    AActiv = getAvgActivity(df)
    ADistance = getAvgDistance(df)
    st.subheader("Your Daily Averages:")
    # Format and display values side by side
    st.markdown(
    f"<div style='display: flex; flex-direction: row; align-items: center;'>"
    f"<div style='margin-right: 20px;'><b>Steps:</b> You took an average of <b>{ASteps} steps per day</b></div>"
    f"<div style='margin-right: 20px;'><b>Sleep:</b> You slept an average of <b>{int(ASleeps)} hours per night</b></div>"
    f"<div style='margin-right: 20px;'><b>Calories Burned:</b> You burned an average of <b>{ACals} calories per day</b></div>"
    f"<div style='margin-right: 20px;'><b>Activity:</b> You were active for an average of <b>{AActiv} minutes per day</b></div>"
    f"<div><b>Distance:</b> You traveled an average of <b>{ADistance} miles per day</b></div>"
    f"</div>",
    unsafe_allow_html=True
    )
    st.write(" ")
    st.write(" ")
    st.write("**Click here to get an AI generated healthy lifestyle review!**")
    generate = st.button('AI Health Recap')
    if generate:
        st.write(Recommendations(ASleeps,ASteps,ADistance,AActiv,ACals))
    
    tab1, tab2= st.tabs(["Data", "Correlations"])
    
    with tab1:
        # Access the selected individual from session state
        st.subheader("_Steps_")
        st.pyplot(DisplaySingleBarInfo(df,"Date","TotalSteps"))
        
        st.subheader("_Distance Traveled_")
        st.pyplot(DisplaySingleBarInfo(df,"Date","TotalDistance"))
        
        st.subheader("_Sleep_")
        st.pyplot(DisplayMultipleBarInfo(df,8,10))
        st.write('_Note: some individuals didn\'t wear their watches to sleep everynight... Resulting in poor sleep data_' )
        
        st.subheader("_Calories_")
        st.pyplot(DisplaySingleBarInfo(df,"Date","Calories"))
        
        st.subheader("_Active Time_")
        st.pyplot(DisplayMultipleBarInfo(df,3,7))
        
    #Corelations in the data
    with tab2:
        st.header("Lets look at some correlations in your data:")
        st.subheader("_Calories vs Steps vs Sedentary Time_")
        st.pyplot(DisplayCaloriesRelationship(df))
        
        st.subheader("_Sleep Time vs Steps vs Active Time_")
        st.pyplot(DisplaySleepTimeRelationship(df))
        
        st.subheader("_Time to fall asleep vs Steps vs Active Time_")
        st.pyplot(DisplayTimeToFallAsleepRelationship(df))
    
elif selected == "Workouts":
    st.title("AI Workouts")
    indiv = int(st.session_state.selected_individual)
    df = OrganiseData(indiv, Unorganised, DailyActivity, SleepActivity)
    # Collect user input
    st.write("Enter some personal information to help our AI model get a better understanding of your needs: ")
    age = st.number_input("Age of the individual", min_value=0, step=1)
    gender = st.radio("Gender of the individual", options=["Male", "Female"])
    height = st.number_input("Height of the individual (cm)", min_value=0, step=1)
    weight = st.number_input("Weight of the individual (kg)", min_value=0, step=1)
    equipment = st.selectbox("Availability of workout equipment", options=["I don't have access to any sort of gym equipment","I have access to an outdoor gym","I only access to a small home gym", "I have access to a fully equipped gym"])
    goals = st.text_input("Fitness goals of the individual")
    #Avg data info
    ASteps = getAvgSteps(df)
    ASleeps = getAvgSleep(df)
    ACals = getAvgCaloriesBurned(df)
    AActiv = getAvgActivity(df)
    ADistance = getAvgDistance(df)
    
    submit = st.button('Generate Workout')
    
    st.subheader("Here is your personalized weekly workout plan: ")
    if submit:
        work = Workout(age,gender,height,weight,equipment,goals,ASleeps,ASteps,ADistance,AActiv,ACals)
        st.write(work)

    
elif selected == "Wrapped":
    indiv = int(st.session_state.selected_individual)
    df = OrganiseData(indiv, Unorganised, DailyActivity, SleepActivity)
    
    # Get averages and totals
    ASleeps = getAvgSleep(df)
    TSleeps = getTotalSleep(df)
    ACals = getAvgCaloriesBurned(df)
    TCals = getTotalCaloriesBurned(df)
    ADistance = getAvgDistance(df)
    TDistance = getTotalDistance(df)
    ASteps = getAvgSteps(df)
    TSteps = getTotalSteps(df)
    AActivity = getAvgActivity(df)
    TActivity = getTotalActivity(df)
    
    # Title and introduction
    st.title("🎉Your Month's Activity Wrapped!🎉")
    st.markdown("Here's a summary of your activity for the past month:")

    # Sleep section
    st.markdown("## Sleep")
    st.markdown(f"**Total Sleep:** {int(TSleeps)} hours")
    st.markdown(f"**Average Sleep:** {ASleeps:.2f} hours per day")

    # Calories section
    st.markdown("## Calories Burned")
    st.markdown(f"**Total Calories Burned:** {TCals} calories")
    st.markdown(f"**Average Calories Burned:** {ACals} calories per day")

    # Distance section
    st.markdown("## Distance")
    st.markdown(f"**Total Distance:** {TDistance} miles")
    st.markdown(f"**Average Distance:** {ADistance:.2f} miles per day")

    # Steps section
    st.markdown("## Steps")
    st.markdown(f"**Total Steps:** {TSteps} steps")
    st.markdown(f"**Average Steps:** {ASteps} steps per day")

    # Activity section
    st.markdown("## Activity")
    st.markdown(f"**Total Activity:** {TActivity} minutes")
    st.markdown(f"**Average Activity:** {AActivity} minutes per day")

    # Add some extra styling
    st.markdown(
        """
        <style>
            /* Title */
            .css-1k0jdt6 {
                font-family: "Comic Sans MS", cursive, sans-serif;
                font-size: 36px;
                color: #000000;  /* Black color */
            }
            /* Section headings */
            h2 {
                font-family: "Arial", sans-serif;
                font-size: 24px;
                color: #000000;  /* Black color */
            }
            /* Text */
            p {
                font-family: "Verdana", sans-serif;
                font-size: 18px;
                color: #000000;  /* Black color */
            }
        </style>
        """,
        unsafe_allow_html=True
    )
