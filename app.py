# app.py
from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = os.environ.get('OPENAI_API_KEY')

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form['user_message']
        bot_response = get_bot_response(user_message)
        return render_template('chat.html', messages=messages)
    else:
        return render_template('chat.html', messages=messages)

def get_bot_response(user_message):
    messages.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=1000
    )

    # Extract and print the assistant's reply
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return reply

if __name__ == '__main__':
    app.run(debug=True)
