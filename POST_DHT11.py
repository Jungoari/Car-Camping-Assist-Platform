import requests
import json

# Attempt to import Adafruit_DHT; if unavailable, set flag
try:
    import Adafruit_DHT
    DHT_AVAILABLE = True
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
except ModuleNotFoundError:
    DHT_AVAILABLE = False
    print("⚠️ Adafruit_DHT 라이브러리가 설치되어 있지 않습니다. 설치 후 다시 시도하세요.")

url = 'http://203.253.128.177:7579/Mobius/IoTPL_2/dht'
headers =	{
				'Accept':'application/json',
				'X-M2M-RI':'12345',
				'X-M2M-Origin':'IoTPL_2',
				'Content-Type':'application/vnd.onem2m-res+json; ty=4'
			}

# 센서 안정화를 위해 3초 대기 (전원 연결 직후 안정화 시간)
print("센서 안정화를 위해 3초 대기 중…")
import time
time.sleep(3)

while True:
    # Read temperature and humidity from DHT sensor
    if not DHT_AVAILABLE:
        exit(1)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        temp_val = int(round(temperature))
        humid_val = int(round(humidity))
        data = {
            "m2m:cin": {
                "con": f"{temp_val},{humid_val}"
            }
        }
        r = requests.post(url, headers=headers, json=data)
        try:
            r.raise_for_status()
            print(json.dumps(r.json(), indent=2))
        except Exception as exc:
            print('There was a problem: %s' % (exc))
    else:
        print("Failed to retrieve data from DHT sensor")
    # 1분 대기 후 다음 읽기
    time.sleep(60)
