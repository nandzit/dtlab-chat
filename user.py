# Questo modulo implementa una semplice versione di un database per gli utenti in memoria.

import uuid
import bcrypt
from enum import Enum
from datetime import datetime

users = []
# Utenti sono memorizzati come dizionari.
# utente = {
#    'id': '123'
#    'name': 'giuseppe',
#    'surname': 'capasso',
#    'password': '123',
#    'email': 'giuseppe@test.com'
#    'created': '5-03-2024', 
# }

# Result è un'enumerazione. Serve a rendere più leggibile il codice. Ad esempio, 
# potrei far ritornare 2 quando un utente non viene trovato, ma questo sarebbe poco leggibile. 
# In python, le enumerazioni sono un particolare tipo di classe che ereditano da Enum.
class Result(Enum):
    OK = 1
    NOT_FOUND = 2 
    NOT_AUTHORIZED = 3
    DUPLICATED = 4

#Metodo di utilità per cercare un utente dato in ingresso l'email. Se non esiste viene ritornato None
def findUserByEmail(email: str) -> dict:
    for user in users:
        if user['email'] == email:
            return user
    return None

#Metodo di utilità per cercare un utente dato in ingresso un ID. Se non esiste viene ritornato None
def findUserByID(id: str) -> dict:
    try: 
      bID = uuid.UUID(id)
    except:
      return None
    for user in users:
        if user['id'] == bID:
            return user
    return None

# SaveUser memorizza un utente nel sistema dopo la procedura di signin degli utenti. 
# Prima controlla che non sia già registrato un utente con la stessa email, altrimenti ritorna un errore
# con la chiamata uuid.uuid4() si genera una stringa randomica che rappresenta l'ID dell'utente
# è fortemente sconsigliata la memorizzazione delle password degli utenti in chiaro, in quanto
# sarebbero accessibili da tutti. In questo caso utilizziamo il modulo bcrypt ("https://github.com/pyca/bcrypt/")
# Bcrypt fornisce due funzioni:
#   hashpw: che ritorna una versione "hashata" della password
#   chechpw: che effettua un confronto tra una password in chiaro e una hashata per vedere se corrispondono
# Alla fine viene creato un utente e inserito nella lista

def SaveUser(name: str, surname: str, email: str, password: str) -> (Result, dict):
    if findUserByEmail(email) is None:
        id = uuid.uuid4()
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        user = {
            'id': id,
            'name': name,
            'surname': surname,
            'email': email,
            'created': datetime.utcnow().isoformat(),
            'password': hashed
        }
        users.append(user.copy())
        user['password'] = ''
        return Result.OK, user
    else:
        return Result.DUPLICATED, None


# La funzione login controlla che esiste un utente con l'email inserita ed usa la funzione bcrypt.checkpw per controllare che la password sia corretta. 
def Login(email: str, password: str)-> (Result, dict):
    u = findUserByEmail(email)
    if u is not None and bcrypt.checkpw(password.encode('utf8'), u['password']):
        res = u.copy()
        res ['password'] = ''
        return Result.OK, res
    else:
        return Result.NOT_AUTHORIZED, None
