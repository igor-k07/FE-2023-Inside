from pyb import delay, Pin, ADC, Timer
import pyb
from machine import UART

uart = UART(6, 115200, stop=1)
btn = Pin('Y7', Pin.IN, Pin.PULL_UP)
servo1 = pyb.Servo(1)
p1 = Pin('Y9')
in_b = Pin('Y10', Pin.OUT_PP)
in_a = Pin('Y11', Pin.OUT_PP)

l_r = Pin('Y5', Pin.OUT_PP)
l_b = Pin('Y4', Pin.OUT_PP)
l_g = Pin('Y3', Pin.OUT_PP)

in_a.high()
in_b.low()
tim = Timer(2, freq=10000)
ch1 = tim.channel(3, Timer.PWM, pin=p1)
inn = ''
speed = 0
serv = 10
servo1.angle(serv)
r = 0
g = 0
b = 0
f = 0


def rgb(r,g,b):
    if r == 1:
        l_r.low()
    else:
        l_r.high()

    if g == 1:
        l_g.low()
    else:
        l_g.high()

    if b == 1:
        l_b.low()
    else:
        l_b.high()


rgb(1,1,1)
start = False

while True:
    print(btn.value())
    if uart.any():
        a = chr(uart.readchar())
        if a != '$':
            inn += a
            if len(inn) > 10:
                inn = ''
        else:
            try:
                if len(inn) == 9:
                    if start == False:
                        rgb(0, 0, 0)
                        start = True
                    speed = int(inn[0:3]) - 200
                    serv = int(inn[3:6]) - 200 + 10
                    r = int(inn[6])
                    g = int(inn[7])
                    b = int(inn[8])
                    inn = ''
                    # print(speed, serv, r, g, b)
                    servo1.angle(serv)
                    ch1.pulse_width_percent(speed)
                    rgb(r,g,b)
                    uart.write(str(btn.value()) + '$')
            except ValueError:
                print('err')









