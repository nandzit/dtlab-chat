# Questo modulo utilizza Flask per realizzare un web server. L'applicazione può essere eseguita in vari modi
# FLASK_APP=server.py FLASK_ENV=development flask run
# python server.py se aggiungiamo a questo file app.run()

from flask import Flask, request
import user
from enum import Enum
import message
import jwt
import pdb
# viene creata l'applicazione con il nome del modulo corrente.
app = Flask(__name__)

class Result(Enum):
    OK = 1
    NOT_FOUND = 2
    NOT_AUTHORIZED = 3
    DUPLICATED = 4


#Never save the private key in your code, but in this case is "Carino"
private_key = "gaiaiswatchingyou"

# getErrorCode è una funzione di utilità che mappa i valori ritornati dal modulo user con quelli del
# protocollo HTTP in caso di errore. 
# 404 - Not Found: una risorsa non è stata trovata sul server;
# 403 - Forbidden: accesso negato;
# 409 - Conflict: è violato un vincolo di unicità. Ad esempio, esiste già un utente con la stessa mail registrata;
# Come ultima spiaggia è buona norma ritornare "500 - Internal Server Error" per indicare che qualcosa è andato storto
def getErrorCode(result: user.Result)->int:
    if result is user.Result.NOT_FOUND:
        code = 404
    elif result is user.Result.NOT_AUTHORIZED:
        code = 403
    elif result is user.Result.DUPLICATED:
        code = 409
    else:
        code = 500

    return code

@app.route('/user', methods=['POST'])
def createUser():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    email = data['mail']
    password = data['password']
    
    result, u = user.SaveUser(name, surname, email, password)
    
    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return u, 201

@app.route('/user/find', methods=['GET'])
def findUser ():
    data = request.get_json()
    credential = request.args.get('cred')
    #Auth here 
    u = user.findUserByEmail(credential)
    #Check response
    #First email than password
    if u is None:
          u = user.findUserByID(credential)
          if u is None:
                code = 404 
                return 'User not found', code
          else:
                return 'User {0}{1} found'.format(u["name"], u["surname"]), 201
    else:
        return 'User {0}{1} found'.format(u["name"], u["surname"]), 201

    
@app.route('/user/login', methods=["POST"])
def login ():   
    data = request.get_json()
    email = data['email']
    password  = data['password']
    result, u = user.Login(email,password)
    if result is not user.Result.OK:
        code = getErrorCode(result)
        return "Sorry we don't know you", code
    else:
        try:
            pdb.set_trace()
            credentials = {"email": u["email"], "password":u["password"]}
            encoded_jwt = jwt.encode(credentials, private_key, algorithm="HS256")
            return encoded_jwt, 200
        except:
            return "An error occurred", 500

@app.route('/user/delete', methods=["DELETE"])
def deleteUser():
    data = request.get_json()
    user_id = request.args.get('id')
    result = user.DeleteUser(user_id)

    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return '', 200

@app.route('/user/create_message', methods=["POST"])
def createMessage():
    data = request.get_json()
    user = Auth()
    #Insert Authorization
    try: 
        receiverEmail = data["receiver"]
        receiver = findUserByEmail(receiver)
        if receiver is None: 
            return "Receiver not found", 404
        else:
            senderID = user["id"]
            receiverID = receiver["id"]
            content = data["content"]
            text = {'receiver': receiverID, 'sender': senderID, 'content': content}
            message.saveMessage(text)
            return "Message sent successfully", 201
    except:
        return 'Something went wrong, check your fields', 500

@app.route('/user/inbox', methods=["GET"]) 
def retrieveConversation():
    data = request.get_json()
    user = Auth()
    #Get mail from sender and receiver
    receiverEmail = data.args.get('receiver')
    receiver = user.findUserByEmail(receiverEmail)
    if receiver is not None:
        receiver_id = receiver["id"]
        sender_id = user["id"]
        try: 
          message = message.retrieveConversation(receiverEmail, senderEmail)
          if message is None:
              return "Conversation is Empty", 200
          else: 
              return message, 200
        except: 
            return "A problem occured during creation"
    else:    
       return "User not Found", 404


if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
