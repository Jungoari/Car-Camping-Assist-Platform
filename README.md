# Car-Camping-Assist-Platform

라즈베리파이와 GPS모듈, 가스센서등을 사용하여 차박(Car Camping)에 필요한 서비스를 제공하는 IoT Platform 입니다.

본인은 차박(Car Camping)을 취미로 삼고 있으며, 다양한 환경에서 캠핑과 차박을 경험해왔습니다.
그 과정에서 겪은 불편함과 위험 요소들을 직접 해결하고자 이 프로젝트를 기획하고 개발하게 되었습니다.

## 1. 안전 확보를 위한 센싱
  겨울철 차박에서는 체온 유지를 위해 무시동 히터나 기타 난방 기기를 사용하는 경우가 많습니다. 하지만 차량이라는 밀폐된 공간의 특성상, 가스가 누출되면 질식이나 중독 사고로 이어질 수 있는 심각한 위험이 존재합니다.
  이를 방지하기 위해 MQ-2 가스 센서를 차량 내부에 설치하고, 측정된 데이터를 REST API를 통해 Mobius IoT Platform에 전송합니다. 위험 상황이 감지되면 인근 차량에 알림을 보내 즉각적인 대응이 가능하도록 설계하였습니다.

## 2. 고립된 환경에서의 물품 요청
   차박은 일반적으로 인적이 드문 야외나 오지에서 진행되는 경우가 많으며, 특히 야간에는 외부와의 접촉이 어렵고, 술을 마신 상태라면 이동조차 어려운 상황이 벌어질 수 있습니다.
   이를 해결하기 위해 NEO-6M GPS 모듈을 활용하여 자신의 위치를 정확히 파악하고, 인근 차량의 위치를 함께 서버에 공유합니다. 이 기능을 통해 주변에 있는 사람들과 안전하게 물품을 요청하거나 도움을 받을 수 있는 방법을 고안하였습니다.



---

## Used Hardware

| 구성품                 | 수량 |
|----------------------|------|
| Raspberry Pi 3       | 4EA  |
| Raspberry Pi Monitor | 2EA  |
| 5V LED Strip         | 2EA  |
| GAS Sensor MQ-2      | 2EA  |
| Buzzer               | 2EA  |
| GPS Module NEO-6M    | 2EA  |
| PIR Sensor HC-SR501  | 2EA  |

---

## System Architecture

![System Architecture](images/Architecture.png)

> 위 그림은 센서, 라즈베리파이, Mobius 서버 간의 통신 흐름 및 역할을 나타냅니다.

---

## Demonstration Video

![Demo](images/Demo_Video.mp4)  
[▶Watch Video](images/Demo_Video.mp4)

---

## Key Features

### 1. 안전 감지 및 경고 시스템 
차량 내에 설치된 가스 센서, PIR 센서, 온습도 센서를 통해 실시간으로 위험 요소를 감지합니다.
일산화탄소 농도가 일정 기준을 초과하거나 주변에서 지속적인 움직임이 감지되면 LED 및 부저로 즉각 경고를 발생시킵니다.
이 정보는 Mobius 서버에도 전송되어 주변 차량과 위험 상황을 공유할 수 있습니다.

### 2. GPS 기반 위치 전송 및 공유
NEO-6M GPS 모듈을 이용해 차량의 현재 위치를 실시간으로 파악하고 Mobius 서버에 전송합니다.
서버는 다른 차량의 위치도 함께 받아 사용자 간 위치 기반 정보 공유가 가능하도록 합니다.
이를 통해 주변 차량 간 상황 파악 및 협업이 용이해집니다.

### 3. 물품 요청 기능 
차량 내부의 버튼을 통해 사용자는 미리 설정된 물품을 간편하게 요청할 수 있습니다.
요청 정보는 Mobius에 전송되어, 주변 차량 사용자들이 실시간으로 요청 내역과 위치를 확인할 수 있습니다.
이를 통해 오지나 야간 상황에서도 필요한 물품을 빠르게 요청하고 전달받는 것이 가능합니다.

---

## Technology Stack

- Python 3
- Raspberry Pi OS
- Mobius oneM2M IoT Platform
- REST API (HTTP + JSON)

---

## Closing

본 프로젝트는 **실제 차박 환경을 고려한 IoT 플랫폼** 구축에 중점을 두었습니다.  
Developed by Choi.J, Kim.J, Seo.J, Chae.K - SCH Univ.

> 캠핑의 즐거움에 안전을 더하다.  
> **Car-Camping-Assist-Platform**

---
