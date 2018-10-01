import requests

def askQuestion(question):
    req = {'question': question}
    res = requests.post( 'http://localhost:8000/ask',json=req)

question = input()
askQuestion(question)
