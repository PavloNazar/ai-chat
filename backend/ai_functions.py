from openai import OpenAI
import re

client = OpenAI()

def generate_chat_suggestion(chat: []) -> list[str]:
    messages = ""
    for i in range(len(chat)):    
        messages += chat[i]['user'] + ":"+ chat[i]['message'] + "\n"
    prompt = "Based on this conversation -> \n"+messages+". Create 3 different responses (only my answers),how i can continue this conversation."

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
            
        ],
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    suggestions = []
    for line in response.splitlines():
        lines = re.split("me:", line, flags=re.IGNORECASE)
        if lines[len(lines)-1].strip() != "":
            suggestions.append(lines[len(lines)-1])
        
    print(suggestions)
    return suggestions






# func(chat) -> list[str] // ["Hello!", "Hey hey!", "bob!"]