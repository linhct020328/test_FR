from cypher.Aes256CBC import *
import paho.mqtt.client as paho
import ssl
from time import strftime

clientId = "mqtt-servo"
topic = "testServo"
mqtt_broker = "192.168.0.103"  # ip mqtt-windowm   #"broker.mqtt-dashboard.com"
mqtt_port = 1883
mqttUser = "linh99"
mqttPassword = "1234567890"

pathCa = './certs_localhost/mqtt_ca.crt'
pathClient = './certs_localhost/mqtt_client.crt'
pathClientKey = './certs_localhost/mqtt_client.key'

directionState = 0

openState = "Open door"
closeState = "Close door"
unknownState = "Unknown face"

def convertAesToMsg(string, key, iv):
    decoded = decrypt_aes_256(string, key, iv)
    return decoded

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    global directionState
    list_states = []
    f = open("listStates/stateslist.txt", "r")
    x = f.read()
    z = x.rstrip().split("\n")
    for i in z:
        smallList = i.rstrip()
        list_states.append(smallList)
    leng = len(z)
    id  = leng
    f.close()

    key = 'qwertyuiopasdfghjklzxcvbnm123456'
    iv = 'caothithuylinh99'
    message = (msg.payload).decode("utf-8")
    if (len(message) <= 24):
        text_msg = convertAesToMsg(message, key, iv)
        msgRes = str(text_msg)
        if (msgRes == "openDoor" or msgRes == "open") and directionState == 0:
            directionState = 1
            f = open("listStates/stateslist.txt", "a+")
            f.write("\n" +
                    "   " + str(id) +
                    "                       " + strftime("%d/%m/%y at %I:%M%p") +
                    "                                       " + openState)
            f.close()

        elif (msgRes == "closeDoor" or msgRes == "close") and directionState == 1:
            directionState = 0
            f = open("listStates/stateslist.txt", "a+")
            f.write("\n" +
                    "   " + str(id) +
                    "                       " + strftime("%d/%m/%y at %I:%M%p") +
                    "                                       " + closeState)
            f.close()
    else:
        f = open("listStates/stateslist.txt", "a+")
        f.write("\n" +
                "   " + str(id) +
                "                       " + strftime("%d/%m/%y at %I:%M%p") +
                "                                       " + unknownState)
        f.close()

# def runState():
client = paho.Client()
client.tls_set(pathCa, pathClient, pathClientKey, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
client.connect(mqtt_broker, mqtt_port)
client.username_pw_set(username=mqttUser, password=mqttPassword)
client.subscribe(topic)
client.on_message = on_message
client.loop_forever()

# if __name__ == "__main__":
#     runState()