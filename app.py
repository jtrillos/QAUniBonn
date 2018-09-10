from flask import Flask,request,jsonify

import numpy as np
from gensim.models import FastText


def get_word_embedding(word):
    return model[word]


def getQuestionVector(question):
    words=question.split()
    #print words
    numberWords=len(words)
    questionVector=np.zeros(300)
    for word in words:
        wordVector=get_word_embedding(word)
        questionVector=np.add(questionVector,wordVector)
    questionVector=np.divide(questionVector,numberWords)
    return questionVector






app = Flask(__name__)

@app.route('/')
def hello_world():
    return "this is a dummy fasttext server"

@app.route('/getvec', methods=['POST'])
def get_vec():
    req = request.json['question']
    return getQuestionVector(question)


if __name__ == '__main__':
    model = FastText.load_fasttext_format('data/wiki.en.bin')
    app.run(host='0.0.0.0', port=8000, debug=True)
