import numpy as np
import pandas
from gensim.models import FastText
path_to_data = '/home/eis/wiki_en/'
model = FastText.load_fasttext_format(path_to_data+'wiki.en.bin')



def get_word_embedding(word):
    return model[word]

def getQuestionVector(question):
    words=question.split()
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

        with open('data/templates.txt') as f:
             content = f.readlines()

        i=0

        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        for question in range(len(content)):
            templates.append(content[question])
            i = i + 1
            questionVector = getQuestionVector(content[question])
            print(questionVector)
            templatesList.append(questionVector)
        templateMatrix = np.array(templatesList)
        np.save('templatesMatrix', templateMatrix)
        return templateMatrix


vectors = getTemplateVectors()
