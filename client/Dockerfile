# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /usr/src/hypercube-client

ENV APP_NAME=hypercube-client
ENV LOCAL_HOST=0.0.0.0
ENV INIT_PORT=8880
ENV HOP_SERVER_PORT=6000
#ENV HYPERCUBE_SIZE=3
#ENV SUPERSET_THRESHOLD=10


#FROM opencv:latest
COPY . .
RUN pip3 install -r requirements.txt

############# ADDED FROM MICHELE
RUN pip3 install py-algorand-sdk
#CMD [ "mkdocs", "serve",  "--dev-addr=0.0.0.0:8000" ]




#EXPOSE 5000


#CMD ["sh", "-c", "python3 server.py $INIT_PORT"]