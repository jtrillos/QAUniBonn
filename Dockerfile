FROM java:8

# Install vim
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

# Install python
RUN apt-get update \
  && apt-get install -y python-pip python-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python python \
  && pip install --upgrade pip 
RUN pip install elasticsearch SPARQLWrapper simplejson gensim pandas flask

# Install fuseki
RUN apt-get install -y ruby-full
WORKDIR /
RUN wget http://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-3.4.0.zip
RUN unzip apache-jena-fuseki-3.4.0.zip && rm apache-jena-fuseki-3.4.0.zip
RUN chmod +x apache-jena-fuseki-3.4.0/bin/s-*

# Copy files
WORKDIR /QAUniBonn
ADD . /QAUniBonn

#Download wiki.en
WORKDIR /QAUniBonn/wiki_en
RUN wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip
RUN unzip wiki.en.zip && rm wiki.en.zip

#Run Flask server API
WORKDIR /QAUniBonn/api
ENTRYPOINT ["python"]
CMD ["app.py"]