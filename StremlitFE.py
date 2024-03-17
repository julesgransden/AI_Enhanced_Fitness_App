import streamlit as st
from streamlit_option_menu import option_menu
from ViewData import *
from Displayfunctions import *
from WorkoutAI import *
from RecomendationAI import *
from Wrapped import *
from MedicalLLMAgent import *
from LoginPage import *
from databse import *
from NearbyClinic import *

st.set_option('deprecation.showPyplotGlobalUse', False)



def Main(name):
    
    st.set_page_config(
        page_title="BeBetter2.0",
        page_icon="❤️",
        layout = "wide"
    )
    
    st.sidebar.image('BeBetter2.0.png')
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
            options=["Home", "Health Data", "Workouts", "Wrapped", "Injuries"],
            icons=["house", "activity", "chat-right-heart", "person-arms-up", "bandaid"],#bootstrap icons
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Home":
        st.header(f'Welcome back {name.upper()} !', divider='grey')
        st.markdown("This is a new state-of-the-art health and fitness app.\nHere you can not only visualize your health data collected by your fitbit device,\nbut, also, utilize openAI's very powerful GPT3.5-turbo API to:\n- Provide you with a set of recommendations and general health evaluations based\n on your health data.\n- Create a personalized fitness regiment(workout schedule) based on your goals and\n personal details as well as your fitbit data!\n- Keep Track,Treat and monitor injuries that occur during trainings or workouts. ")
        st.subheader("Lets's take a look at your Health Data ... ")

    elif selected == "Health Data":
        userID = get_ID(name)
        df = getHealthData(userID)
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
        userID = get_ID(name)
        df = getHealthData(userID)
        # Collect user input
        cursor = db.cursor()
        # Query the database to retrieve user-specific data
        query = f"SELECT age FROM persoInfo WHERE name = '{name}';"
        cursor.execute(query)
        age = cursor.fetchone()[0]
        query = f"SELECT gender FROM persoInfo WHERE name = '{name}';"
        cursor.execute(query)
        gender = cursor.fetchone()[0]
        query = f"SELECT weight FROM persoInfo WHERE name = '{name}';"
        cursor.execute(query)
        weight = cursor.fetchone()[0]
        query = f"SELECT height FROM persoInfo WHERE name = '{name}';"
        cursor.execute(query)
        height = cursor.fetchone()[0]
        st.write("Tell us about your goals to help our AI model get a better understanding of your needs: ")
        equipment = st.selectbox("Availability of workout equipment", options=["I don't have access to any sort of gym equipment","I have access to an outdoor gym","I only access to a small home gym", "I have access to a fully equipped gym"])
        goals = st.text_input("Fitness goals of the individual")
        #Avg data info
        ASteps = getAvgSteps(df)
        ASleeps = getAvgSleep(df)
        ACals = getAvgCaloriesBurned(df)
        AActiv = getAvgActivity(df)
        ADistance = getAvgDistance(df)
        
        submit = st.button('Generate Workout')
        
        ActiveInjury = IsInjured(userID)
        
        if submit:
            work = Workout(age,gender,height,weight,equipment,goals,ASleeps,ASteps,ADistance,AActiv,ACals)
            if ActiveInjury:
                active = ActivationSet(ActiveInjury,age,gender,height,weight,equipment)
                st.subheader("Activation:")
                st.write(active)
            st.subheader("Workout Plan:")
            st.write(work)

        
    elif selected == "Wrapped":
        userID = get_ID(name)
        df = getHealthData(userID)
        
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

    elif selected == "Injuries":

        st.title("Did you get hurt?")
        tab1, tab2, tab3= st.tabs(["Medical Chatbot", "Find Medical Clinic", "Injury history"])
        
        with tab1:
            ChatBot()
            
        with tab2:
            
            clinics = ReturnNearestPlace("Medicval Clinics")
            st.subheader("Here are some medical clinics OPEN nearby")
            # Display each clinic name and link
            for index, row in clinics.iterrows():
                st.write(f"**{row['name']}**")
                st.write(f"Preview: [{row['url']}]({row['url']})")
                        
        with tab3:
            userID = get_ID(name)
            df = getInjuryData(userID)
            st.write(df)
            
            st.markdown("Add a new injury to your profile: ")
            date, injury = st.columns(2)

            with date:
                date_input = st.text_input("Date of injury (MM/YYYY):")

            with injury:
                injury_input = st.text_input("Describe injury:")
            upload = st.button("Upload")  
            if upload and date and injury:
                # Reset the values of text inputs
                uploadInjurytoDB(userID, date_input, injury_input)
            
            st.markdown("have you recovered from your injury?")
            listOfInjuries = getListOfInjuries(userID)
            date = st.selectbox("which one?", listOfInjuries)
            recovered = st.button("Recovered!")
            if recovered:
                UpdateRecovered(userID,date)
       
    logout_button = st.sidebar.button('Logout')
    if logout_button:
        st.session_state.logged_in = False
        st.session_state.name = None        
            
if __name__ == "__main__":
    cursor = db.cursor()
    # Initialize session state (only once)
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # Initialize login state

    if not st.session_state.logged_in:
        st.title('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        login_button = st.button('Login')

        if login_button:
            if authenticate(username, password):
                st.session_state.logged_in = True  # Set login state to True
                query = f"SELECT name FROM persoInfo WHERE username = '{username}';"
                cursor.execute(query)
                name = cursor.fetchone()[0]
                st.session_state.name = name
            else:
                st.error('Invalid credentials')
    else:  # Check if logged in and username is not None
        Main(st.session_state.name)  
