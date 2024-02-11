# System Analysis Design Project

This project is a system analysis and design project that aims to [briefly describe the purpose of the project].

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Clients](#clients)

## Installation

To set up the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git

    cd your-repository
    ```
2. Usage:

   ```bash
   docker build . -t kalhasti:latest
   docker compose down
   docker compose up --scale queue=1
   ```
   now you have a running instance of the application (check the yaml file for the ports)

3. Clients:

   We have a few clients that are using our application. They are:
    1- Interactive Python Client
    2- Python Client
    3- Java Client

## Clients
    client.py
    client_flask.py
    JavaClient.java
 