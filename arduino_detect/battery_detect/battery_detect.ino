#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // RX, TX
LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C 주소와 LCD 크기 설정
int sw, number_sw = 0;
int barLength = 16;
int value = 0;

void setup() {
  lcd.begin(16, 2); // LCD 초기화
  lcd.init();
  lcd.backlight(); // 백라이트 활성화
  zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작
  pinMode(13, INPUT_PULLUP);  // 내부 풀업 저항 사용
}



void loop() {
  value = analogRead(A0);  // 가변 저항의 값을 읽음
  int barValue = map(value, 0, 1023, barLength, 0);  // 가변 저항의 값을 바 그래프의 길이로 변환
  int perValue = map(value, 0, 1023, 100, 0);  // 가변 저항의 값을 바 그래프의 길이로 변환

  // 첫 번째 줄에 가변 저항의 값 출력
  lcd.setCursor(0, 0);
  lcd.print("Value: ");
  lcd.print(perValue);
  lcd.print("       ");  // 숫자를 지우기 위해 공백 출력
  // 두 번째 줄에 바 그래프 출력
  lcd.setCursor(0, 1);
  
  for (int i = 0; i < barLength; i++) {
    if (i < barValue) {
      lcd.print("#");
    } else {
      lcd.print(" ");
    }
  }
  
  if (perValue <= 10) //배터리 잔량 10퍼센트 이하
  {
    zigbeeSerial.print("battery");
   	delay(2000); 
  }
}
