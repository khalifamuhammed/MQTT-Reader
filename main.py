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
