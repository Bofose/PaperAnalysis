from app import app
from flask import request, jsonify
from service import upload_function
import json


@app.route('/paperanalysis/uploadpaper', methods=['POST'])
def register_model():
    if 'file' not in request.files:
        resp = jsonify({'code': 400, 'data': None, 'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'code': 400, 'data': None, 'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file:
        isthisFile = request.files.get('file')
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                if key == 'data':
                    jsondata = value
        jsondatavalue = json.loads(jsondata)
        message, code, data = upload_function.save_paper_details(isthisFile, jsondatavalue)
        resp = jsonify({'code': code, 'data': data, 'message': message})
        if code == 400:
            resp.status_code = 400
            return resp
        return resp


if __name__ == "__main__":
    app.run(debug=True, port=5003)
