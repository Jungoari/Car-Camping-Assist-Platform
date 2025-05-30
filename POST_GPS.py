import serial
import requests
import time

# DMM → Decimal Degree 변환 함수
def dmm_to_decimal(dmm, direction):
    degrees = int(float(dmm) / 100)
    minutes = float(dmm) - degrees * 100
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

# Mobius 정보
MOBIUS_URL = 'http://203.253.128.177:7579/Mobius/IoTPL_2/GPS'
HEADERS = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'SBvrw2zjvJsW',  # 사용자 AE-ID
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
}

# 시리얼 포트 초기화
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        
        # 유효한 문장 필터
        if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
            parts = line.split(',')

            # 위도/경도 위치 파싱
            if line.startswith('$GPGGA') and len(parts) > 5:
                lat, lat_dir = parts[2], parts[3]
                lon, lon_dir = parts[4], parts[5]
            elif line.startswith('$GPRMC') and len(parts) > 6:
                lat, lat_dir = parts[3], parts[4]
                lon, lon_dir = parts[5], parts[6]
            else:
                continue

            # 값이 비어있지 않으면 변환
            if lat and lon and lat_dir and lon_dir:
                try:
                    lat_dd = dmm_to_decimal(lat, lat_dir)
                    lon_dd = dmm_to_decimal(lon, lon_dir)
                    print(f"위도: {lat_dd:.6f}, 경도: {lon_dd:.6f}")

                    # Mobius에 보낼 데이터 준비
                    payload = {
                        "m2m:cin": {
                            "con": f"{lat_dd:.6f},{lon_dd:.6f}"
                        }
                    }

                    # HTTP POST 요청 전송
                    response = requests.post(MOBIUS_URL, headers=HEADERS, json=payload)
                    response.raise_for_status()
                    print("✅ 전송 완료:", response.status_code)

                    # 다음 전송을 위해 잠깐 대기
                    time.sleep(5)

                except Exception as e:
                    print(f"⚠️ 변환 또는 전송 중 오류: {e}")
except KeyboardInterrupt:
    print("종료합니다.")
finally:
    ser.close()