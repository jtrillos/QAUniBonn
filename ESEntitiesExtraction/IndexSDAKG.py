import bz2, os, re
from urllib2 import unquote
from elasticsearch import helpers
from elasticsearch import Elasticsearch
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# using directly the endpoint to query
sparql = SPARQLWrapper("http://localhost:3030/kommunikationsroboter/sparql")

indexName = "kommunikationsroboter"
docTypeName = "robot"

es = Elasticsearch()

print "Wiping any existing index..."
es.indices.delete(index=indexName, ignore=[400, 404])
indexSettings = {
    "mappings": {
        docTypeName: {
            "properties": {
                "label": {
                    "type": "text",
                    "fields": {
                        "text": {
                            "type": "text"
                        }
                    }
                },
                "uri": {
                    "type": "text",
                    "fields": {
                        "text": {
                            "type": "text"
                        }
                    }
                }
            }
        }
    }
}
es.indices.create(index=indexName, body=indexSettings)

count = 0

query = """
    PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct:   <http://purl.org/dc/terms/>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>

    SELECT DISTINCT ?uri ?label 
    WHERE { 
      {?uri foaf:name ?label}
      UNION
      {?uri rdfs:label ?label}
      UNION
      {?uri dct:label ?label}
      UNION
      {?uri dcat:keyword ?label}
    }
""" 
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
if not results["results"]["bindings"]:
    print ("No results found")
    sys.exit(1)
else:
    for result in results["results"]["bindings"]:
        es.index(index=indexName, doc_type=docTypeName, id=count, body={
          'uri': result["uri"]["value"],
          'label': result["label"]["value"],
        })
        count = count + 1
        print result["uri"]["value"] + " ---> " + result["label"]["value"]
    print "Total of index entities: " + `count`
print "Proccess finished"