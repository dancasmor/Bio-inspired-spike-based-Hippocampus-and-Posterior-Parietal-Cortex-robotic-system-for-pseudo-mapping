#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <SoftwareSerial.h>

// Serial pins
const byte rxPin = 12;
const byte txPin = 19; 
SoftwareSerial softSerial(rxPin, txPin);

// UDP Server
const char* ssid     = "robot_control";
const char* password = "spinnaker.pass";
IPAddress laptop = IPAddress(192, 168, 4, 2);
const int rcv_port = 8888;
const int laptop_rcv_port = 8889;
WiFiUDP send_udp;
WiFiUDP rcv_udp;
char packetBuffer[64];

// Command pins
const byte command1 = 22;
const byte command2 = 23;
const byte command3 = 14;
const byte command4 = 15;
const byte command5 = 33;
const byte read_finish = 27;
int ack = 0;

void setup(){
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);

  pinMode(command1, OUTPUT);
  pinMode(command2, OUTPUT);
  pinMode(command3, OUTPUT);
  pinMode(command4, OUTPUT);
  pinMode(command5, OUTPUT);
  pinMode(read_finish, INPUT);

  digitalWrite(command1, LOW);
  digitalWrite(command2, LOW);
  digitalWrite(command3, LOW);
  digitalWrite(command4, LOW);
  digitalWrite(command5, LOW);

  softSerial.begin(9600);
  while(!softSerial){
    delay(1);
  }
  
  WiFi.softAP(ssid, password);
  
  /*IPAddress myIP = WiFi.softAPIP();
  Serial.println(myIP);*/

  rcv_udp.begin(rcv_port);  // Listening port
}

void loop() {
  // Read from serial and send to client
  if(softSerial.available()){
    char c = softSerial.read();

    send_udp.beginPacket(laptop, laptop_rcv_port);
    send_udp.write(c);
    send_udp.endPacket();
  }

  // Read from client and send to serial
  int packetSize = rcv_udp.parsePacket();
  if(packetSize > 0){             
    int len = rcv_udp.read(packetBuffer, 64);
    if(len > 0){
      packetBuffer[len] = '\0';
    }

    //softSerial.print(packetBuffer); // TODO: Adafruit Feather continously retransmits the data
    if(packetBuffer[0] == 1){
      digitalWrite(command1, HIGH);
    }else if(packetBuffer[0] == 2){
      digitalWrite(command2, HIGH);
    }else if(packetBuffer[0] == 3){
      digitalWrite(command3, HIGH);
    }else if(packetBuffer[0] == 4){
      digitalWrite(command4, HIGH);
    }else if(packetBuffer[0] == 5){
      digitalWrite(command5, HIGH);
    }
    
    ack = digitalRead(read_finish);
    while(ack != HIGH){
      ack = digitalRead(read_finish);
      delayMicroseconds(10);
    }
    digitalWrite(command1, LOW);
    digitalWrite(command2, LOW);
    digitalWrite(command3, LOW);
    digitalWrite(command4, LOW);
    digitalWrite(command5, LOW);
  }
}
