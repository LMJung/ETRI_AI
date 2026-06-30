# clap_dance.py  ----  실습 2 전체 코드
from ai_ponybot import i2c, PonyMotor, PonyOLED
from neopixel import NeoPixel
from machine import ADC, Pin
from time import sleep, ticks_ms, ticks_diff
import random

oled  = PonyOLED(i2c)
mic   = ADC(Pin(35)); mic.atten(ADC.ATTN_11DB)

THRESH = 1000

def sound_level():
    s = [mic.read() for _ in range(50)]
    return max(s) - min(s)




def calibrate(ms=1000):
    t0 = ticks_ms(); peak = 0
    while ticks_diff(ticks_ms(), t0) < ms:
        peak = max(peak, sound_level())
        sleep(0.01)
    return peak


MARGIN = 700                             # 주변보다 이만큼 커야 '박수' (덜 잡히면 ↓, 잡음 많으면 ↑)
WINDOW = 1500                            # 첫 박수 후 추가 박수를 받는 시간(ms)

ambient = calibrate()
THRESH = ambient + MARGIN                # 박수 인정 기준
REARM  = ambient + MARGIN // 3           # 이 아래로 떨어지면 다음 박수 받을 준비(히스테리시스)
print('ambient=%d  THRESH=%d  REARM=%d' % (ambient, THRESH, REARM))

# ---- ② 상승엣지 검출로 박수 세기 (첫 박수 후 WINDOW 동안) ----
def count_claps():
    # (1) 첫 박수를 기다린다 (소리 막대 표시)
    while True:
        lv = sound_level()
        #meter(lv)
        if lv > THRESH:
            break
        sleep(0.005)
    # (2) 첫 박수 등록 후, 창을 열고 추가 박수 카운트
    count = 1
    #blink()
    armed = False                        # 방금 큰 소리였으니 일단 잠금
    t0 = ticks_ms()
    while ticks_diff(ticks_ms(), t0) < WINDOW:
        lv = sound_level()
        if armed and lv > THRESH:        # 조용했다가 다시 커짐 = 상승엣지 = 박수
            count += 1
        #    blink()
            armed = False
        elif (not armed) and lv < REARM: # 충분히 조용해지면 재무장
            armed = True
        sleep(0.005)
    return count



print('박수로 춤을 지휘하세요!')
while True:
    n = count_claps()
    if n == 0:
        continue

    print('박수 개수: %d' % n )