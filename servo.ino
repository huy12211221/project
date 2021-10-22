#include <Servo.h>
#include "DHT.h"

const int DHTPIN = 2;       
const int DHTTYPE = DHT11;

Servo servo;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  servo.attach(5);
  servo.write(0);
  dht.begin();
}

void loop() {
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    Serial.print(h);
    Serial.print(",");
    Serial.println(t);
    delay(200);

    if (Serial.available() != 0){
       String data = Serial.readString();
       servo.write(data.toInt());
       Serial.println(data);
    }
}
