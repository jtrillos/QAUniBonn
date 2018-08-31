# QAUniBonn

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
$ docker run -d  --name elasticsearch -e transport.host=0.0.0.0 -e cluster.name=elasticsearch -e http.host=0.0.0.0 -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```