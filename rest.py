#!flask/bin/python
import os
import tempfile

from language_processor import LanguageProcessor
from file_response import FileResponse

from flask import Flask, Response, request, send_file, render_template, send_from_directory
from flask_cors import CORS

from text_response import TextResponse

UPLOAD_FOLDER = './temp'
TIKA_SERVER = 'http://localhost'
TIKA_PORT = '8085'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def to_json_array(list):
    results = '['
    first = True
    for item in list:
        if not first:
            results = results + ','
        results = results + item.toJSON()
        first = False
    results = results + ']'
    return results

# Route to serve static resources
@app.route('/resources/<path:path>')
def send_resources(path):
    return send_from_directory('resources', path)

# The home page route
@app.route("/")
def hello_world(name=None):
    return render_template('index.html', tika_server=TIKA_SERVER + ':' + TIKA_PORT)

@app.route('/api/v1.0/data/sanitize', methods=['POST'])
def get_sanitized_text():
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    tr = TextResponse(lp.tokens_to_string(lp.remove_stops()))
    tr.remove_punctuation()    
    return Response(tr.toJSON(),  mimetype='application/json')


@app.route('/api/v1.0/data/tokens', methods=['POST'])
def get_tokens_from_text():
    stop_words = request.args.get("stop-words")
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    if (stop_words == "false"):
        return Response(to_json_array(lp.remove_stops()),  mimetype='application/json')
    else:
        return Response(to_json_array(lp.pos()),  mimetype='application/json')

@app.route('/api/v1.0/entities', methods=['GET'])
def get_entities():
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.entities()),  mimetype='application/json')


@app.route('/api/v1.0/entities/<string:kind>', methods=['GET'])
def get_entities_of_kind(kind):
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.entities_of_lind(kind)),  mimetype='application/json')


@app.route('/api/v1.0/sentences', methods=['GET'])
def get_sentences():
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.sentences()),  mimetype='application/json')


@app.route('/api/v1.0/match/<string:matcher>', methods=['GET'])
def get_entities_with_matcher(matcher):
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.matcher(matcher)),  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')   