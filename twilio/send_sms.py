from twilio.rest import Client, TwilioRestClient
from credentials import account_sid, auth_token, my_number, twilio_number


def sendsms(message):
    client = Client(account_sid, auth_token)
    client.messages.create(to = my_number,
                   					 from_= twilio_number,
                                     body= message,
                                     media_url = "https://i.ytimg.com/vi/nomNd-1zBl8/maxresdefault.jpg")

if(__name__ == '__main__'):
    message = "We may have found your pet."
    sendsms(message)
