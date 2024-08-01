# MQTT Reader Client and Mosquitto Broker with Docker

This project demonstrates how to set up an MQTT client using Python with the `gmqtt` library, and a Mosquitto MQTT broker, both running in Docker containers. The client listens for messages on the `/events` topic and logs them.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Publishing Messages](#publishing-messages)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Overview

- **Mosquitto**: An open-source message broker that implements the MQTT protocol.
- **gmqtt**: An asynchronous MQTT client library for Python.
- **Docker**: Used to containerize the application and broker.

## Directory Structure
```commandline
your_project_directory/
├── Dockerfile
├── docker-compose.yml
├── main.py
└── mosquitto/
   ├── config/
   │   └── mosquitto.conf
   ├── data/
   └── log/
```



## Prerequisites

- Docker Desktop installed on your machine.
- Mosquitto client tools installed (for publishing messages manually).

## Setup

### Step 1: Clone the Repository

```
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```
### Step 2: Create Directory Structure and Configuration

```commandline
mkdir -p mosquitto/config mosquitto/data mosquitto/log
```
Create mosquitto/config/mosquitto.conf with the following content:
```commandline
listener 1883
allow_anonymous true
```
### Step 3: Create Dockerfile
Create a Dockerfile in the root directory with the following content:

```commandline
FROM python:3.9-slim

WORKDIR /app

COPY main.py .

RUN pip install gmqtt

CMD ["python", "main.py"]
```

### Step 4: Create Docker Compose File
Create a 'docker-compose.yml' file in the root directory:

```commandline
version: '3'

services:
  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: mosquitto
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log

  mqtt_client:
    build: .
    container_name: mqtt_client
    depends_on:
      - mosquitto
```

### Step 5: Create the Python Application
Create main.py in the root directory with the following content:

```commandline
import asyncio
import logging
from gmqtt import Client as MQTTClient

logging.basicConfig(level=logging.INFO)

class MQTTHandler:
    def __init__(self, client_id):
        # Initialize the MQTT client with a given client_id
        self.client = MQTTClient(client_id)

    def on_connect(self, client, flags, rc, properties):
        # Callback function when the client connects to the broker
        logging.info(f'Connected: {client._client_id}')
        # Subscribe to the /events topic with QoS level 0
        client.subscribe('/events', qos=0)

    def on_message(self, client, topic, payload, qos, properties):
        logging.info(f'Received message on topic {topic}: {payload}')

    async def connect(self, broker_host):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        await self.client.connect(broker_host)

    async def run(self):
        # Connect to the Mosquitto broker and start an infinite loop to keep the client running
        await self.connect('mosquitto')
        while True:
            await asyncio.sleep(1)

async def main():
    # Create an instance of the MQTTHandler with the client ID 'mqtt_client'
    mqtt_handler = MQTTHandler('mqtt_client')
    # Run the MQTT handler
    await mqtt_handler.run()

if __name__ == '__main__':
    # Execute the main function using asyncio's event loop
    asyncio.run(main())


```

### Running the Project
1. Build and Start the Services:
```commandline
docker-compose up --build
```
This command builds the Docker images and starts the Mosquitto broker and MQTT client services.

### Publishing Messages
To manually publish a message to the /events topic, use the following command:
```commandline
mosquitto_pub -h localhost -t "/events" -m '{"sensor_value":20.2}'
```
Make sure you have the Mosquitto client tools installed on your system.

### Output
On the reader side client the output wil look like below:
```commandline
Received message on topic /events: b"'{sensor_value:20.2}'"
```
