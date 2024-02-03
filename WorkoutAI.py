from openai import OpenAI
import json

##This function will return a personalized workout based on your oersonal information and goals. BUT will also
#Take into account the information provided by your fitbit.

client = OpenAI(api_key="YOUR_API_KEY")

# Define a function for recommendation on daily health stats
def get_Workout(age, gender, height, weight, equipment, goals, sleep, steps, distance, active, calories):
    
    # Check if parameters are None and provide default values
    age = age if age is not None else 30  # Replace with a suitable default age
    gender = gender if gender is not None else "Male"  # Replace with a suitable default gender
    height = height if height is not None else 170  # Replace with a suitable default height
    weight = weight if weight is not None else 70  # Replace with a suitable default weight
    equipment = equipment if equipment is not None else "None"  # Replace with a suitable default equipment availability
    goals = goals if goals is not None else "General Fitness"  # Replace with a suitable default fitness goals


    """Generate a personalized workout schedule"""
    # Your logic to generate the workout schedule based on the provided information goes here
    # This function should return a string containing the personalized workout schedule
    workout_schedule = f"Workout Schedule for {age} year old {gender}:\n"
    workout_schedule += f"Height: {height} cm, Weight: {weight} kg\n"
    workout_schedule += f"Availability of workout equipment: {equipment}\n"
    workout_schedule += f"Goals: {goals}\n"
    workout_schedule += "Based on your health stats:\n"
    workout_schedule += f"Sleep: {sleep} hours\n"
    workout_schedule += f"Steps: {steps} steps, Distance: {distance} miles\n"
    workout_schedule += f"Active Time: {active} minutes\n"
    workout_schedule += f"Calories Burned: {calories} calories\n"
    # Your logic to generate the workout schedule based on the health stats recommendations
    # Add recommendations and personalized workout plan here
    return workout_schedule

def Workout(age, gender, height, weight, equipment, goals, sleep, steps, distance, active_time, calories):

    messages = [
        {"role": "user", "content": "Generate a detailed workout schedule, with exercise, number of repetitions and number of series for each exercise, for me based on this data"},
        {"role": "user", "content": f"My average sleep time is {sleep} hours."},
        {"role": "user", "content": f"I walk {steps} steps daily, covering a distance of {distance} miles."},
        {"role": "user", "content": f"I spend {active_time} minutes daily being active."},
        {"role": "user", "content": f"I burn {calories} calories daily."},
        {"role": "user", "content": f"I am {age} years old."},
        {"role": "user", "content": f"My gender is {gender}."},
        {"role": "user", "content": f"My height is {height} cm."},
        {"role": "user", "content": f"My weight is {weight} kg."},
        {"role": "user", "content": f"I have access to {equipment} workout equipment."},
        {"role": "user", "content": f"My fitness goals are: {goals}."}
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_Workout",
                "description": "Generate a personalized workout schedule",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "age": {"type": "integer", "description": "Age of the individual"},
                        "gender": {"type": "string", "description": "Gender of the individual"},
                        "height": {"type": "integer", "description": "Height of the individual in cm"},
                        "weight": {"type": "integer", "description": "Weight of the individual in kg"},
                        "equipment": {"type": "string", "description": "Availability of workout equipment"},
                        "goals": {"type": "string", "description": "Fitness goals of the individual"},
                        "sleep": {"type": "integer", "description": "Average daily sleep time in hours"},
                        "steps": {"type": "integer", "description": "Daily average number of steps taken by an individual"},
                        "distance": {"type": "integer", "description": "Daily average distance traveled by an individual"},
                        "activeTime": {"type": "integer", "description": "Daily average time spent active by an individual"},
                        "calories": {"type": "integer", "description": "Average number of calories burned in a day by an individual"},
                    },
                    "required": ["age", "gender", "height", "weight", "equipment", "goals", "sleep", "steps", "distance", "activeTime", "calories"],
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_Workout": get_Workout,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                age=function_args.get("age"),
                gender=function_args.get("gender"),
                height=function_args.get("height"),
                weight=function_args.get("weight"),
                equipment=function_args.get("equipment"),
                goals=function_args.get("goals"),
                sleep=function_args.get("sleep"),
                steps=function_args.get("steps"),
                distance=function_args.get("distance"),
                active=function_args.get("activeTime"),  # Corrected parameter name
                calories=function_args.get("calories"),   
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response

        result = (second_response.choices[0].message).content
        return result
    
