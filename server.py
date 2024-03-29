import requests
import random
import string
from flask import Flask, render_template, request, jsonify
import json
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://testai_fartiredso:cd7e4c051ff05bb1216d9cb6372e1d5e2e5974ec@rxe.h.filess.io:27018/testai_fartiredso')
db = client['testai_fartiredso']
collection = db['chat']

def get_uuid():
    response = requests.get("https://www.uuidgenerator.net/api/version4")
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

def gen_id():
    id_format = ''.join(random.choices(string.ascii_uppercase, k=2)) + \
                ''.join(random.choices(string.ascii_lowercase, k=2)) + \
                random.choice(string.ascii_uppercase) + \
                ''.join(random.choices(string.ascii_lowercase, k=2)) + \
                random.choice(string.digits)

    custom_id = ''.join(random.sample(id_format, len(id_format)))
    return custom_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        txt = request.form.get('text')
        mode = request.form.get('mode')
        uuid_1 = request.form.get('uuid')
        id_1 = request.form.get('id')
        id = gen_id() if id_1 is None else id_1
        uuid = get_uuid() if uuid_1 is None else uuid_1
        webk = True if mode == '1' else False

        url = 'https://www.blackbox.ai/api/chat'

        data = {
            'messages': [
                {
                    'id': id,
                    'content': txt,
                    'role': 'user'
                }
            ],
            'id': id,
            'previewToken': None,
            'userId': uuid,
            'codeModelMode': True,
            'agentMode': [],
            'trendingAgentMode': [],
            'isMicMode': False,
            'isChromeExt': False,
            'githubToken': None,
            'webSearchMode': webk,
            'maxTokens': "10240"
        }

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            result = response.text
            
            # Store data in MongoDB
            collection.insert_one({'id': id, 'uuid': uuid, 'web_mode': int(webk), 'result': result})

            return jsonify({
                'id': id,
                'uuid': uuid,
                'web': webk,
                'Creator': "@ExploitNeT - @ImSoheilOfficial",
                'data': result
            })
        else:
            return jsonify({'status': False, 'error': response.text})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
