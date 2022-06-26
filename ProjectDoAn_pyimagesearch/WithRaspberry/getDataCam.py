import paho.mqtt.client as paho
import cv2
import time
from time import strftime
import base64
import Aes256CBC

clientId = "mqtt-servo"
topic = "testServo"
mqtt_broker = "192.168.0.103"  # ip mqtt-windowm   #"broker.mqtt-dashboard.com"
mqtt_port = 1883

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

def convertMsgToAes(msg, key, iv):
    encoded = Aes256CBC.encrypt_aes_256(msg, key, iv)
    return encoded

while True:
    start_time = time.time()
    ret, frame = cam.read()

    client = paho.Client()
    client.connect(mqtt_broker, mqtt_port)


    key = 'qwertyuiopasdfghjklzxcvbnm123456'  # 32bit
    iv = "caothithuylinh99"  # 16bit

    if ret:
        # _, img_encode = cv2.imencode('.jpg', frame)
        imgByte = frame.tobytes()
        img = imgByte.hex()
        imgSend = convertMsgToAes(img, key, iv)
        client.publish(topic, imgSend)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break



