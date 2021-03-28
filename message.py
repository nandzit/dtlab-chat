import json
from json.decoder import JSONDecodeError
import pdb
import os.path
import os
from datetime import datetime

test = {"receiver": 'Mario', 'sender': 'Giovanni', 'content': 'Il cane è ubriaco'}


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
            
saveMessage(test)

def retrieveConversation (receiver, sender):
    try:
        messages = []
        with open("db.json", "r") as file:
            pdb.set_trace()
            data=json.load(file)
            temp = data['messages']
            for message in temp:
                if message["receiver"] == receiver and message["sender"] == sender:
                    messages.append(message)
                    print(messages) 
                    print(added)
            messages.sort(key=lambda x: datetime.datetime.strptime(x['at'], '%d/%m/%y %H:%M:%S'))
            return messages
    except:
        return None



print(retrieveConversation("Mario", "Giovanni"))
