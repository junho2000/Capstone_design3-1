# 라즈베리파이를 이용한 교통안전 통합 솔루션

## 개요
기존 시스템은 대부분 자동차사고 발생 시 운전자 또는 제3자가 직접 전화로 신고하는 시스템입니다.
이러한 시스템은 개별 운전자의 사고에 대해서 조기 예측 및 즉각 대응이 쉽지 않아 골든 타임을 놓칠 가능성이 있습니다. 또한 사건 발생 시 즉각적인 정보공유가 힘들어 출동 지연 및 혼란을 발생시킬 수 있습니다.

이러한 시스템은 개별 운전자의 사고에 대해서 조기 예측 및 즉각 대응이 쉽지 않아 골든 타임을 놓칠 가능성이 있습니다. 또한 사건 발생 시 즉각적인 정보공유가 힘들어 출동 지연 및 혼란을 발생시킬 수 있습니다.
국민 자동차 안전 솔루션팀은 이러한 현재 시스템을 넘어 통합 시스템을 제시합니다. 통합 시스템은 V2X를 통해 차량내 다양한 iot센서를 활용해 수집된 데이터를 통합적으로 분석하여 개별 운전자의 위험상황 조기 예측 및 즉각적인 대응을 가능하게 해줍니다.

## 코드 설명
### 1. alcohol_detect.ino

#### 설명
사용장비 : MQ-3 아두이노 알코올 센서 모듈 [SZH-SSBH-045], XB24CZ7WIT-004 지그비 모듈, 아두이노 우노, 아두이노 (Arduino) 호환 XBee 쉴드 XBee Shield 3.0

두 개의 알코올 센서값의 평균이 임계값인 300을 넘으면 알코올을 감지하도록 구성했음.

감지했을 경우 LED와 부저로 운전자에게 경고를 한 후, Zigbee통신으로 서버인 라즈베리파이에 'alcohol'신호 전송함.

```c
#include <SoftwareSerial.h>
...
SoftwareSerial zigbeeSerial(10, 11);  // ZigBee 모듈을 연결할 시리얼 핀 설정, TX, RX을 10번 11번 핀에 할당한다.
...
zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작 바우드레이트 9600
...
zigbeeSerial.print("alcohol"); // 라즈베리파이 서버에 alcohol이라는 신호를 보냄
```

#### 시행착오 및 문제해결 방법
알코올 센서가 조금 민감하게 반응해서 한번 감지가 되면 여러번 감지가 됐음. 또한 라즈베리파이 서버에서 1초마다 수신 받도록 했기 때문에 코드 마지막에 delay(2000);을 추가해 경고가 계속울리지 않고 정상적으로 라즈베리파이 서버에 수신하도록 했음.

### 2. fire_detect.ino

#### 설명
사용장비 : [SMG-A] 불꽃 감지 센서 모듈 [ONE025], [SMG] MQ-135 아두이노 유해가스/공기질 센서 모듈 [SZH-SSBH-038], XB24CZ7WIT-004 지그비 모듈, 아두이노 우노, 아두이노 (Arduino) 호환 XBee 쉴드 XBee Shield 3.0

두 개의 유해가스/공기질 센서값의 평균이 임계값인 17을 넘으면 알코올을 감지 또는 하나의 불꽃 감지 센서 모듈이 불꽃을 감지하면 각각 2개의 LED와 하나의 부저로 운전자에게 경고를 한 후, Zigbee통신으로 서버인 라즈베리파이에 'fire'신호 전송함.

```c
#include <SoftwareSerial.h>
...

SoftwareSerial zigbeeSerial(10, 11);  // ZigBee 모듈을 연결할 시리얼 핀 설정, TX, RX을 10번 11번 핀에 할당한다.
int flame_state = 0; // 불꽃센서가 감지하면 0을 반환함
const int threshold = 17; // 화재 감지를 위한 임계값
...

zigbeeSerial.begin(9600);   // ZigBee 모듈 시리얼 통신 시작 바우드레이트 9600
...

zigbeeSerial.print("fire"); // 라즈베리파이 서버에 fire 이라는 신호를 보냄
```

#### 시행착오 및 문제해결 방법
유해가스/공기질 센서를 하루이상 미리 데워놓아야한다고해서 전날 센서를 6시간 정도 써보고 센서를 꺼놓음. 대회 당일 미리 데우지 않고 사용했지만 감지가 잘됐음. 또한 
이 센서를 사용하기 위해서는 밀폐된 공간에 가스를 넣어줘야 수치가 빠르게 올라갔음. 평소에는 11 ~ 13 정도의 수치를 유지하다 1분정도 밀폐된 상자에 가스를 넣어주면 17 ~ 20정도로 올라갔음. 

불꽃 감지 센서는 불꽃이 가까이 있어야 감지됐음. 또한 감지각을 벗어나면 감지가 안됐음.


### 3. drowsy_detect.py
#### 설명
사용장비 : LOGITECH STREAMCAM, 라즈베리파이 8gb ram (rasbian 64bit), 모니터

One Millisecond Face Alignment with an Ensemble of Regression Trees 논문에 나온 방법으로 얼굴에 특징점을 뽑아 눈 위아래에 있는 두점들의 두쌍의 2-norm의 크기를 이용해 눈을 감았을 때, 눈은 반쯤 감았을 때, 눈을 완전히 감았을 때를 감지함. 

