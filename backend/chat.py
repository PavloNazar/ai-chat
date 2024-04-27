from flask import Flask, request
from flask_cors import CORS
from ai_functions import *
from telethon.sync import TelegramClient
from telethon.types import PeerUser, MessageService


api_id = 0
api_hash = ''
client = TelegramClient('@abc', api_id, api_hash)

app = Flask(__name__)
CORS(app)

# Enable CORS for all routes
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response


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
async def get_all_chats():
    await client.connect()
    chats = []
    async for dialog in client.iter_dialogs():
        chats.append({"chat_id": dialog.id,"user":dialog.name})
    return chats

@app.route("/messages/<chat_id>", methods = ["GET"])
async def get_all_messages_from_chats(chat_id):
    chat_id = int(chat_id)
    await client.connect()
    messages = []
    async for message in client.iter_messages(chat_id):
        if isinstance(message, MessageService):
            continue
        user = None
        if message.from_id is None:
            user = message.peer_id
        else:
            user = message.from_id
        my_user = await client.get_entity(user)
        print(my_user.first_name, message.message)
        
        messages.append(str(message))
    return messages

       

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


# passauit
# async def main():
#     app.run(debug=True)

if __name__ == "__main__":
    client.loop.run_until_complete(app.run(debug=True))