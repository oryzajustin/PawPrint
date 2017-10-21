from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods = ['GET', 'POST'])

def sms_reply():
    response = MessagingResponse()
    body = request.values.get('Body', None)
    
    if(body == 'Yes' or body == 'yes' or body == 'Y' or body == 'y'):
        response.message("Okay, great! Here's where your pet was last seen.")
        #TODO send information about pet, and remove client request from database
    elif(body == 'No' or body == 'no' or body == 'N' or body == 'n'):
        response.message("Oh no :( We'll keep looking for your pet!")
    else:
        response.message("Please enter either 'Y' or 'N'")
    
    return str(response)

if(__name__ == '__main__'):
    app.run()