sql 관련 설명은 아래 4번 코드에서 설명하도록 하겠음.

- [YouTube 영상](https://www.youtube.com/watch?v=ksi42rwGyas)
- [Github 링크](https://github.com/infoaryan/Driver-Drowsiness-Detection)
이 링크에서 코드를 가져와 졸음을 감지했음. 하지만 동양인의 눈의 크기와 저자의 눈의 크기가 다르기 때문에 비율을 조정해줘야 했음. 아래 코드가 조정된 비율임.

```python
def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)

	#Checking if it is blinked
	if(ratio>0.24):
		return 2 #active
	elif(ratio>0.2 and ratio<=0.4):
		return 1 #drowsy 경고
	else:
		return 0 #sleep 경고
...

if y1 + y1 > h//3*2:
  cv2.putText(face_frame, "Head up!", (300,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)
```

#### 시행착오 및 문제해결 방법
이 코드를 실행하기 위해선 shape_predictor_68_face_landmarks.dat파일이 같은 경로안에 있어야함.

코드를 실행하면 가끔 라즈베리파이 안에서 돌아가지 못할 때가 있었음
1. 라즈베리파이가 충분히 신호가 강한 인터넷에 연결되지 않았을 경우 sql에 데이터를 넣을 수 없어서 파일이 중간에 멈췄음. 신호가 약하면 화면이 멈췄음.
2. 라즈베리파이가 심하게 과열되었을 경우 정상적으로 작동하던 코드가 갑자기 작동이 안될 때가 있었음.

웹캠을 킨 라즈베리파이에 VNC를 이용해 접근할려 했지만 계속 검은 화면이 나왔음. 이 문제를 해결 할 수 없었기 때문에 따로 모니터를 사용했음.


### 4. rasp_zigbee_coordinator.py
#### 설명
사용장비 : XB24CZ7WIT-004 지그비 모듈, 라즈베리파이 4gb ram (rasbian 32bit)

이 코드는 위에 1,2 번 코드로부터 지그비 통신으로 fire, alcohol 신호를 받으면 sql 서버에 올림. 이때 3번 코드는 라즈베리파이에 웹캠이 연결되어 형식이므로 직접 sql서버에 데이터를 넣음.

#### a. 지그비 통신
지그비 통신을 사용하기 위해선 먼저 XCTU를 설치해 지그비 모듈마다 따로 설정을 해줘야한다. 각 지그비 모듈을 송신 장치로 쓸건지 아니면 수신 장치로 쓸건지 설정을 할 수 있음. 기타 자세한 사항은 아래 링크를 따라하면 된다. 이때 따로 지그비 어댑터가 필요하지 않다. 만약 라즈베리파이 GPIO핀과 지그비랑 연결할 수 있는 선만 있으면 설정할 수 있음.
- [YouTube 링크](https://www.youtube.com/watch?v=oWKUBBdtUFU)

아두이노와는 달리 라즈베리파이에서는 기본 tx rx핀이 블루투스 통신으로 고정 할당되어 있으므로 고정을 해제하거나 다른 핀을 tx, rx핀으로 사용해야했음. 그래서 uart3을 활성화해 4번 5번 핀을 tx, rx 핀으로 활용했음. 아래는 참고한 블로그 글임. 만약 수신이 제대로 안된다면 tx, rx핀을 반대로 꼽았을 가능성이 매우 큼.
- [Github 링크](https://m.blog.naver.com/emperonics/222039301356)

```python
#지그비 설정
xbee = serial.Serial()
xbee.port = "/dev/ttyAMA1" #uart3을 사용하게되면 /dev/ttyAMA1이 열림
xbee.baudrate = 9600 #아두이노와 같은 바우드레이트 설정
#1초마다 수신
xbee.timeout = 1
xbee.writeTimeout = 1

#신호를 받는 코드, 라즈베리파이에서는 수정했지만 github에선 아직 수정안됨. 
#신호받은 줄에 fire이나 alcohol이 포함되어 있을 경우 sql 테이블에 넣음
data = xbee.readline().strip()

if data == b'fire':
  fire_alert = 1
            
if data == b'alcohol':
  alcohol_alert = 1
  
```
#### a. sql 데이터 베이스 사용

관련 설명...

```python
# aws rds를 이용해 데이터베이스를 열어 인터넷이 연결되어 있으면 어떠한 ip로도 sql에 접근할 수 있도록 설정
connection = pymysql.connect(host='ip', port=3306, user='id', passwd='pwd', db='db name')
cursor = connection.cursor()
  
```
#### 시행착오 및 문제해결 방법
지그비 통신으로 데이터를 수신 받으면 1초에 한줄 씩 받으므로 
```python
data = xbee.readline().strip()

if data == b'fire':
  fire_alert = 1
            
if data == b'alcohol':
  alcohol_alert = 1
```
이런식으로 받거나 1초안에 연속된 신호들을 계속 받게되면 수신이 제대로 작동하지 않음. -> 해결

sql에 데이터를 넣을 때 10번 까지 밖에 들어가지 않음. -> cursor.execute("SELECT MAX(CAST(MarkerID AS UNSIGNED)) FROM person") 해결

### 5. mysql_with_tkinter.py

관리자 한명이 실시간으로 통합적으로 볼 수 있는 GUI화면. 

라이브러리 사용
import customtkinter
from tkintermapview import TkinterMapView

버튼 하나하나 설명 + 데이터 테이블 설명
