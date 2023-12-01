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

furhat.say(text = 'Hello, I am Furhat, your virtual robot. How are you today?', blocking=True)