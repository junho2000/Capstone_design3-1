#include <SPI.h>   // 온도센서-SPI통신
#include "Adafruit_MAX31855.h"   // 온도센서 라이브러리(아두이노 IDE에서 다운)
#include <LiquidCrystal_I2C.h>  // LCD패널 라이브러리(아두이노 IDE에서 다운)
#include <SoftwareSerial.h> 
// 온도센서 SO핀
#define SO 2  
// 온도센서 CS핀
#define CS 3  
// 온도센서 CK핀
#define SCK 4 
// LED
#define LED 5   
// 부저
#define BUZZ_PIN 6   
// 릴레이
#define relay 7   

// L298N [SZH-MDBL-020] 모터드라이버
#define Dir1Pin_A 8 // 방향제어 핀 1
#define Dir2Pin_A 9 // 방향제어 핀 2
#define MotorPin 12  // 모터 제어&속도제어 핀

// MAX6675 온도센서
Adafruit_MAX31855 thermocouple(SCK, CS, SO); 

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // RX, TX

// LCD 패널: I2C 주소와 LCD 크기 설정
LiquidCrystal_I2C lcd(0x27, 16, 2); 

void buzz() 
{   
   analogWrite(BUZZ_PIN, 5000);
   delay(300);
   analogWrite(BUZZ_PIN, 0);
   delay(50);
}

void setup() 
{
  lcd.begin(16, 2); // LCD 초기화
  lcd.init();
  lcd.backlight(); // 백라이트 활성화

  //시리얼 통신 시작
  Serial.begin(9600);
  //zigbee 통신 시작
  zigbeeSerial.begin(9600);

  pinMode(LED, OUTPUT); 
  pinMode(BUZZ_PIN, OUTPUT);  
  pinMode(relay, OUTPUT); 
  pinMode(Dir1Pin_A, OUTPUT);
  pinMode(Dir2Pin_A, OUTPUT);
  pinMode(MotorPin, OUTPUT);

  //온도센서
  Serial.print("MAX6675 온도센서");

  if (!thermocouple.begin()) 
  {
    Serial.print("ERROR.");
    while (1) delay(10);
  }

  Serial.print("MAX6675 온도센서 Done");
}

void loop() 
{
  // 현재 온도
  double f = thermocouple.readCelsius();
  double c = (f-32) * 5 / 9;  //섭씨

  if (isnan(f)) 
  {
    Serial.println("Thermocouple fault(s) detected!");
    uint8_t e = thermocouple.readError();
  } 
   
  else 
  {
    Serial.print("현재 배터리 온도: ");
    Serial.println(c);
    lcd.print("현재 배터리 온도: ");  //LCD패널에 현재 온도 표시
    lcd.print(c);
  }

  delay(1000);

  //비정상적인 온도 감지
  if(c < 18)
   {
     Serial.print("low temp");
     Serial.println(c);
     // 배터리 온도 비정상 신호, 현재 온도
     zigbeeSerial.print("low temp");
     //zigbeeSerial.print("temp: ");
     //zigbeeSerial.print(c);

     analogWrite(MotorPin, 0);
     digitalWrite(relay, HIGH);
     Serial.println("모터 OFF 히터 ON");
     digitalWrite(LED, HIGH);
     buzz();
   }

   else if(c > 23)   
   { 
     Serial.print("high temp");
     Serial.println(c);
     // 배터리 온도 비정상 신호, 현재 온도
     zigbeeSerial.print("high temp");
     //zigbeeSerial.print("temp: ");
     //zigbeeSerial.print(c);

     analogWrite(MotorPin, 255);
     digitalWrite(relay, LOW);
     Serial.println("모터 ON 히터 OFF");
     digitalWrite(LED, HIGH);
     buzz();
   }

   else   // 배터리 온도 정상
   {
     analogWrite(MotorPin, 0);
     digitalWrite(relay, LOW);
     digitalWrite(LED, LOW);
     analogWrite(BUZZ_PIN, 0);
   }
}
