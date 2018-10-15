# QAUniBonn

## List of dependencies
- Docker
- Python 2.7

## Steps of installation
- Download or clone the repository ```$ git clone https://github.com/jtrillos/QAUniBonn.git ```
- Create a virtual environment for Python 2.7 ```$ virtualenv pythenv --python=python2  ```
	- Run the virtual environment ```$ source pythenv/bin/activate```
	- Install the dependencies ```$ pip install elasticsearch SPARQLWrapper simplejson gensim pandas flask nltk ```
		```$ pip install -U scikit-learn```
- Run ```$ python IndexSDAKG.py ``` to import all the entities and labels of the KG to ElasticSearch (This is needed only when the KG is being updated or it is the first time).
- Download [wiki-en.bin fasttext](https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip)
	- Move the wiki.en.bin file into the data folder of the project.
- If there is no data of nltk uncomment the lines 8 - 11 in nerQuestion.py

## Start Fuseki Server Docker
- Pull Docker Fuseki Server 
```sh
$ docker pull stain/jena-fuseki
```
- Run Docker Fuseki Server (Remember to change the path whereFuseki_TripleStore is stored)
```sh
$ docker run -d --name qaunibonn_fuseki -p 3030:3030 -e ADMIN_PASSWORD=robot -v /path/to/Docker/Fuseki_TripleStore/:/fuseki/ -it stain/jena-fuseki
```

## Start ElasticSearch Server Docker
- Pull Docker ElasticSearch Server
```sh
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```
- Run Docker ElasticSearch Server
```sh
$ docker run -d  --name elasticsearch -e transport.host=0.0.0.0 -e cluster.name=elasticsearch -e http.host=0.0.0.0 -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

If server does not connect with the container of ElasticSearch Server
```sh
$ docker run -d --name qaunibonn_elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

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
