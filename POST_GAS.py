import requests
import RPi.GPIO as GPIO
import spidev
import time

# GPIO 핀 설정
LED_PIN = 21

# SPI 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 버스 0, 장치 0 (CE0)
spi.max_speed_hz = 1000000  # SPI 통신 속도 설정
ADC_CHANNEL = 0  # MQ-2 A0 핀 연결 채널 (MCP3008의 채널 0)

# Mobius 설정
MOBIUS_URL = 'http://203.253.128.177:7579/Mobius/IoTPL_2/GAS'
HEADERS = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'SBvrw2zjvJsW',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
}

def read_adc(channel):
    """spidev를 사용하여 MCP3008에서 ADC 값 읽기"""
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def send_mobius_alert():
    """DANGER 상태일 때만 Mobius에 경고 전송"""
    data = {
        "m2m:cin": {
            "con": "DANGER"
        }
    }
    try:
        response = requests.post(MOBIUS_URL, headers=HEADERS, json=data, timeout=5)
        response.raise_for_status()
        print("Mobius에 DANGER 전송 성공")
    except requests.exceptions.RequestException as e:
        print(f"Mobius 전송 실패: {e}")

def setup():
    """초기 설정: GPIO 및 SPI 초기화"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    print("Setup 완료")

def loop():
    """주요 루프: 센서 값 읽기, 상태 판단, Mobius 전송 및 LED 제어"""
    try:
        while True:
            raw_value = read_adc(ADC_CHANNEL)
            threshold = 800  # 임계값 설정

            if raw_value > threshold:
                print(f"DANGER 감지! RAW: {raw_value} (임계값 {threshold} 초과)")
                send_mobius_alert()

                blink_duration = 3
                blink_interval = 0.3
                start_time = time.time()
                print(f"LED 점멸 시작 ({blink_duration}초 동안)...")
                while (time.time() - start_time) < blink_duration:
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    time.sleep(blink_interval)
                    GPIO.output(LED_PIN, GPIO.LOW)
                    time.sleep(blink_interval)
                print("LED 점멸 종료.")

            else:
                print(f"현재 안전: RAW: {raw_value} (임계값 {threshold} 이하)")
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(3)

    except KeyboardInterrupt:
        print("\n프로그램 종료 요청 감지 (Ctrl+C).")
    finally:
        print("GPIO 및 SPI 리소스 해제 중...")
        spi.close()
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("리소스 해제 완료. 프로그램 종료.")

if __name__ == "__main__":
    setup()
    loop()