import requests
import random
import string
from flask import Flask, render_template, request, jsonify
import json
import boto3

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', aws_access_key_id='ASIA4N2NY7ZRD5EZA6FA', aws_secret_access_key='Vf95aLRU4wWSJ888vGuYthDCMRBMPIDTjH4TDUEL')
table = dynamodb.Table('fantastic-bear-veilCyclicDB')

def get_uuid():
    response = requests.get("https://www.uuidgenerator.net/api/version4")
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

def gen_id():
    alphabet = string.ascii_lowercase
    digits = string.digits

    id_format = random.choices(string.ascii_uppercase, k=2) + random.choices(string.ascii_lowercase, k=2) + random.choice(string.ascii_uppercase) + random.choices(string.ascii_lowercase, k=2) + random.choice(string.digits)
    
    custom_id = ''.join(random.sample(id_format, len(id_format)))
    return custom_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        txt = request.form['text']
        mode = request.form['mode']
        uuid_1 = request.form['uuid']
        id_1 = request.form['id']
        id = gen_id() if id_1 == None else id_1
        uuid = get_uuid() if uuid_1 == None else uuid_1
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
            'id': '6clrFCv',
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
            
            # Store data in DynamoDB table
            response_dynamodb = table.put_item(
                Item={
                    'id': id,
                    'uuid': uuid,
                    'web_mode': int(webk),
                    'result': result
                }
            )

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
