import bz2, os, re
from urllib2 import unquote
from elasticsearch import helpers
from elasticsearch import Elasticsearch
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

import simplejson as json

reload(sys)
sys.setdefaultencoding('utf8')

# using directly the endpoint to query
sparql = SPARQLWrapper("http://localhost:3030/kommunikationsroboter/sparql")

indexName = "kommunikationsroboter"
docTypeName = "robot"

def roomnumber (uri):
        query ="""
                PREFIX sda: <http://beta.sda.tech/schema/>
                PREFIX ex: <http://example.org/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                SELECT ?x {
                GRAPH ?g {

                        <%s>  a foaf:Person; ex:address ?room. 
                        ?room ex:name ?x.
                  
                
                }}
        """% uri["hits"]["hits"][0]["_source"]["uri"]

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if not results["results"]["bindings"]:
            print ("No results found")
            sys.exit(1)
        else:
                print "The room is " + results["results"]["bindings"][0]["x"]["value"]
                json_results=  json.dumps(results,separators=(',',':'),sort_keys=True) #results to json
                print json_results

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
userSearch = raw_input("What is the room of ")
result = es.search(index=indexName, body={
  'query': {
    'match': {
      'label': userSearch,
     }
  }
})

roomnumber(result)


print "Proccess finished"