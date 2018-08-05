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
	- Run Fuseki ```$ ./fuseki-server -config=/path/to/the/repository/QAUniBonn/config.ttl ```
	- The server starts at `http://localhost:3030/`
- Create a virtual environment for Python 2.7 ```$ virtualenv pythenv --python=python2  ```
	- Run the virtual environment ```$ source pythenv/bin/activate```
	- Install the dependencies ```$ pip install elasticsearch ``` and ```$ pip install SPARQLWrapper ```
- Go to the folder ESEntitiesExtraction
	- Run ```$ python IndexSDAKG.py ``` to import all the entities and labels of the KG to ElasticSearch (This is needed only when the KG is being updated or it is the first time).
	- Run ```$ python searchSDAES.py ``` to search and get a response 
