#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import numpy as np
from gensim.models import FastText

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "this is a dummy fasttext server"

@app.route('/getvec/<string:question>')
def get_vec(question):
    wordVector = model[question]
    return str(question)

if __name__ == '__main__':
	model = FastText.load_fasttext_format('wiki_en/wiki.en.bin')
	app.run(debug=True, host='0.0.0.0', port=8000)
