import json
import random


result = "whine"

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
    
value = what_drink(result)
print(value)