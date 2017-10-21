from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods = ['GET', 'POST'])

def sms_reply():
    response = MessagingResponse()
    body = request.values.get('Body', None)
    
    if(body == 'Hi' or body == 'hi'):
        response.message("Hi, what can I do for you?")
    elif(body == 'Bye' or body == 'bye'):
        response.message("Goodbye!")
    else:
        response.message("I am not a bot, these responses are hard coded.")
    
    return str(response)

if(__name__ == '__main__'):
    app.run()
