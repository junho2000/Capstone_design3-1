#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

// ZigBee 모듈을 연결할 시리얼 핀 설정
SoftwareSerial zigbeeSerial(10, 11);  // RX, TX
LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C 주소와 LCD 크기 설정
int sw = 0;
int flag = 0;
int barLength = 16;
int value = 0;
float cycle = 0;

void setup() {
  lcd.begin(16, 2); // LCD 초기화
  lcd.init();
  lcd.backlight(); // 백라이트 활성화
  Serial.begin(9600);
  zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작
  pinMode(13, INPUT);  // 내부 풀업 저항 사용
}

float calcDoD(int x){
  return 1 / (98105 * pow(x, -1.138)) * 100; //한번에 100번 충전한다고 가정
  
}
  
void loop() {
  value = analogRead(A0);  // 가변 저항의 값을 읽음
  int barValue = map(value, 0, 1023, barLength, 0);  // 가변 저항의 값을 바 그래프의 길이로 변환
  int perValue = map(value, 0, 1023, 0, 100);  // 가변 저항의 값을 바 그래프의 길이로 변환
  
  sw = digitalRead(13);
  if(sw) {cycle += calcDoD(perValue); Serial.println(sw);  sw = 0; delay(500);}  
  
 
  
  // 첫 번째 줄에 가변 저항의 값 출력
  lcd.setCursor(0, 0);
  lcd.print("DoD:");
  lcd.print(perValue);
  lcd.print("Cycle:");
  lcd.print(cycle);
  lcd.print("           ");  // 숫자를 지우기 위해 공백 출력
  
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
  if (cycle >= 1) //배터리 교체 신호
  {
    zigbeeSerial.print("cycle");
   	delay(2000); 
  }
}