#!flask/bin/python
import os
import json
import spacy
from NamedEntity import NamedEntity
from PartOfSpeech import PartOfSpeech
from flask import Flask, Response, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return Response('{"name": "nofile"}',  mimetype='application/json')
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return Response('{"name": "hello"}',  mimetype='application/json')

    return Response('{"name": "goodbye"}',  mimetype='application/json')


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