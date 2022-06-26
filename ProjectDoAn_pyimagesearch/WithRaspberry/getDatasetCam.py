import paho.mqtt.client as paho
import cv2
import time
from time import strftime
import base64
import Aes256CBC

clientId = "mqtt-servo"
topic = "testServo"
mqtt_broker = "192.168.0.103"#ip mqtt-windowm   #"broker.mqtt-dashboard.com"
mqtt_port = 1883

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

face_detector = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

count = 0

def convertMsgToAes(msg, key, iv):
    encoded = Aes256CBC.encrypt_aes_256(msg, key, iv)
    return encoded

while True:
    start_time = time.time()
    ret, frame = cam.read()

    client = paho.Client()
    client.connect(mqtt_broker, mqtt_port)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=7, minSize=(int(minW), int(minH)))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("y"):
        key = 'qwertyuiopasdfghjklzxcvbnm123456'  # 32bit
        iv = "caothithuylinh99"  # 16bit
        imgByte = frame.tobytes()
        img = imgByte.hex()
        imgSend = convertMsgToAes(img, key, iv)
        client.publish(topic, imgSend)
        count += 1

    elif key == ord("q"):
        break

    elif count >= 100:
        break


