import base64
import argparse
import cv2
import os
import Aes256CBC
from PIL import Image

import paho.mqtt.client as paho
import cv2
import numpy as np
import json

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
args = vars(ap.parse_args())

topic = "testServo"
mqtt_broker = "192.168.0.103"
mqtt_port = 1883

label = input("What is your name:")
label = label.strip().lower()

count = 0

def convertAesToMsg(msg, key, iv):
    decoded = Aes256CBC.decrypt_aes_256(msg, key, iv)
    return decoded

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    key = 'qwertyuiopasdfghjklzxcvbnm123456'  # 32bit
    iv = "caothithuylinh99"  # 16bit
    global count
    count = count + 1
    message = (msg.payload).decode("utf-8")
    img_msg = convertAesToMsg(message, key, iv)
    img = bytes.fromhex(img_msg)
    imgRes = Image.frombytes("RGB", (640, 480), img, "raw", "BGR")
    p = os.path.sep.join([args["output"], "{}.jpg".format(label + str(count).zfill(5))])
    imgRes.save(p)


client = paho.Client()
client.connect(mqtt_broker, mqtt_port)
client.subscribe(topic)
client.on_message = on_message
client.loop_forever()
