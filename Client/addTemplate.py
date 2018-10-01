import requests

def addtemplate(question,sparql):
        req = {
                'question':question,
                'sparql':sparql
                }
        res = requests.post('http://0.0.0.0:8000/add-template',json=req)
        return res


question = input("question")
sparql = input("sparql")
addtemplate(question,sparql)




