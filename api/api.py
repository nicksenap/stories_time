from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/request_transcription', methods=['POST'])
def request_transcription():
    return jsonify(request.json)


app.run()
