#include <SoftwareSerial.h>
#include <TinyGPS++.h>

//이미 zigbee 통신으로 인해 tx rx핀을 쓰고 있어서 GPS 모듈로 데이터를 못받을 수도 있음
//알코올 센서에서 받은 수치가 임계값보다 높을 경우 LED와 부저로 경고를 한 후 지그비모듈로 coordinator에 alcohol 신호를 보낸다
//아마 위도 경도는 못보낼 듯

#define RX_PIN 2
#define TX_PIN 3
#define BUZZ = 6
#define LED 13
#define ALCOHOL_SENSOR_PIN1 A0
#define ALCOHOL_SENSOR_PIN2 A1
#define THRESHOLD 500 // 알코올 수치 기준값

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // RX, TX

TinyGPSPlus gps;

void setup()
{
	zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작
	gpsSerial.begin(9600);
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
	// 알코올 수치 측정
	int alcoholValue1 = analogRead(ALCOHOL_SENSOR_PIN1);
	int alcoholValue2 = analogRead(ALCOHOL_SENSOR_PIN2);

    int mean = (alcoholValue1 + alcoholValue2) / 2;

	if (mean > THRESHOLD) {
		digitalWrite(LED, HIGH);
        zigbeeSerial.print("alcohol"); // 상황
		buzer()

        //gps 안되면 구현 안될 수도 있음
        while (gpsSerial.available() > 0)
		{
			if (gps.encode(gpsSerial.read())) {
				if (gps.location.isValid()) {
					// 알코올 수치와 GPS 데이터 시리얼 통신으로 보내기

					zigbeeSerial.print("alcohol"); // 상황
					zigbeeSerial.print(gps.location.lat(), 6); //위도
					zigbeeSerial.print(gps.location.lng(), 6); //경도
				}
			}
		}
	}

	delay(1000); // 일정 시간 간격으로 반복 실행
}