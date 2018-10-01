from flask import Flask,request,jsonify
from exceptions import OSError,  ValueError, TypeError
from gensim import corpora
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from gensim.models import FastText
import bz2, os, re
from urllib2 import unquote
from elasticsearch import Elasticsearch, helpers
from SPARQLWrapper import SPARQLWrapper, JSON
import simplejson as json
import sys
import nerQuestion as ner

reload(sys)
sys.setdefaultencoding('utf8')

#############################
######GLOBAL VARIABLES#######
# using directly the endpoint to query
sparql = SPARQLWrapper("http://localhost:3030/kommunikationsroboter/sparql")
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

indexName = "kommunikationsroboter"
docTypeName = "robot"
############################

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

# Find the cosine similarity comparing templates.json with question
def ranking(question):
  with open('data/templates.json', 'r') as templates_json:
    try:
      templatesDict = json.load(templates_json)
      templateVectorMatrix = np.array([])
      n=0
      for template in templatesDict :
        n=n+1
        vector = np.array(template['vec_representation'])
        if templateVectorMatrix.size > 0:
          if templateVectorMatrix.size==1:
            templateVectorMatrix = np.stack((templateVectorMatrix,vector))
          else:
            templateVectorMatrix = np.vstack((templateVectorMatrix,vector))
        else:
          templateVectorMatrix = np.hstack((templateVectorMatrix,vector))

      sims=cosine_similarity(getQuestionVector(question).reshape(1,-1),templateVectorMatrix)
      sims_index = np.argsort(sims)[0][::-1][:n]

      for i in range(n):
        templatesDict[i]['ranking'] = sims[0][i]

      # sort temaplates by ranking
      templatesDict = sorted(templatesDict, key=sort_by_ranking, reverse=True)
      #print("sims_index computed")
      #print(str(sims_index))

      return json.dumps(templatesDict)
    except ValueError:
      print("error")
      return {'err' : 'No templates found'}

def sort_by_ranking(d):
  try:
      return float(d['ranking'])
  except KeyError:
      return 0

# Given a query question, uri and a jsonTemplate returns the answer
def queryFuseki (question, uri, jsonTemplate):
  flag = False
  for item in json.loads(jsonTemplate):
    sparqlQuery = item['sparql_query'] % uri
    sparql.setQuery(sparqlQuery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print results
    if results.get('boolean'):
      json_results = {
        'question': question,
        'response': results["boolean"]
      }
      flag = True
      break
    elif results["results"]["bindings"]:
      r = ""
      for item in results["results"]["bindings"]:
        if r == "":
          r = item["x"]["value"]
        else:
          r = r + ", " + item["x"]["value"]
      json_results = {
        'question': question,
        'response': r
      }
      flag = True
      break
  
  if flag:
    # resutl in json
    return json.dumps(json_results)
  else:
    json_results = {
      'question': question,
      'response': "No results found"
    }
    # resutl in json
    return json.dumps(json_results)
app = Flask(__name__)

@app.route('/')
def hello_world():
  return "this is a dummy fasttext server"
 
# Create the templates.json 
@app.route('/add-template', methods=['POST'])
def addtemplate():
  question = request.json['question']
  sparl_query= request.json['sparql']
  vec = getQuestionVector(question).tolist()

  with open('data/templates.json','r') as templates_json:
    try:
      templatesDict = json.load(templates_json)
    except ValueError:
      print("no json could be read")
      templatesDict=[]

  ranking = -1;

  for template in templatesDict:
    print(type(template))
    try:
      ranking = template['ranking'] if(template['ranking'] > ranking) else ranking
    except TypeError:
      ranking = ranking

  ranking = ranking + 1

  new_entry = {
    'ranking' : ranking,
    'question' : question,
    'vec_representation' : vec,
    'sparql_query' : sparl_query
  }
  templatesDict.append(new_entry)

  with open('data/templates.json', 'w+') as templates_json:
    json.dump(templatesDict,templates_json)

  return "Template saved" + str(new_entry)

@app.route('/ask', methods=['POST'])
def get_question():
  if not request.json or not 'question' in request.json:
      abort(400)
  question = request.json['question']
  # extract the entity
  entity = ner.extract_entity_question (question)
  newQuestion = ner.replace_entity_name(question, entity)

  # search the URI of the entity
  uriEntity = es.search(index=indexName, body={
    'query': {
      'match': {
        'label': entity[0],
       }
    }
  })

  # Integration
  jsonTemplate = ranking(newQuestion)
  return queryFuseki(question, uriEntity["hits"]["hits"][0]["_source"]["uri"],jsonTemplate)

if __name__ == '__main__':
  model = FastText.load_fasttext_format('/home/eis/wiki_en/wiki.en.bin')
  app.run(host='0.0.0.0', port=8000, debug=True)
