#!flask/bin/python
import os
import tempfile

from language_processor import LanguageProcessor
from file_response import FileResponse

from flask import Flask, Response, request, send_file
from flask_cors import CORS

UPLOAD_FOLDER = './temp'

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


@app.route('/api/v1.0/upload', methods=['POST'])
def upload_file():
    response = FileResponse("")
    response.sucess = False
    if 'file' not in request.files:
        return Response(response.toJSON(),  mimetype='application/json')
    file = request.files['file']
    response.original_filename = file.filename
    if file and response.allowed_file():
        extension = response.get_extnesion()
        temp_name = next(tempfile._get_candidate_names()) + "." + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_name))
        response.filename = temp_name
        response.sucess = True
    return Response(response.toJSON(),  mimetype='application/json')


@app.route('/api/v1.0/download/<string:name>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


@app.route('/api/v1.0/clear/<string:name>', methods=['POST'])
def delete_file(filename):
    response = FileResponse(filename)
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        response.sucess = False
    return Response(response.toJSON(),  mimetype='application/json')


@app.route('/api/v1.0/redact/<string:filename>', methods=['GET'])
def redact(filename):
    rtype = request.args.get('rtype')
    entities = request.args.get('entities')
    white_list = request.args.get('w')
    white_list = request.args.get('b')
    print("Type: ", rtype)
    print("Entities: ", entities)
    print("White List: ", white_list)
    print("Black List: ", white_list)
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


@app.route('/api/v1.0/tokens/<string:filename>', methods=['GET'])
def get_tokens(filename):
    lp = LanguageProcessor(FileResponse.text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    return Response(to_json_array(lp.pos()),  mimetype='application/json')


@app.route('/api/v1.0/tokens/<string:filename>/<string:tag>', methods=['GET'])
def get_token_of_type(filename, tag):
    lp = LanguageProcessor(FileResponse.text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    return Response(to_json_array(lp.pos_of_type(tag)),  mimetype='application/json')


@app.route('/api/v1.0/entities/<string:filename>', methods=['GET'])
def get_entities(filename):
    lp = LanguageProcessor(FileResponse.text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    lp.add_black_list('Securitisation;flexibly')
    lp.add_white_list('movements;speculate')
    return Response(to_json_array(lp.entities()),  mimetype='application/json')


@app.route('/api/v1.0/entities/<string:filename>/<string:kind>', methods=['GET'])
def get_entities_of_kind(filename, kind):
    lp = LanguageProcessor(FileResponse.text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    return Response(to_json_array(lp.entities_of_lind(kind)),  mimetype='application/json')


@app.route('/api/v1.0/sentences/<string:filename>', methods=['GET'])
def get_sentences(filename):
    lp = LanguageProcessor(FileResponse.text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    return Response(to_json_array(lp.sentences()),  mimetype='application/json')


@app.route('/api/v1.0/sentiment', methods=['GET'])
def get_sentiment():
    text = str(request.get_data().decode())
    lp = LanguageProcessor(text)
    return Response(lp.sentiment().toJSON(),  mimetype='application/json')


@app.route('/api/v1.0/match/<string:filename>/<string:matcher>', methods=['GET'])
def get_entities_with_matcher(filename, matcher):
    lp = LanguageProcessor(FileResponse.text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    return Response(to_json_array(lp.matcher(matcher)),  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)   