from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO
from subprocess import call
import git
import time
import random

gitupdater = git.cmd.Git("https://github.com/uschults/Viljakuivati.git")
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''
broker = '80.250.119.25'
port = 1883

def on_message(client, userdata, msg):
    #print(msg.topic+" --  "+str(msg.payload))
    data = msg.payload.decode()
    #print(data)
    if(data == "update"):
            print("starting update")
           
            msg = gitupdater.pull()
            print(msg)
            # Shouldn't restart if already up to date
            if(not msg == "Already up to date."):
                print("restarting") 
                call(["sudo", "systemctl", "restart", "kuivati.service"])
                publish(client, "pistate", "Offline")
            #answer
def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            # subscribe for update button
            client.subscribe("update")

        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client


def mqtt_init():
    client = connect_mqtt()
    client.loop_start()
    return client

    
client = mqtt_init()

while (True):
    pass