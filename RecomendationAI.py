from openai import OpenAI
import json

#This will provide recomendations based on your daily health and fitness data

client = OpenAI(api_key="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")

# Define a function for recommendation on daily health stats
def get_health_recommendations(sleep, steps, distance, active, calories):
    """Generate health recommendations based on provided data."""
    # Determine sleep recommendation
    if sleep < 7:
        sleep_recommendation = f"The daily average sleep time of {sleep:.2f} hours is below the recommended amount of 7-9 hours for adults. It's important to prioritize improving sleep duration and quality."
    elif sleep >= 7 and sleep <= 9:
        sleep_recommendation = f"Your sleep duration of {sleep:.2f} hours falls within the recommended range of 7-9 hours for adults, which is excellent."
    else:
        sleep_recommendation = f"Your sleep duration of {sleep:.2f} hours exceeds the recommended range of 7-9 hours for adults. While longer sleep may not necessarily be harmful, ensure the quality of your sleep."
    
    # Determine activity recommendation based on steps and distance
    if steps >= 10000 and distance >= 5:
        activity_recommendation = f"Walking {steps} steps daily, covering a distance of {distance} miles, shows that you're meeting the recommended daily activity levels. Keep up the good work!"
    else:
        activity_recommendation = f"Walking {steps} steps daily, covering a distance of {distance} miles, is a positive start, but consider increasing your activity levels to meet the recommended targets."
    
    # Determine caloric burn recommendation
    if calories >= 2000:
        calories_recommendation = f"Burning an average of {calories} calories daily indicates an active lifestyle, which is commendable."
    else:
        calories_recommendation = f"Consider increasing your daily caloric burn to support a more active lifestyle."
    
    # Construct the final recommendation message
    recommendation_message = (
        "Based on the data provided, it seems that there are some areas where improvements could be made to achieve a healthier lifestyle:\n\n"
        f"Sleep: {sleep_recommendation}\n\n"
        f"Physical Activity: {activity_recommendation}\n\n"
        f"Caloric Burn: {calories_recommendation}\n\n"
        "In summary, while there are aspects of your lifestyle that are positive, such as your physical activity levels, there are opportunities for improvement, particularly in sleep duration and caloric burn."
    )
    
    return recommendation_message



def Recommendations(sleep, steps, distance, active_time, calories):

    messages = [
        {"role": "user", "content": "Am I living a healthy lifestyle based on this data?"},
        {"role": "user", "content": f"My Daily average sleep time is {sleep} hours."},
        {"role": "user", "content": f"I walk {steps} steps daily, covering a distance of {distance} miles."},
        {"role": "user", "content": f"I spend {active_time} minutes daily being active."},
        {"role": "user", "content": f"I burn {calories} calories daily."},
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_health_recommendations",
                "description": "Get health recommendation and review on Daily Average of Sleep, Steps, Distance, Active time and Calories burned. Be very specific",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sleep": {
                            "type": "integer",
                            "description": "Average daily sleep time in hours",
                        },
                        "steps": {
                            "type": "integer",
                            "description": "Daily average number of steps taken by an individual",
                        },
                        "distance": {
                            "type": "integer",
                            "description": "Daily average distance traveled by an individual",
                        },
                        "activeTime": {
                            "type": "integer",
                            "description": "Daily average time spent active by an individual",
                        },
                        "calories": {
                            "type": "integer",
                            "description": "Average number of calories burned in a day by an individual",
                        },
                    },
                    "required": ["sleep", "steps", "distance", "activeTime", "calories"],
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
            "get_health_recommendations": get_health_recommendations,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
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
        
