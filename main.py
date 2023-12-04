from furhat_remote_api import FurhatRemoteAPI
from time import sleep
import random

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
    color("reset")
    return result

def say(message): # speaks to user
    color("blue")
    furhat.say(text = message, blocking=True)
    color("reset")


# Start a conversation
color("blue")
say('Hello, I am Mack, your virtual bartender. Blue light means im speaking, Green listening, Yellow Thinking and red means error. What can i help you with today?')

while True:

    result = listen()
    print(f'User: {result}')
    if "drink" in result:
        say('Would you like a drink?')
        result = listen()
        print(f'User: {result}')
        
        if "yes" in result or "yeah" in result or "sure" in result:
            say("Okay, what kind of drink would you like?")
            result = listen()
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
            say("Okay then, i will drink myself")
            sleep(1)
            say("would you like a drink now?")
            result = listen()
            print(result)
            if "no" in result or "nope" in result or "nah" in result:
                say("Okay then, would you like to quit?")
                result = listen()
                print(result)
                say("Okay, goodbye")
                break
    else:
        say("Huh? I am retarded, please say the word drink!")

    

