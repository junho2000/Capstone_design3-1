#include <SoftwareSerial.h>

#define BUZZ 6
#define LED 13
#define ALCOHOL_SENSOR_1 A0
#define ALCOHOL_SENSOR_2 A1
#define THRESHOLD 300 // 알코올 수치 기준값

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // RX, TX

void setup()
{
	zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작
	pinMode(LED, OUTPUT);
}

void buzer()
{
	analogWrite(BUZZ, 30);
	delay(300);
	analogWrite(BUZZ, 0);
	delay(50);
}

void loop()
{
  // 알코울 수치 측정
  int alcoholValue_1 = analogRead(ALCOHOL_SENSOR_1);
  int alcoholValue_2 = analogRead(ALCOHOL_SENSOR_2);

  int alcoholValue = (alcoholValue_1 + alcoholValue_2) / 2;

  if (alcoholValue > THRESHOLD) 
  {
    digitalWrite(LED, HIGH);
    buzer();
    zigbeeSerial.print("alcohol");
    digitalWrite(LED, LOW);
  }

  delay(2000);
}