FROM python:alpine
COPY . /app
WORKDIR /app
EXPOSE 8888
# CMD sleep 10000