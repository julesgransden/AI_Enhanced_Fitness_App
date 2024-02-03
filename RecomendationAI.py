from openai import OpenAI
import json

#This will provide recomendations based on your daily health and fitness data

client = OpenAI(api_key="YOUR_API_KEY")

# Define a function for recommendation on daily health stats
def get_health_recommendations(sleep, steps, distance, active, calories):
    """Give a health review for a 18-65 year old adult"""
    return json.dumps({"sleep": sleep, "steps":steps, "distance":distance, "activeTime":active, "calories":calories})

def Recommendations(sleep, steps, distance, active_time, calories):

    messages = [
        {"role": "user", "content": "Am I living a healthy lifestyle based on this data?"},
        {"role": "user", "content": f"My average sleep time is {sleep} hours."},
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
        
