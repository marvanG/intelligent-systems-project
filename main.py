from furhat_remote_api import FurhatRemoteAPI
from time import sleep
import random

# Instantiate FurhatRemoteApi
furhat = FurhatRemoteAPI('localhost')

# get voices
voices = furhat.get_voices()

# set robot voice
furhat.set_voice(name='Isabelle-Neural')

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

# Start a conversation
color("blue")
furhat.say(text = 'Hello, I am Mack, your virtual bartender. How are you today?', blocking=True)
while True:

    color("green")
    result = furhat.listen()
    print(f'User said: {result.message}')
    print(result)
    
    break

    

