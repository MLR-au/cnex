FROM debian:latest

# Install some dependencies
RUN apt-get update && \
    apt-get install -y vim-nox git libxml2-dev libxslt1-dev python-dev \
        nodejs zlib1g-dev python-pip python-magic

RUN pip install lxml requests pyramid waitress cookiecutter \
        pymongo msgpack ujson networkx

COPY run-service /usr/local/bin/

WORKDIR /srv/cnex/api

ENTRYPOINT /usr/local/bin/run-service
