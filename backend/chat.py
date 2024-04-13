from flask import Flask, request
from flask_cors import CORS
from ai_functions import *
from telethon.sync import TelegramClient

api_id = 0
api_hash = ''
client = TelegramClient('@abcd', api_id, api_hash)

app = Flask(__name__)
CORS(app)

database = {
    "chat_1":{
        "name": "Ryan Gosling",
        "messages": [
            {"user": "Ryan Gosling", "message": "Hello! I am real Ryan Gosling. Thanks for stopping by. So, what's on your mind? Life can be pretty unpredictable, just like a script that takes unexpected turns. But hey, that's what makes it interesting, right? Anyway, let's chat. What do you want to talk about?"},
            {"user":"Me","message":"ok"},
            {"user":"Me","message":"Same here. Any exciting plans for the weekend?"},
            {"user":"Ryan Gosling","message":"Hello! I am real Ryan Gosling. Thanks for stopping by. So, what's on your mind? Life can be pretty unpredictable, just like a script that takes unexpected turns. But hey, that's what makes it interesting, right? Anyway, let's chat. What do you want to talk about?"}
        ]
    },
    "chat_2":{
        "name": "Margo Robbie",
        "messages": [
            {"user":"Margo Robbie", "message": "Hey there! It's Margo Robbie here, just a quick note to say you're amazing just as you are! Keep shining bright!"},
            {"user":"Me","message":"ok"},
            {"user":"Me","message":"Same here. Any exciting plans for the weekend?"},
            {"user":"Margo Robbie","message":"Hey there! It's Margo Robbie here, just a quick note to say you're amazing just as you are! Keep shining bright!"}
        ]
    }
}

@app.route("/chats", methods = ["GET"])
def get_all_chats():
    chats = []
    for dialog in client.iter_dialogs():
        chats.append({"chat_id": dialog.id,"user":dialog.name})
    return chats

@app.route("/messages/<chat_id>", methods = ["GET"])
def get_all_messages_from_chats(chat_id):
    return database[chat_id].get("messages")

@app.route("/suggestions/<chat_id>", methods = ["GET"])
def get_all_suggestions(chat_id):
    messages = database[chat_id].get("messages")
    return generate_chat_suggestion(messages)

@app.route("/message", methods = ["POST"])
def post_message():
    chat_id: str = request.form["chat_id"]
    name: str = request.form["name"]
    message: str = request.form["message"]
    messages = database[chat_id].get("messages")
    messages.append({"user":name,"message":message})

    return "Message was added"



    