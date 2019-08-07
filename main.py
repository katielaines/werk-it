from flask import Flask
from flask import request, Response, jsonify
from werkzeug.datastructures import ImmutableMultiDict
import json
import requests
import random
import re

app = Flask(__name__)
userlist = []

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/addme', methods=['POST'])
def addme():
    username = request.data.decode()['user_id']
    userlist.append(username)
    return Response()


@app.route('/select', methods=['POST'])
def select():
    data = ImmutableMultiDict(request.form).to_dict()
    print('---------ENTERED SELECT-------------')
    print(json.dumps(data))
    channel = data.get('channel_id')
    print(channel)
    # channel = 'CLTN9FWJK'
    token = 'xoxp-401097423840-401121670704-719274018822-79240cb58c50405036901b9de95006ac'
    url = 'https://slack.com/api/channels.info'
    params = {
        'channel': channel,
        'token': token
    }
    print(params)
    r = requests.get(url=url, params=params)
    resp = json.loads(r.text)
    print(resp)
    chl = resp.get('channel')
    print(chl)
    users = chl.get('members')
    print(users)
    selection = users[random.randint(0, len(users)-1)]
    print(selection)
    phrases = [
        'Today I choose...<@%u>',
        'Hmm.. better make it..<@%u>',
        'I would love for <@%u> to select a pose!',
        '<@%u> is a poser! :laughing:',
        '<@%u> volunteers as tribute!',
        'Show us what you got, <@%u>!',
        'Hey, <@%u>! Strike a pose!',
        'Today\'s victim is... <@%u>!'
    ]
    phrase = phrases[random.randint(0, len(phrases)-1)]
    return jsonify(
        response_type='in_channel',
        text=re.sub('%u', selection, phrase),
    )


if __name__ == '__main__':
    app.run(debug=True)
