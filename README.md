# QAUniBonn

# Install without Docker:
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
	- Run Fuseki ```$ ./fuseki-server -config=/path/to/the/repository/QAUniBonn/config.ttl ```
	- The server starts at `http://localhost:3030/`
- Create a virtual environment for Python 2.7 ```$ virtualenv pythenv --python=python2  ```
	- Run the virtual environment ```$ source pythenv/bin/activate```
	- Install the dependencies ```$ pip install elasticsearch SPARQLWrapper simplejson gensim pandas flask```
- Run ```$ python IndexSDAKG.py ``` to import all the entities and labels of the KG to ElasticSearch (This is needed only when the KG is being updated or it is the first time).
- Run ```$ python searchSDAES.py ``` to search and get a response 
- Download [wiki-en.bin fasttext](https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip)
- Go to templateWrapper.py and modify the path in line 4
- Run ```$ python templateWrapper.py ```

# Install with Docker:
## List of dependencies
- Docker

## Steps of installation
- Download or clone the repository ```$ git clone https://github.com/jtrillos/QAUniBonn.git ```

## Start Fuseki Server Docker
- Pull Docker Fuseki Server 
```sh
$ docker pull stain/jena-fuseki
```
- Copy the folder Fuseki_TripleStore in the server
- Run Docker Fuseki Server (Remember to change the path where Fuseki_TripleStore is stored)
```sh
$ docker run -d --name qaunibonn_fuseki -p 3030:3030 -e ADMIN_PASSWORD=robot -v /path/to/Fuseki_TripleStore/:/fuseki/ -it stain/jena-fuseki
```

## Start ElasticSearch Server Docker
- Pull Docker Fuseki Server 
```sh
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```
- Run Docker ElasticSearch Server
```sh
$ docker run -d  --name elasticsearch -p 9200:9200 -e transport.host=0.0.0.0 -e cluster.name=elasticsearch -e http.host=0.0.0.0 -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```
