#!flask/bin/python
import os
import tempfile

import fitz
import spacy

from language_processor import LanguageProcessor
from file_response import FileResponse
from part_of_speech import PartOfSpeech
from flask import Flask, Response, flash, request, redirect, url_for
from flask_cors import CORS

UPLOAD_FOLDER = './temp'

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app)

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

def get_named_entities(lines):
    return nlp(lines).ents

def get_extnesion(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return "tmp"

@app.route('/upload', methods=['POST'])
def upload_file():
    response = FileResponse("")
    if 'file' not in request.files:
        return Response(response.toJSON(),  mimetype='application/json')
    file = request.files['file']
    if file and FileResponse.allowed_file(file.filename):
        extension = get_extnesion(file.filename)
        temp_name = next(tempfile._get_candidate_names()) + "." + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_name))
        response.original_filename = file.filename
        response.filename = temp_name
    return Response(response.toJSON(),  mimetype='application/json')


@app.route('/api/v1.0/tokens', methods=['GET'])
def get_tokens():
    f = open('input.txt', 'r')
    lp = LanguageProcessor(f.read())
    return Response(to_json_array(lp.pos()),  mimetype='application/json')


@app.route('/api/v1.0/tokens/<string:tag>', methods=['GET'])
def get_token_of_type(tag):
    f = open('input.txt', 'r')
    lp = LanguageProcessor(f.read())
    return Response(to_json_array(lp.pos_of_type(tag)),  mimetype='application/json')

@app.route('/api/v1.0/entities', methods=['GET'])
def get_entities():
    f = open('input.txt', 'r')
    lp = LanguageProcessor(f.read())
    return Response(to_json_array(lp.entities()),  mimetype='application/json')


@app.route('/api/v1.0/entities/<string:kind>', methods=['GET'])
def get_entities_of_kind(kind):
    f = open('input.txt', 'r')
    lp = LanguageProcessor(f.read())
    return Response(to_json_array(lp.entities_of_lind(kind)),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)   