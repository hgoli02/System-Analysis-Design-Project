FROM ubuntu:latest
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && pip3 install --upgrade pip \
    && pip3 install flask \
    && pip3 install requests \
    && pip3 install pythonping \
    && pip3 install prometheus_flask_exporter \
    && rm -rf /var/lib/apt/lists/*
    

COPY . /app
WORKDIR /app
EXPOSE 8000
EXPOSE 8891
EXPOSE 8890
CMD sleep 10000

