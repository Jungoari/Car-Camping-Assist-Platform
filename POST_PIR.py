import requests
import json
import sys
import time
import random

# 플랫폼 확인
if 'linux' in sys.platform:
    import RPi.GPIO as GPIO
    USING_PI = True
else:
    print("현재 라즈베리파이가 아니므로 GPIO 기능은 비활성화됩니다.")
    USING_PI = False

# PIR 센서 설정
if USING_PI:
    PIR_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    BUZZER_PIN = 27
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Mobius 설정
url = 'http://203.253.128.177:7579/Mobius/IoTPL_2/pir'
headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'SBvrw2zjvJsW',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
}

# 감지 시작
try:
    print("PIR 센서 감지 시작...")
    while True:
        if USING_PI:
            pir_value = GPIO.input(PIR_PIN)
        else:
            pir_value = random.choice([0, 0, 0, 1])  # 테스트용

        # 움직임 감지 시마다 전송
        if pir_value == 1:
            if USING_PI:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
            print(f"움직임 감지됨: {pir_value}")

            data = {
                "m2m:cin": {
                    "con": str(pir_value)
                }
            }

            r = requests.post(url, headers=headers, json=data)
            try:
                r.raise_for_status()
                print("데이터 전송 완료:")
                print(json.dumps(r.json(), indent=2))
            except Exception as exc:
                print('오류 발생: %s' % (exc))

        time.sleep(0.3)  # 빠른 감지를 위해 polling 간격 짧게

except KeyboardInterrupt:
    print("감지 중단됨")
finally:
    if USING_PI:
        GPIO.cleanup()