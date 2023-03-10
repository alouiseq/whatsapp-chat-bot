from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

failed_msg = 'Oh no! I can\'t find a {} for you at this time.'
no_data_msg = 'Whoops, I seem to be missing that data! Ask me about famous quotes, jokes, cats, dogs, and memes instead!'

def getJsonData(req_url, headers={'accept': 'application/json'}, params={}):
    r = requests.get(req_url, headers=headers, params=params)
    if r.status_code == 200:
        return r.json()

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body' '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    searched = False

    if 'quote' in incoming_msg:
        data = getJsonData('https://api.quotable.io/random')
        if data:
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = failed_msg.format('quote')

        msg.body(quote)
        searched = True
    if 'joke' in incoming_msg:
        data = getJsonData('https://icanhazdadjoke.com')
        if data:
            joke = data['joke']
        else:
            joke = failed_msg.format('joke')
        msg.body(joke)
        searched = True
    if 'cat' in incoming_msg:
        msg.media('https://cataas.com/cat')
        searched = True
    if 'dog' in incoming_msg:
        breed = None
        data = getJsonData('https://dog.ceo/api/breeds/list/all')
        if data:
            breeds = list(data['message'].keys())

        for b in breeds:
            if b in incoming_msg:
                breed = b;
                break

        if breed:
            data = getJsonData(f'https://dog.ceo/api/breed/{breed}/images/random')
        else:
            data = getJsonData('https://dog.ceo/api/breeds/image/random')

        if data:
            dog_url = data['message']
            msg.media(dog_url)
        else:
            dog = failed_msg.format('dog')
            msg.body(dog)

        searched = True
    if 'meme' in incoming_msg:
        keywords = incoming_msg.replace(' ', ',').replace(',meme', '').replace('meme,', '')
        url = "https://humor-jokes-and-memes.p.rapidapi.com/memes/random"
        querystring = {"keywords":f"{keywords}","number":"3","media-type":"image","keywords-in-image":"false","min-rating":"4"}
        headers = {
            "X-RapidAPI-Key": "d16b6e4142mshfff4f1f121ab449p1088cajsnfabf9adc12f5",
            "X-RapidAPI-Host": "humor-jokes-and-memes.p.rapidapi.com"
        }

        data = getJsonData(url, headers, querystring)

        if data:
            msg.media(data['url'])
        else:
            msg.body(failed_msg.format('meme'))
        searched = True
    if not searched:
        msg.body(no_data_msg)

    return str(resp)

if __name__ == '__main__':
    app.run(port=4000)
