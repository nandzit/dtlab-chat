from user import Result
import uuid
from datetime import datetime

messages = {"aaaaaaaaaaaa": ["vincenzo", "ciao ciao"]}

def saveMessage(mittente: str, destinatario: str, messaggio: str):
    now = datetime.now()

    current_time = now.strftime("%D:%H:%M:%S")
    if (mittente not in messages):
        messages[mittente] = []
    if(destinatario not in messages):
        messages[destinatario] = []

    test = [mittente, messaggio, current_time]
    print("Aggiunto", test)

    messages[destinatario].append(test)

    print("Messaggi totalI:", messages[destinatario])
    return

def getMessages(destinatario: str):
    idDestinatario = uuid.UUID(destinatario)
    return messages[idDestinatario]
