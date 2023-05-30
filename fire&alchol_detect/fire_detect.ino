#define MQ135_PIN1 A0
#define MQ135_PIN2 A1
#define FLAME_SENSOR_PIN1 2
#define FLAME_SENSOR_PIN2 3
#define AIR_QUALITY_THRESHOLD 200 // 공기질 임계값
#define FLAME_THRESHOLD 500		  // 불꽃 감지 임계값

void setup()
{
	Serial.begin(9600);
	pinMode(FLAME_SENSOR_PIN, INPUT);
}

void loop()
{
	// 공기질 데이터 수집
	int airQualityValue1 = analogRead(MQ135_PIN1);
	int airQualityValue2 = analogRead(MQ135_PIN2);

	int mean_air = (airQualityValue1 + airQualityValue2) / 2;

	if (mean_air > AIR_QUALITY_THRESHOLD)
	{
		// 시리얼 통신을 통해 공기질 데이터 보내기
		Serial.print("fire alert!"); //상황
	}

	// 불꽃 감지
	int flameValue1 = digitalRead(FLAME_SENSOR_PIN1);
	int flameValue2 = digitalRead(FLAME_SENSOR_PIN2);

    int mean_flame = flameValue1 & flameValue2;

	if (mean_flame == HIGH) {
		// 시리얼 통신을 통해 불꽃 감지 여부 보내기
		Serial.print("fire alert!"); //상황
	}

	delay(1000); // 일정 시간 간격으로 반복 실행
}
