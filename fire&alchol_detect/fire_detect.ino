#include <SoftwareSerial.h>

//공기질 센서에서 받은 값이 임계값을 넘었을 경우, 불꽃 감지 센서 감지됐을 경우 LED를 키고 부저를 울리며 지그비모듈로 fire신호를 보냄

#define MQ135_PIN1 A0
#define MQ135_PIN2 A1
#define BUZZ = 6
#define FLAME_SENSOR_PIN1 7
#define FLAME_SENSOR_PIN2 8
#define LED 13
#define AIR_QUALITY_THRESHOLD 200 // 공기질 임계값
#define FLAME_THRESHOLD 500		  // 불꽃 감지 임계값

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // RX, TX

void setup()
{
	zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작
	pinMode(FLAME_SENSOR_PIN1, INPUT);
	pinMode(FLAME_SENSOR_PIN2, INPUT);
	pinMode(LED, OUTPUT);
}

void buzer()
{
	analogWrite(BUZZ, 50);
	delay(300);
	analogWrite(BUZZ, 0);
	delay(50);
}

void loop()
{
	digitalWrite(LED, LOW);
	// 공기질 데이터 수집
	int airQualityValue1 = analogRead(MQ135_PIN1);
	int airQualityValue2 = analogRead(MQ135_PIN2);
	

	int mean_air = (airQualityValue1 + airQualityValue2) / 2;

	if (mean_air > AIR_QUALITY_THRESHOLD)
	{
		// 시리얼 통신을 통해 공기질 데이터 보내기
		digitalWrite(LED, HIGH);
		zigbeeSerial.print("fire"); //상황
		buzer()
	}

	// 불꽃 감지
	int flameValue1 = digitalRead(FLAME_SENSOR_PIN1);
	int flameValue2 = digitalRead(FLAME_SENSOR_PIN2);

    int mean_flame = flameValue1 & flameValue2;

	if (mean_flame == HIGH) {
		// 시리얼 통신을 통해 불꽃 감지 여부 보내기
		digitalWrite(LED, HIGH);
		zigbeeSerial.print("fire"); //상황
		buzer()
	}

	delay(1000); // 일정 시간 간격으로 반복 실행
}
