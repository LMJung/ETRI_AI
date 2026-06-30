# ble_drive_8way.py  ----  블루투스 명령으로 메카넘 8방향 주행
from time import sleep, ticks_ms, ticks_diff
import ble_library
import bluetooth
from ai_ponybot import i2c, PonyMotor

motor = PonyMotor(i2c)

ble = bluetooth.BLE()
p = ble_library.BLESimplePeripheral(ble, 'ESP-KJI')

# 키패드 배치:  7 8 9 / 4 5 6 / 1 2 3
#   8=전진 2=후진 4=좌횡 6=우횡 9=앞우 7=앞좌 3=뒤우 1=뒤좌 5=정지
CMD = {
    # 숫자(키패드) 그대로
    '8':8, '2':2, '4':4, '6':6, '9':9, '7':7, '3':3, '1':1, '5':5,
    # 영어 약어/단어
    'F':8, 'FWD':8, 'FORWARD':8,
    'B':2, 'BACK':2, 'BACKWARD':2,
    'L':4, 'LEFT':4,
    'R':6, 'RIGHT':6,
    'FR':9, 'FL':7, 'BR':3, 'BL':1,
    'S':5, 'STOP':5,
}
NAME  = {8:'FWD',2:'BACK',4:'LEFT',6:'RIGHT',9:'F-R',7:'F-L',3:'B-R',1:'B-L',5:'STOP'}
SPEED = 60          # 기본 속도 (명령에 ",속도"를 붙이면 변경)

# 앞뒤가 반대로 움직이면 True (좌횡·우횡은 그대로, 앞뒤·대각선 앞뒤만 교정)
INVERT_FB = True
FB_SWAP = {8:2, 2:8, 9:3, 3:9, 7:1, 1:7, 4:4, 6:6, 5:5}

last_cmd = ticks_ms()

def on_rx(v):
    global last_cmd
    data = v.strip().upper()
    if not data:
        return
    # "8" / "8,80" / "F:80" 형식 허용 (속도 옵션)
    spd = SPEED
    for sep in (',', ':'):
        if sep in data:
            data, s = data.split(sep, 1)
            s = s.strip()
            if s.isdigit():
                spd = max(0, min(100, int(s)))
            break
    data = data.strip()

    code = CMD.get(data)
    if code is None:
        print("알 수 없는 명령:", data)
        return

    drive_code = FB_SWAP[code] if INVERT_FB else code
    if drive_code == 5:
        motor.mecanum(5)
    else:
        motor.mecanum(drive_code, spd)
    last_cmd = ticks_ms()
    print("CMD:%-4s -> %-5s spd:%d" % (data, NAME[code], spd))

p.on_write(on_rx)

print("BLE 8방향 제어 대기... (기기명 ESP-KJI)")
print("보낼 명령 예: 8 / FWD / 9 / FR / 6,80 / STOP")

while True:
    # 연결이 끊기면 안전을 위해 정지
    if not p.is_connected():
        motor.mecanum(5)
    sleep(0.1)
