import numpy as np
import pandas
from gensim.models import FastText
path_to_data = '/data/nikolskyy'
model = FastText.load_fasttext_format(path_to_data+'wiki.de.bin')



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
        global templateMatrix
        global templatesList
        global templates
        templatesList = []
        templates = []

        with open('questions.txt') as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        for question in range(len(content)):
            templates.append(question)
            i = i + 1
            questionVector = getQuestionVector(question)
            templatesList.append(questionVector)
        templateMatrix = np.array(templatesList)
        np.save('templatesMatrix', templateMatrix)
        return templateMatrix



