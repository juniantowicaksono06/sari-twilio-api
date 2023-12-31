from flask import Flask, render_template, jsonify, make_response, send_file, jsonify
from flask import request
 
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
 
from dotenv import load_dotenv
import os
import pprint as p
load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
api_key = os.environ['TWILIO_API_KEY_SID']
api_key_secret = os.environ['TWILIO_API_KEY_SECRET']
twiml_app_sid = os.environ['TWIML_APP_SID']
twilio_number = os.environ['TWILIO_NUMBER']

app = Flask(__name__)

def return_response(status_code = 200, message: str = None, data: dict or list = None, response_type = "json", filepath = None, attachment=True, preflight=False):
    if not preflight:
        if response_type == "json":
            obj = {
                "status_code": status_code
            }
            if data is not None:
                obj['data'] = data
            
            if message is not None:
                obj['message'] = message
                
            response = make_response(jsonify(obj))
            response.status_code = status_code
        elif response_type == 'file' and filepath is not None: 
            response = send_file(filepath, as_attachment=attachment)
    else:
        response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    return response

@app.route('/')
def home():
    return render_template(
        'home.html',
        title="In browser calls",
    )
@app.route('/sari_webview_call', methods=["GET", "OPTIONS"])
def call_webview():
    return render_template(
        'sari_webview.html',
        title="SARI WebView Call"
    )

@app.route('/token', methods=['GET', 'OPTIONS'])
def get_token():
    if request.method == 'OPTIONS':
        return return_response(preflight=True)
    identity = twilio_number
    outgoing_application_sid = twiml_app_sid

    access_token = AccessToken(account_sid, api_key,
                               api_key_secret, identity=identity)

    voice_grant = VoiceGrant(
        outgoing_application_sid=outgoing_application_sid,
        incoming_allow=True,
    )
    access_token.add_grant(voice_grant)
    response = return_response(200, data={'token': access_token.to_jwt(), 'identity': identity})
    # response = jsonify(
        # {'token': access_token.to_jwt(), 'identity': identity})

    return response

@app.route('/handle_calls', methods=['POST'])
def call():
    p.pprint(request.form)
    response = VoiceResponse()
    dial = Dial(callerId=twilio_number)

    if 'To' in request.form and request.form['To'] != twilio_number:
        print('outbound call')
        dial.number(request.form['To'])   
        response.append(dial)
        print(str(response))
        return str(response)
    else:
        print('incoming call')
        caller = request.form['Caller']
        dial = Dial(callerId=caller)
        dial.client(twilio_number)
    return ''

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)