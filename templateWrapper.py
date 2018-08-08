import numpy as np
from gensim.models import FastText
path_to_data = '/app/'
model = FastText.load_fasttext_format(path_to_data+'data/wiki.de.bin')



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

def getTemplateVectors():

