import json
from json.decoder import JSONDecodeError
import pdb
import os.path
import os
from datetime import datetime

def saveMessage(body):
    message = body
    time = "{}".format(datetime.now())
    message["at"] = time
    
    if os.path.isfile('db.json'): 
        checkf = open("db.json")
    else:    
        os.system('touch db.json')

    with open("db.json","r+") as file:
        try:
            data=json.load(file)
            temp = data['messages']
            temp.append(message)
            file.seek(0)
            json.dump({"messages": temp}, file, indent=2)
            file.truncate()
        except JSONDecodeError: 
            file.seek(0)
            json.dump({'messages':[message]}, file, indent=2)    
            
def retrieveConversation (receiver, sender):
    try:
        messages = []
        with open("db.json", "r") as file:
            data=json.load(file)
            temp = data['messages']
            for message in temp:
                if message["receiver"] == receiver and message["sender"] == sender:
                    messages.append(message)
            messages.sort(key=lambda x: datetime.strptime(x['at'], '%Y-%m-%d %H:%M:%S.%f'))
            if len(messages) == 0:
                return None
            else: 
                return messages
    except:
        return None

