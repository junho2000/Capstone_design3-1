#include <SoftwareSerial.h>

// 음주운전
#define BUZZ0 6 
#define LED_alcohol 13
#define ALCOHOL_SENSOR_1 A0
#define ALCOHOL_SENSOR_2 A1
#define BUZZ1 6
#define LED_fire 13
//차량화재
#define FLAME_SENSOR_PIN 7
#define MQ135_PIN1 A0
#define MQ135_PIN2 A1
#define THRESHOLD 300 // 알코올 수치 기준값
#define FLAME_THRESHOLD 17  

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // RX, TX

int flame_state = 0; // 감지하면 0
int air_state = 0;
int mean_air = 0;

void buzz_alcohol()
{
   analogWrite(BUZZ0, 30);
   delay(300);
   analogWrite(BUZZ0, 0);
   delay(50);
}

void buzz_fire()
{
   analogWrite(BUZZ1, 30);
   delay(300);
   analogWrite(BUZZ1, 0);
   delay(50);
}

void setup() 
{
  Serial.begin(9600);
  zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작
  pinMode(LED_alcohol, OUTPUT);
  pinMode(BUZZ0, OUTPUT);
  pinMode(MQ135_PIN1, INPUT); // 공기질1
  pinMode(MQ135_PIN2, INPUT); // 공기질2
  pinMode(FLAME_SENSOR_PIN, INPUT);
  pinMode(LED_fire, OUTPUT); 
  pinMode(BUZZ1, OUTPUT);
}

void loop()
{
  // 알코울 수치 측정
  int alcoholValue_1 = analogRead(ALCOHOL_SENSOR_1);
  int alcoholValue_2 = analogRead(ALCOHOL_SENSOR_2);
  
  // 센서 값의 평균
  int alcoholValue = (alcoholValue_1 + alcoholValue_2) / 2;
  
  // 차량화재
  flame_state=digitalRead(FLAME_SENSOR_PIN);
  digitalWrite(LED_fire, LOW);
  
  // 공기질센서
  int airQualityValue1 = analogRead(MQ135_PIN1);
  int airQualityValue2 = analogRead(MQ135_PIN2);

  Serial.print("Air Sensor Value 1: ");
  Serial.println(airQualityValue1);
  Serial.print("Air Sensor Value 2: ");
  Serial.println(airQualityValue2);
  
  // 두 센서 값의 평균을 계산합니다.
  mean_air = (airQualityValue1 + airQualityValue2) / 2;
  
  if (alcoholValue > THRESHOLD) 
  {
    digitalWrite(LED_alcohol, HIGH);
    buzz_alcohol();
    Serial.print("alcohol");
    zigbeeSerial.print("alcohol");
    digitalWrite(LED_alcohol, LOW);
  }
  
  // 평균 값이 임계값보다 크면 LED를 켭니다.
  if(mean_air > FLAME_THRESHOLD || flame_state == 0) 
  {
    digitalWrite(LED_fire, HIGH);
    buzz_fire();
    Serial.print("fire");
    zigbeeSerial.print("fire");
    digitalWrite(LED_fire, LOW);
  }
delay(2000);
}
