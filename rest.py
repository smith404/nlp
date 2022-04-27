#!flask/bin/python
import os
import tempfile
import json

from langdetect import detect

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

language_data = open('data/languages.json')
languages = json.load(language_data)

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


# Static route to serve static resources
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


@app.route('/api/v1.0/data/language', methods=['POST'])
def get_text_language():
    body_text = request.get_data(as_text=True)
    iso2 = detect(body_text)
    item = { "longname": "unknown", "iso2": "xx"}
    items = [lang for lang in languages if lang['iso2'] == iso2]
    if len(items) > 0:
        item = items[0]
    return Response(json.dumps(item),  mimetype='application/json')


@app.route('/api/v1.0/data/tokens', methods=['POST'])
def get_tokens_from_text():
    stop_words = request.args.get("stop-words")
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    if (stop_words == "false"):
        return Response(to_json_array(lp.remove_stops()),  mimetype='application/json')
    else:
        return Response(to_json_array(lp.pos()),  mimetype='application/json')

@app.route('/api/v1.0/entities', methods=['POST'])
def get_entities():
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.entities()),  mimetype='application/json')


@app.route('/api/v1.0/entities/<string:kind>', methods=['POST'])
def get_entities_of_kind(kind):
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.entities_of_lind(kind)),  mimetype='application/json')


@app.route('/api/v1.0/sentences', methods=['POST'])
def get_sentences():
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.sentences()),  mimetype='application/json')


@app.route('/api/v1.0/paragraphs', methods=['POST'])
def get_paragraphs():
    limit = request.args.get("limit")
    if limit is None:
        limit = 0
    try:
        limit_int = int(limit)
    except ValueError:
        limit_int = 0
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.paragraphs(limit_int)),  mimetype='application/json')


@app.route('/api/v1.0/match/<string:matcher>', methods=['POST'])
def get_entities_with_matcher(matcher):
    body_text = request.get_data(as_text=True)
    lp = LanguageProcessor(body_text)
    return Response(to_json_array(lp.matcher(matcher)),  mimetype='application/json')


@app.route('/api/v1.0/compare', methods=['POST'])
def compare_texts():
    body = request.json
    text1 = body['first']
    text2 = body['second']
    result = {}
    result['similarity'] = LanguageProcessor.compare(text1, text2)
    print(LanguageProcessor.compare(text1, text2))
    return Response(json.dumps(result),  mimetype='application/json')


@app.route('/api/v1.0/comparelist', methods=['POST'])
def compare_lists():
    body = request.json
    list1 = body['first']
    list2 = body['second']
    result = []
    for text1 in list1:
        result_list = []
        for text2 in list2:
            comparison = {}
            comparison['result'] = LanguageProcessor.compare(text1, text2)
            result_list.append(comparison)
        result.append(result_list) 
    return Response(json.dumps(result),  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')   