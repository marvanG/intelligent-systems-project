from furhat_remote_api import FurhatRemoteAPI
import json
import random

from sympy import false
import requests

furhat = FurhatRemoteAPI('localhost')
# functions
def color(color): # changes lightning color
    if color == "blue": # speaking
        furhat.set_led(red=0, green=0, blue=200)
    elif color == "green": # listening
        furhat.set_led(red=0, green=200, blue=0)
    elif color == "yellow": # thinking
        furhat.set_led(red=200, green=200, blue=0)
    elif color == "red": # error
        furhat.set_led(red=200, green=0, blue=0)
    elif color == "purple": # Drunk warning
        furhat.set_led(red=200, green=0, blue=200)
    elif color == "white": # Sober warning
        furhat.set_led(red=200, green=200, blue=200)
    elif color == "reset": # reset
        furhat.set_led(red=0, green=0, blue=0)


def listen(): # listens to user
    color("green")
    result = furhat.listen().message
    print(f'Customer: {result}')
    color("reset")
    return result

def say(message): # speaks to user
    color("blue")
    furhat.say(text = message, blocking=True)
    print(f'MAECK: {message}')
    color("reset")

def yes(): # Answers yes in random words
    with open('facts.json','r') as file:
        data = json.load(file)

    random_yes_answer = random.choice(list(data['say_yes'].values()))
    return random_yes_answer

random_yes_answer = yes()
print(f"random answer : {random_yes_answer}")

def no(): #Answers no in random words
    with open('facts.json','r') as file:
        data = json.load(file)

    random_no_answer = random.choice(list(data['say_no'].values()))
    return random_no_answer

random_no_answer = no()
print(f"random no: {random_no_answer} ")    

def what_drink(result): #Random selection of drinks
    with open('facts.json','r') as file:
        data=json.load(file)
   
    
    drinks_list = list(data['available_drinks'].values())
    print(drinks_list)

    matching_drinks = [drink for drink in drinks_list if drink.lower() in result]
    print(matching_drinks)
    
    if matching_drinks:
       my_drink = matching_drinks[0]
       my_drink = ''.join(my_drink)    
       #random_drink = random.choice(list(data['available_drinks'].values()))
       return my_drink
    

def no_answer(): #If the robot recieves no answer or answers it doesnt understand
    with open('facts.json','r') as file:
       data = json.load(file)
    
    random_non_answer = random.choice(list(data["no_answer"].values()))
    return random_non_answer




#def sad_costumer():
    

#def angry_costumer():


#def happy_costumer():        





              






# AI functions
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
def clean_response(response):

    print(f'\nResponse: {response}\n')
    generated_text = response[0]["generated_text"]
    if generated_text.strip() != "":
        response = generated_text.strip()
        if (response.startswith('"') and response.endswith('"')) or (response.startswith("'") and response.endswith("'")):
            response = response[1:-1]  # Remove the first and last character
    else:
        response = "No response"
    return response

def query(API_URL, headers, chat_history, input_instructions):
    chat_history
    chat_history_list = chat_history.split('\n')
    if len(chat_history_list) > 10:
        chat_history_list = chat_history_list[-10:]
    
    last_10_lines = '\n'.join(chat_history_list)

    ai_input = f"{input_instructions + last_10_lines}MAECK:"
    print(f'ai input: {ai_input}')
    payload = {
        "inputs": ai_input,
        "parameters": {
            "max_new_tokens": 50,
            "stop": ["\n", "customer:", "Customer:", "?"],
            "temperature": 1.1,
            "top_k": 15,
            "top_p": 0.95,
            "return_full_text": False,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
        
