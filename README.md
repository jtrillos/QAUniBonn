# QAUniBonn

## List of dependencies
- Python 2.7
- [ElasticSearch](https://www.elastic.co/downloads/elasticsearch)
- [apache-jena-fuseki-3.4.0](http://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-3.4.0.zip)

## Steps of installation
- Download or clone the repository ```$ git clone https://github.com/jtrillos/QAUniBonn.git ```
- Download and install ElasticSearch
	- Start ElasticSearch ```$ sudo service elasticsearch start```
- Download and extract the apache-jena-fuseki-3.4.0
	- Go to the config.ttl in the QAUniBonn repository and modify the path in line 21
	- Run Fuseki ```$ ./fuseki-server -config=/path/to/the/repository/QAUniBonn/Docker/Fuseki_TripleStore/configuration/config.ttl ```
	- The server starts at `http://localhost:3030/`
- Create a virtual environment for Python 2.7 ```$ virtualenv pythenv --python=python2  ```
	- Run the virtual environment ```$ source pythenv/bin/activate```
	- Install the dependencies ```$ pip install elasticsearch SPARQLWrapper simplejson gensim pandas flask nltk ```
		```pip install -U scikit-learn```
- Run ```$ python IndexSDAKG.py ``` to import all the entities and labels of the KG to ElasticSearch (This is needed only when the KG is being updated or it is the first time).
- Download [wiki-en.bin fasttext](https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip)
	- Move the wiki.en.bin file into the data folder of the project.
- If there is not data of nltk uncomment the lines 8 - 11 in nerQuestion.py

If there is no data of nltk uncomment the lines 8 - 11 in nerQuestion.py

## Run Server:
To run the server
```sh
$ python app.py
```

To run the server in background
```sh
$ nohup python app.py &
```

## Example request API:
```sh
$ curl -i -H "Content-Type: application/json" -X POST -d '{"question":"Where is SDA?"}' http://localhost:8000/ask
```
