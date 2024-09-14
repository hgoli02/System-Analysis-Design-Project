# System Analysis Design Project

This project is a system analysis and design project that aims to develop a distributed dockerized message queue with cool abilites.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Clients](#clients)

## Installation

1. Usage:

   ```bash
   docker build . -t kalhasti:latest
   docker compose down
   docker compose up --scale queue=1
   ```
   now you have a running instance of the application (check the yaml file for the ports)

2. Clients:

   We have a few clients that are using our application. They are:
    1- Interactive Python Client
    2- Python Client
    3- Java Client

## Clients
    client.py
    client_flask.py
    JavaClient.java
 
