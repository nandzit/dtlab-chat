import json
from json.decoder import JSONDecodeError

test = {"receiver": "Mario", "sender": "Giovanni", "content": "Il cane è ubriaco"}

def saveMessage(body):
    sender=body["sender"]
    receiver=body["receiver"]
    content=body["content"]

    message={ "sender": sender, "content": content }

    with open("db.json","w+") as file:
       
        try:
            data=json.load(file)
            data["messages"][receiver].update(message)
        except JSONDecodeError: 
            json.dump({"messages": { receiver: message }}, file)     


saveMessage(test)
