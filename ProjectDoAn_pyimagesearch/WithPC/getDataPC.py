import base64

import cv2

import Aes256CBC
from PIL import Image
from io import BytesIO

import paho.mqtt.client as paho

topic = "testServo"
mqtt_broker = "192.168.0.103"
mqtt_port = 1883

count = 0

frameSize = (640, 480)
out = cv2.VideoWriter('output_video.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 60, frameSize)

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
    imgRes = Image.frombytes("RGB", frameSize, img, "raw", "BGR")
    p = "data/data." + str(count) + ".jpg"
    imgRes.save(p)
    frame = cv2.imread(p)
    out.write(frame)
    # cv2.imshow("frame", frame)

client = paho.Client()
client.connect(mqtt_broker, mqtt_port)
client.subscribe(topic)
client.on_message = on_message
client.loop_forever()
out.release()

