from furhat_remote_api import FurhatRemoteAPI
from time import sleep
import random
from functions_script import color, listen, say,yes,no,what_drink,no_answer
from functions_script import color, listen, say, clean_response, get_api_key, query, getEmotions
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
    # get users (how does this work?)
    users = furhat.get_users()
    print(f'\nUsers: {users}')
    furhat.attend(user = 'CLOSEST')

    manager = Manager()
    emotion = manager.list([''])

    procs = []
    proc = Process(target=getEmotions, args=(emotion,))  # instantiating without any argument
    procs.append(proc)
    proc.start()
    sleep(10) #emotion detector takes some time to boot :/

    # AI part

    API_PATH = ".../API_KEY.txt" # Path to your API key (create a free account on huggingface.co and generate a key)
    with open(API_PATH, 'r') as file:
        API_KEY = "Bearer " +file.read().strip()
    API_PATH = "../API_KEY.txt" # Path to your API key (create a free account on huggingface.co and generate a key)
    #API_KEY = "Bearer " + get_api_key(API_PATH)
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
    color("blue")

    #say('Hello, I am Mack, your virtual bartender. Blue light means im speaking, Green listening, Yellow Thinking and red means error. What can i help you with today?')
    """
    while True:
        
        result = listen()
        print(f'User: {result}')
        if "drink" in result or "could" in result or "have" in result:
            
            yes_answer = yes()
            say(yes_answer)
            sleep(1)
            say('What would you like?')
            result = listen()
            print(f'User: {result}')
            
            if "yes" in result or "yeah" in result or "sure" in result or "ye" in result:

                say("Okay, what kind of drink would you like?")
                result = listen()
                result = what_drink(result)

                print(f'User: {result}') 

                say("Okay, I will make you a " + result)
                color("yellow")
                furhat.gesture(name = "Nod")
                sleep(1)
                color("reset")
                say("Here is your " + result) 
                say("Enjoy!")
                sleep(1)
                say("Would you like another drink?")
                
            else:
                non_answer = no_answer()
                say(non_answer)
                #say("Okay then, i will drink myself")
                sleep(1)
                say("would you like something else?")
                result = listen()
                print(result)
                if "no" in result or "nope" in result or "nah" in result:
                    say("Okay then, would you like to quit?")
                    result = listen()
                    print(result)
                    say("Okay, goodbye")
                    break
        else:
            say("Huh?")
    """

    say('Hello, I am MAECK, your virtual bartender. What can i do for you today?')

    k=0
    while k< 20:
        k+=1
        user_input = listen()    
        print(f'User: {user_input}')
        if (user_input.strip().lower() == "break" or user_input.strip().lower() == "quit" or user_input.strip().lower() == "exit" or user_input.strip().lower() == "bye"):
                say("Okay then have a nice day, goodbye!")
                break
        elif user_input.strip() != "":
            response = AI_bot_response(user_input)
            say(response)
        print(emotion[0])

    for proc in procs:
            proc.join()

    # while True:
        
    #     result = listen()
    #     print(f'User: {result}')
    #     if "drink" in result:
    #         say('Would you like a drink?')
    #         result = listen()
    #         print(f'User: {result}')
            
    #         if "yes" in result or "yeah" in result or "sure" in result:
    #             say("Okay, what kind of drink would you like?")
    #             result = listen()
    #             print(f'User: {result}')

    #             say("Okay, I will make you a " + result)
    #             color("yellow")
    #             furhat.gesture(name = "Nod")
    #             sleep(1)
    #             color("reset")
    #             say("Here is your " + result)
    #             say("Enjoy!")
    #             sleep(1)
    #             say("Would you like another drink?")
                
    #         else:
    #             say("Okay then, i will drink myself")
    #             sleep(1)
    #             say("would you like a drink now?")
    #             result = listen()
    #             print(result)
    #             if "no" in result or "nope" in result or "nah" in result:
    #                 say("Okay then, would you like to quit?")
    #                 result = listen()
    #                 print(result)
    #                 say("Okay, goodbye")
    #                 break
    #     else:
    #         say("Huh? I am retarded, please say the word drink!")


    

