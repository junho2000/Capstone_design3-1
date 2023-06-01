// 필요한 라이브러리를 포함합니다.
#include <SoftwareSerial.h>

// 핀 번호를 정의합니다.
#define MQ135_PIN1 A0
#define MQ135_PIN2 A1
#define BUZZ_PIN 6
#define FLAME_SENSOR_PIN 7
#define LED1 13
#define LED2 12
#define FLAME_THRESHOLD 500

SoftwareSerial zigbeeSerial(10, 11);
int flame_state = 0; // 감지하면 0
int air_state = 0;



// 임계값을 설정합니다.
const int threshold = 17; // 화재 감지를 위한 임계값

void setup() {
  // 시리얼 통신을 설정합니다.
  Serial.begin(9600);
  zigbeeSerial.begin(9600);
  pinMode(MQ135_PIN1, INPUT);
  pinMode(MQ135_PIN2, INPUT);
  pinMode(FLAME_SENSOR_PIN, INPUT);
  pinMode(LED1, OUTPUT); // 공기질
  pinMode(LED2, OUTPUT); // 불꽃
  pinMode(BUZZ_PIN, OUTPUT);
}

void buzz()
{
  analogWrite(BUZZ_PIN, 50);
  delay(300);
  analogWrite(BUZZ_PIN, 0);
  delay(50);
}

void loop() {
  // 두 개의 센서 값을 읽어옵니다.
  flame_state=digitalRead(FLAME_SENSOR_PIN);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);

  int airQualityValue1 = analogRead(MQ135_PIN1);
  int airQualityValue2 = analogRead(MQ135_PIN2);

  // 센서 값을 시리얼 모니터에 출력합니다.
  Serial.print("Air Sensor Value 1: ");
  Serial.println(airQualityValue1);
  Serial.print("Air Sensor Value 2: ");
  Serial.println(airQualityValue2);
  
  // 두 센서 값의 평균을 계산합니다.
   int mean_air = (airQualityValue1 + airQualityValue2) / 2;

  // 평균 값이 임계값보다 크면 LED를 켭니다.
  if (mean_air > threshold) {
    digitalWrite(LED1, HIGH);
    buzz();
    zigbeeSerial.print("fire");
  }
  digitalWrite(LED1, LOW);

  if(flame_state == 0){
    digitalWrite(LED2, HIGH);
    buzz();
    zigbeeSerial.print("fire");
  }
  digitalWrite(LED2, LOW);
  // 잠시 대기합니다.
  delay(2000);
}