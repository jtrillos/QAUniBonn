import requests

def askQuestion(question):
    req = {'question': question}
    res = requests.post( 'http://localhost:8000/ask',json=req)
    print res.content

question = input()
askQuestion(question)
