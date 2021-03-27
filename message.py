import json
from json.decoder import JSONDecodeError
import pdb
import os.path
import os

test = {"receiver": 'Mario', 'sender': 'Giovanni', 'content': 'Il cane è ubriaco'}

def saveMessage(body):

    if os.path.isfile('db.json'): 
        checkf = open("db.json")
    else:    
        os.system('touch db.json')

    with open("db.json","r+") as file:
        try:
            data=json.load(file)
            temp = data['messages']
            temp.append(body)
            file.seek(0)
            json.dump({"messages": temp}, file, indent=2)
            file.truncate()
        except JSONDecodeError: 
            file.seek(0)
            json.dump({'messages':[ body]}, file, indent=2)    
            
saveMessage(test)



#Retrieve message 
#Retrieve all the messages that has retrieve id and sender id passed as parameters

    
