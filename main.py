import bz2, os, re
from urllib2 import unquote
from elasticsearch import helpers
from elasticsearch import Elasticsearch
from SPARQLWrapper import SPARQLWrapper, JSON
import simplejson as json
import sys
import nerQuestion as ner

reload(sys)
sys.setdefaultencoding('utf8')

# using directly the endpoint to query
sparql = SPARQLWrapper("http://localhost:3030/kommunikationsroboter/sparql")
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

indexName = "kommunikationsroboter"
docTypeName = "robot"

# given a question
question = "Where is SDA?"
# extract the entity
entity = ner.extract_entity_question (question)
# print entity
newQuestion = ner.replace_entity_name(question, entity)

# search the URI of the entity
uriEntity = es.search(index=indexName, body={
  'query': {
    'match': {
      'label': entity[0],
     }
  }
})

# print result["hits"]["hits"][0]["_source"]["uri"]

# Given a query question and an URI
def exampleQueryFuseki (question, uri):
        query ="""
                prefix dbo: <http://dbpedia.org/ontology/>
				prefix schema: <http://schema.org/>
				SELECT ?x {
				  GRAPH ?g {<%s> dbo:location ?loc.
				                    ?loc schema:streetAddress ?address; 
				                     schema:postalCode ?postal; 
				                     schema:addressLocality ?city.
				    BIND(concat(STR(?address), " ", STR(?postal), " ", STR(?city)) as ?x)
				  }
				}
        """% uri

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        # print results
        if not results["results"]["bindings"]:
            json_results = {
              'question': question,
              'response': 'No results found'
            }
            # resutl in json
            print json.dumps(json_results)
            #sys.exit(1)
        else:
            # print "The address is " + results["results"]["bindings"][0]["x"]["value"]
            json_results = {
              'question': question,
              'response': results["results"]["bindings"][0]["x"]["value"]
            }
            # resutl in json
            print json.dumps(json_results)

exampleQueryFuseki(question, uriEntity["hits"]["hits"][0]["_source"]["uri"])