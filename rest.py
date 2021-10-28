#!flask/bin/python
import os
import json
import tempfile

import spacy
from file_response import FileResponse
from part_of_speech import PartOfSpeech
from flask import Flask, Response, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def get_named_entities(lines):
    return nlp(lines).ents

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extnesion(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return "tmp"

@app.route('/upload', methods=['POST'])
def upload_file():
    response = FileResponse("")
    # check if the post request has the file part
    if 'file' not in request.files:
        return Response(response.toJSON(),  mimetype='application/json')
        
    file = request.files['file']

    if file and allowed_file(file.filename):
        extension = get_extnesion(file.filename)
        temp_name = next(tempfile._get_candidate_names()) + "." + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_name))
        response.filename = temp_name

    return Response(response.toJSON(),  mimetype='application/json')


@app.route('/todo/api/v1.0/process', methods=['GET'])
def get_tokens():
    f = open('input.txt', 'r')
    doc = nlp(f.read())
    results = '['
    first = 0
    for token in doc:
        if first != 0:
            results = results + ','
        p = PartOfSpeech(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)
        results = results + p.toJSON()
        first = 1
    results = results + ']'
    return Response(results,  mimetype='application/json')


@app.route('/todo/api/v1.0/process/<string:tag>', methods=['GET'])
def get_token_of_type(tag):
    f = open('input.txt', 'r')
    doc = nlp(f.read())
    results = '['
    first = 0
    for token in doc:
        if token.tag_ == tag:
            if first != 0:
                results = results + ','
            p = PartOfSpeech(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                    token.shape_, token.is_alpha, token.is_stop)
            results = results + p.toJSON()
            first = 1
    results = results + ']'
    return Response(results,  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)   