#include <SPI.h>
#include "Adafruit_MAX31855.h"
#define DO 3
#define CS 4
#define CK 5
Adafruit_MAX31855 thermocouple(CK, CS, DO);
int relay = 7;
int fanPin = 8;
void setup()
{
  
  Serial.begin(9600);
  Serial.print("MAX6675 test");
  if (!thermocouple.begin()) 
  {
    Serial.print("ERROR.");
    while (1) delay(10);
  }

  Serial.print("Done");
  pinMode(relay, OUTPUT);
  pinMode(fanPin, OUTPUT);
  
}

void loop()
{
  double f = thermocouple.readCelsius();
  

  if (isnan(f)) {
     Serial.println("Thermocouple fault(s) detected!");
     uint8_t e = thermocouple.readError();
   } 
   
   else {
     double c=(f-32) * 5 / 9;
     Serial.print("C = ");
     Serial.println(c);
   }

  delay(1000);

  if(f<60){
     
     analogWrite(fanPin, 0);
    
     digitalWrite(relay,HIGH);
     Serial.println("hit");
      delay(10000);
     digitalWrite(relay,LOW);
      delay(1000);
   }
   else{ 
   digitalWrite(relay,LOW);
   delay(100);
   analogWrite(fanPin, 255);
   delay(100);
   
   }

}