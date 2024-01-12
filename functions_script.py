from furhat_remote_api import FurhatRemoteAPI
import json
import random
from sympy import false
import requests
from EmotionDetector import EmotionDetector
import cv2
import opencv_jupyter_ui as jcv2
from ActionUnitDetector import ActionUnitDetector
import warnings
import time

import os


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



def no(): #Answers no in random words
    with open('facts.json','r') as file:
        data = json.load(file)

    random_no_answer = random.choice(list(data['say_no'].values()))
    return random_no_answer



def what_drink(result): #Random selection of drinks
    with open('facts.json','r') as file:
        data=json.load(file)
   
    
    drinks_list = list(data['available_drinks'].values())
    # print(drinks_list)

    matching_drinks = [drink for drink in drinks_list if drink.lower() in result]
    # print(matching_drinks)
    
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


#Reactions for different emotions

def sad_costumer():
    with open('facts.json','r') as file:
        data =json.load(file)
    sad_reaction = random.choice(list(data["sad_costumer"].values()))
    return sad_reaction
    

def angry_costumer():
    with open('facts.json','r') as file:
        data =json.load(file)
    angry_reaction = random.choice(list(data["angry_costumer"].values()))
    return angry_reaction

def surprised_costumer():
    with open('facts.json','r') as file:
        data =json.load(file)
    surprised_reaction = random.choice(list(data["surprised_costumer"].values()))
    return surprised_reaction

def disgusted_costumer():
    with open('facts.json','r') as file:
        data =json.load(file)
    disgusted_reaction = random.choice(list(data["disgusted_costumer"].values()))
    return disgusted_reaction

def fear_costumer():
    with open('facts.json','r') as file:
        data =json.load(file)
    fear_reaction = random.choice(list(data["fear_costumer"].values()))
    return fear_reaction

def happy_costumer():
    with open('facts.json','r') as file:
      data =json.load(file)
    happy_reaction = random.choice(list(data["happy_costumer"].values()))
    return happy_reaction



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
            "max_new_tokens": 70,
            "stop": ["\n", "customer:", "Customer:", "?"],
            "temperature": 1,
            "top_k": 20,
            "top_p": 0.97,
            "return_full_text": False,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
   
    

# emotion detection functions

def getEmotions(emotion):
    warnings.filterwarnings('ignore')
    emotionDetector = EmotionDetector('DiffusionFER/DiffusionEmotion_S/dataset_sheet.csv')
    cam = cv2.VideoCapture(0)
    rec = True
    auDetector = ActionUnitDetector()
    starttime = time.monotonic()
    count = 0
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                raise ("OpenCV found an error reading the next frame.")

            (h, w, c) = frame.shape
            display = frame
            #print(time.monotonic() - starttime)
            
            if rec:
                cv2.circle(display, (40, 40), 10, (0, 0, 255), 6)
                if (time.monotonic() - starttime) > 2.0:
                    starttime = time.monotonic()
                    aus,faces = auDetector.detectAUImage(frame)
                    emotion[0] = emotionDetector.predict(aus)
                    count += 1
                if count > 0:
                    #try:
                    for face in faces:
                        x1 = int(face[0][0])
                        x2 = int(face[0][2])
                        y1 = int(face[0][1])
                        y2 = int(face[0][3])
                        cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 6)
                        cv2.putText(display, emotion[0], (x1 + 20, y1 - 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    #except (UnboundLocalError) as e:
                           #pass #wait another iteration
                        

            cv2.putText(display, "Press SPACE to toggle between recording and stopped", ((w) // 3, (8 * h) // 10),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            cv2.putText(display, "Press ESC to exit", ((w) // 3, (9 * h) // 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),
                        2)

            jcv2.imshow("snap", display)

            key = jcv2.waitKey(1) & 0xFF
            if key == 27:  # ESC to exit
                break
            elif key == 32:  # SPACE to take snap
                rec = not rec

    finally:
        cam.release()
        jcv2.destroyAllWindows()
        
