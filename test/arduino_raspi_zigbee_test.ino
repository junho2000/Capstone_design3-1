#include <SoftwareSerial.h>

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // TX, RX

void setup() {
  zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작
}

void loop() {
  // 데이터 송신
  zigbeeSerial.print("Hello, ZigBee!");  // ZigBee 모듈로 데이터 전송
  
  // 송신 후 대기 시간 설정
  delay(1000);  // 1초 대기
}