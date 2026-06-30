# ble_voice_drive.py  ----  음성 명령(Web Speech 웹앱) 수신 -> 포니봇 주행
#   웹앱이 보내는 명령: forward / backward / left / right / stop
#   ※ 웹앱이 'ESP-000'을 찾으므로 기기 이름을 반드시 'ESP-000'으로 둡니다.
from time import sleep
import ble_library
import bluetooth
from ai_ponybot import i2c, PonyMotor

motor = PonyMotor(i2c)

ble = bluetooth.BLE()
p = ble_library.BLESimplePeripheral(ble, 'ESP-KJI')   # ★ 웹앱 filter 이름과 일치

SPEED     = 60         # 주행 속도
INVERT_FB = False      # 앞뒤가 반대로 가면 True 로 바꾸세요

def on_rx(v):
    cmd = v.strip().lower()
    if not cmd:
        return

    if INVERT_FB:                      # 앞뒤 반전 보정
        if   cmd == 'forward':  cmd = 'backward'
        elif cmd == 'backward': cmd = 'forward'

    if   cmd == 'forward':
        motor.drive('forward', SPEED)
    elif cmd == 'backward':
        motor.drive('backward', SPEED)
    elif cmd == 'left':
        motor.drive('left', SPEED)     # 좌회전(제자리)
    elif cmd == 'right':
        motor.drive('right', SPEED)    # 우회전(제자리)
    elif cmd == 'stop':
        motor.drive('stop')
    else:
        print('알 수 없는 명령:', cmd)
        return
    print('CMD:', cmd)

p.on_write(on_rx)
print("음성 제어 대기 중... (기기명 ESP-KJI)")

while True:
    if not p.is_connected():
        motor.drive('stop')            # 연결 끊기면 안전 정지
    sleep(0.1)
