# Documentation of QAUniBonn

## List of dependencies
- Docker

## Steps of instalation
1. Download or clone the Git repository
```sh
$ git clone https://github.com/jtrillos/QAUniBonn.git
```

### Fuseki Server
2. Pull Docker Fuseki Server
```sh
$ docker pull stain/jena-fuseki
```
2. a. Run Docker Fuseki Server
```sh
$ docker run -d --name qaunibonn_fuseki -p 3030:3030 -e ADMIN_PASSWORD=robot -v /path/to/Docker/Fuseki_TripleStore/:/fuseki/ -it stain/jena-fuseki
```
2. b. Download and extract [Apache Jena Fuseki](http://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-3.4.0.zip)
2. c. Go to apache-jena-fuseki-3.4.0/bin and run the command s-put
```sh
$ ./s-put http://localhost:3030/kommunikationroboter/data http://sda.tech/ path/to/Docker/Fuseki_TripleStore/backups/sda.tech.ttl
```
This process add the Knowledge Graph of SDA in a graph "http://sda.tech/" inside the TripleStore "kommunikationroboter".

### ElasticSearch
3. Pull Docker ElasticSearch
```sh
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```
3. a. Run Docker ElasticSearch
```sh
$ docker run -d --name qaunibonn_elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

### QAUniBonn Repository
4. Install python 2.7 and virtualenv
4. a. Create a virtual environment 
```sh
$ virtualenv pythenv --python=python2
```
4. b. Run the virtual environment
```sh
$ source pythenv/bin/activate
```
4. c. Install the dependencies
```sh
$ pip install elasticsearch SPARQLWrapper simplejson gensim pandas flask nltk 
```
```sh
$ pip install -U scikit-learn
```
5. Download [wiki-en.bin fasttext](https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip)
5. a. Move the wiki-en.bin file into the "data" forlder of the project
6. If there is no data of NLTK in the server, uncomment the lines 8 - 11 in nerQuestion.py
7. Run Client/IndexSDAKG python file to import all the entities and labels of the Knowledge Graph to ElasticSearch (This process is done once or when the Knowledge Graph has been updated).
```sh
$ python IndexSDAKG.py
```

## Run the server
- To run the server
```sh
$ python app.py
```
- To run the server in background
```sh
$ nohup python app.py &
```
## Example of API:
```sh
$ curl -i -H "Content-Type: application/json" -X POST -d '{"question":"Where is SDA?"}' http://localhost:8000/ask
```

### For more information of API
Go to the Documentation folder.