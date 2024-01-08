from furhat_remote_api import FurhatRemoteAPI
from time import sleep
from functions_script import *
from multiprocessing import Process, Manager
import warnings


chat_history = ""

def AI_bot_response(inputs):
        global chat_history
        chat_history += f'Customer: {inputs}\n'
        
        response = query(API_URL, headers, chat_history, input)
        cleaned_text = clean_response(response)
        chat_history += f'MAECK: {cleaned_text}\n'
        print(f'chat history: {chat_history}')
        return cleaned_text

if __name__ == '__main__': 
    warnings.filterwarnings('ignore')
    # Instantiate FurhatRemoteApi
    furhat = FurhatRemoteAPI('localhost')
    # get voices
    voices = furhat.get_voices()
    # set robot voice
    furhat.set_voice(name='Matthew')

    manager = Manager()
    emotion = manager.list([''])

    procs = []
    proc = Process(target=getEmotions, args=(emotion,))  # instantiating without any argument
    procs.append(proc)
    proc.start()
    sleep(10) #emotion detector takes some time to boot :/

    # AI part
    API_PATH = "../API_KEY.txt" # Path to your API key (create a free account on huggingface.co and generate a key)
    API_KEY = "Bearer " + get_api_key(API_PATH)
    print(API_KEY)


    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {"Authorization": API_KEY}


    context = (
        "You are MAECK, the Multimodal Alcohol Enjoyer and Company Keeper. "
        "As a virtual robot bartender, you excel in mixing drinks, humor, and storytelling. "
        "When interacting with customers, focus on providing information and entertainment related to your bartender skills."
        "Keep responses direct, informative, and in line with MAECKs persona.")

    instructions = ("Entertain the customer and serve alcohol.\n")

    input = (
        f"Context: {context}\n\n"
        f"Instructions: {instructions}\n\n")

    # creata a global variable chat_history
    chat_history = "MAECK: Hello, I am MAECK, your virtual bartender. What can i do for you today?\n"

    # Start a conversation
   
    say('Hello, I am MAECK, your virtual bartender. What can i do for you today?')


    while True:
        user_input = listen()    
        print(f'User: {user_input}')

        if (user_input.strip().lower() == "break" or user_input.strip().lower() == "quit" or user_input.strip().lower() == "exit" or user_input.strip().lower() == "stop"):
            say("Okay then have a nice day, goodbye!")
            break
        if user_input.strip() != "":
            print(f'User Emotion: {emotion[0]}')

            if emotion[0] == "sad":
                sad_answer = sad_costumer()
                chat_history += f'MAECK: {sad_answer}\n'
                say(sad_answer)
                sleep(1)
            elif emotion[0] == "angry":
                angry_answer= angry_costumer()
                chat_history += f'MAECK: {angry_answer}\n'
                say(angry_answer)
                sleep(1)
            elif emotion[0] =="surprise":
                surprised_answer = surprised_costumer()
                chat_history += f'MAECK: {surprised_answer}\n'
                say(surprised_answer)
                sleep(1)
            elif emotion[0] == "disgust":
                disgusted_answer = disgusted_costumer()
                chat_history += f'MAECK: {disgusted_answer}\n'
                say(disgusted_answer)
                sleep(1)
            elif emotion[0] == "fear":
                fear_answer = fear_costumer()
                chat_history += f'MAECK: {fear_answer}\n'
                say(fear_answer)
                sleep(1)
            elif emotion[0] == "happy":
                happy_answer = happy_costumer()
                chat_history += f'MAECK: {happy_answer}\n'
                say(happy_answer)
                sleep(1)

            else:
                response = AI_bot_response(user_input)
                say(response)
            

    for proc in procs:
            proc.join()


              






