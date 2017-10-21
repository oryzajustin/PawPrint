from twilio.rest import Client, TwilioRestClient
from credentials import account_sid, auth_token, my_number, twilio_number


def sendsms(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to = my_number,
                                     from_= twilio_number,
                                     body= message)

if(__name__ == '__main__'):
    message = "This is a test message from the twilio number"
    sendsms(message)
