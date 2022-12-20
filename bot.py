from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body' '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'quote' in incoming_msg:
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'joke' in incoming_msg:
        r = requests.get('https://icanhazdadjoke.com', headers={'accept': 'application/json'}) 
        if r.status_code == 200:
            data = r.json()
            joke = data['joke']
        else:
            joke = 'I could not retrieve a joke at this time, sorry.'
        msg.body(joke)
        responded = True
    if 'cat' in incoming_msg:
        msg.media('https://cataas.com/cat')
        responded = True
    if 'dog' in incoming_msg:
        r = requests.get('https://dog.ceo/api/breeds/image/random', headers={'accept': 'application/json'}) 
        if r.status_code == 200:
            data = r.json()
            dog_url = data['message']
            msg.media(dog_url)
        else:
            dog = 'I could not retrieve a dog at this time, sorry.'
            msg.body(dog)
        responded = True
    if not responded:
        msg.body('I only know about famous quotes, cats, dogs, and joke, sorry!')

    return str(resp)

if __name__ == '__main__':
    app.run(port=4000)
