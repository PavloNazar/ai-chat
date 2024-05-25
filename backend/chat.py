from quart import Quart, request
from quart_cors import cors
from ai_functions import *
from telethon.sync import TelegramClient
from telethon.types import PeerUser, MessageService
from telethon.types import InputMessagesFilterChatPhotos
from dotenv import load_dotenv
import os


load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
client = TelegramClient(os.getenv("TELE_NAME"), api_id, api_hash)

app = Quart(__name__)
app = cors(app, allow_origin="*")

# Enable CORS for all routes
# @app.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
#     return response


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

async def get_messages_by_chat_id(chat_id):
    await client.connect()
    messages = []
    async for message in client.iter_messages(chat_id, limit=40):
        first_name = "Me"
        if isinstance(message, MessageService):
            continue
        user = None
        if message.from_id is None:
            user = message.peer_id
        else:
            user = message.from_id
        my_user = await client.get_entity(user)
        
        
        # messages.append(str(message))
        if message.message == "":
            continue
        if message.from_id is None:
            first_name = my_user.first_name
        messages.append({"user":first_name, "message":message.message})
    messages.reverse()
    return messages

@app.route("/chats", methods = ["GET"])
async def get_all_chats():
    async with client:
        # await client.connect()
        chats = []
        async for dialog in client.iter_dialogs():
            if dialog.is_user == True:
                chats.append({"chat_id": dialog.id,"user":dialog.name})
        # await client.disconnect()
        return chats

@app.route("/messages/<chat_id>", methods = ["GET"])
async def get_all_messages_from_chats(chat_id):
    
    chat_id = int(chat_id)
    messages = await get_messages_by_chat_id(chat_id)
    
    return messages

       

@app.route("/suggestions/<chat_id>", methods = ["GET"])
async def get_all_suggestions(chat_id):
    chat_id = int(chat_id)
    messages = await get_messages_by_chat_id(chat_id)
    return generate_chat_suggestion(messages)

@app.route("/message", methods = ["POST"])
async def post_message():
    await client.connect()
    chat_id: int = int((await request.form)["chat_id"])
    # name: str = (await request.form)["name"]
    message: str = (await request.form)["message"]
    await client.send_message(chat_id, message)
    

    return "Message was added"


# passauit
# async def main():
#     app.run(debug=True)

if __name__ == "__main__":
    client.loop.run_until_complete(app.run(debug=True))