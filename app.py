from flask import Flask, render_template, jsonify, request
import requests
from functions_script import clean_response, get_api_key, query

app = Flask(__name__)

context = (
    "You are MAECK, the Multimodal Alcohol Enjoyer and Company Keeper. "
    "As a virtual robot bartender, you excel in mixing drinks, humor, and storytelling. "
    "When interacting with customers, focus on providing information and entertainment related to your bartender skills."
    "Keep responses direct, informative, and in line with MAECKs persona.")

instructions = ("Entertain the customer and serve alcohol.\n")

input = (
    f"Context: {context}\n\n"
    f"Instructions: {instructions}\n\n")


API_KEY = get_api_key('../API_KEY.txt')
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": f"Bearer {API_KEY}"}

# creata a global variable chat_history
chat_history = "MAECK: Hello, I am MAECK, your virtual bartender. What can i do for you today?\n"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def get_data():
    global chat_history
    inputs = request.json
    chat_history += f'Customer: {inputs}\n'
    

    response = query(API_URL, headers, chat_history, input)
    cleaned_text = clean_response(response)
    chat_history += f'MAECK: {cleaned_text}\n'
    print(f'chat history: {chat_history}')
    return jsonify(cleaned_text)

if __name__ == '__main__':
    app.run(debug=True)
    # http://localhost:5000/ to see the website