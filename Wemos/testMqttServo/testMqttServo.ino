#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>
#include "Base64.h"

Servo myservo; 
int pos = 0;
int buttonState = 0; 
int directionState = 0; 
#define servo D2
#define buttonPin D3

const char* ssid = "Meo Meo"; //"TP-Link_111"; 
const char* password = "mangcut9987";//"44455071"; 
const char* mqtt_server = "broker.mqtt-dashboard.com";//ip mqtt-windowm   //
const int mqtt_port = 1883;
const char *topic = "testServo";
String clientId = "mqtt-servo";

const char *CMD_OPEN = "open";
const char *CMD_CLOSE = "close";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  char mesages[100];

  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("]");

  for (int i = 0; i < length; i++)
  {
    char receivedChar = (char)payload[i];

    mesages[i] = receivedChar;
    Serial.print(receivedChar);
  }
  int inputStringLength = sizeof(mesages); 
  int decodedLength = Base64.decodedLength(mesages, inputStringLength);
  char decodedString[decodedLength];
  Base64.decode(decodedString, mesages, inputStringLength);
  Serial.print(decodedString);
  Serial.println();
  if (strcmp(mesages,CMD_OPEN) == 0 && directionState == 0) {
    directionState = 1;
    openDoor();
  } 
  else if (strcmp(mesages,CMD_CLOSE) == 0 && directionState == 1) {
    directionState = 0;   
    closeDoor();
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      //client.publish(topic, "hello");
      client.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  myservo.attach(servo);
  pinMode(buttonPin, INPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  thuCong();
}

void closeDoor(){
  for (pos = 0; pos <= 135; pos += 1) {
    myservo.write(pos);
    delay(15);
  }
  client.publish(topic, "closeDoor");
  client.subscribe(topic); 
}

void openDoor(){
  for (pos = 135; pos >= 0; pos -= 1) {
    myservo.write(pos);
    delay(15);
  }
  client.publish(topic, "openDoor"); 
  client.subscribe(topic);
}

void thuCong(){
   buttonState = digitalRead(buttonPin);
   if (directionState == 0){
     if (buttonState == HIGH) {
        directionState = 1;
        openDoor();
     }
 
   } else if (directionState == 1) {
     if (buttonState == HIGH) {
        directionState = 0;   
        closeDoor();
     }
   }
}
