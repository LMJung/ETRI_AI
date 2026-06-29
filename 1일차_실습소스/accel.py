from machine import I2C, Pin
import mpu6050              # mpu6050.py 업로드 필요
from time import sleep

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
imu = mpu6050.accel(i2c, 0x69)   # 이 보드는 0x69
while True:
    v = imu.get_values()
    print('X', v['AcX'], 'Y', v['AcY'], 'Z', v['AcZ'])
    sleep(0.2)







