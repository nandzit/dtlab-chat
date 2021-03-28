# Questo modulo utilizza Flask per realizzare un web server. L'applicazione può essere eseguita in vari modi
# FLASK_APP=server.py FLASK_ENV=development flask run
# python server.py se aggiungiamo a questo file app.run()

from flask import Flask, request
import user
import message

# viene creata l'applicazione con il nome del modulo corrente.
app = Flask(__name__)

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
    email = data['email']
    password = data['password']
    
    result, u = user.SaveUser(name, surname, email, password)

    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return u, 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    result, u = user.Login(email, password)

    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return u, 201

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id: str):
    email = request.authorization.username
    password = request.authorization.password

    print(email, password)

    result, u = user.Login(email, password)

    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return 'Utente Cancellato', user.deleteUser(id)


@app.route('/inbox', methods=['POST'])
def sendMessage():
    data = request.get_json()
    mittente = data['mittente']
    destinatario = data['destinatario']
    messaggio = data['messaggio']

    uMittente = user.findUserByEmail(mittente)
    uDestinatario = user.findUserByEmail(destinatario)
    if (uMittente is not None) and (uDestinatario is not None):
        message.saveMessage(uMittente['id'], uDestinatario['id'], messaggio)
        return 'Messaggio creato', 201
    else:
        return '', user.Result.NOT_FOUND

@app.route('/inbox/<id>', methods=['GET'])
def getMessages(id: str):

    if(user.findUserByID(id)):
        messages = message.getMessages(id)
        if(messages is not None):
            return '', user.Result.OK
        else:
            return "Casella vuota", user.Result.NOT_FOUND
    else:
        return 'Utente non trovato', user.Result.NOT_FOUND

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
