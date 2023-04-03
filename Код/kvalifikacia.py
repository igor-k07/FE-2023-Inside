import cv2, time
import RobotAPI as rapi
import numpy as np
import serial
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)
port = serial.Serial('/dev/ttyS0', baudrate = 115200, stopbits=serial.STOPBITS_ONE)
##
fps = 0
fps1 = 0
fps_time = 0
btntime = time.time()
dl=0
dr=0
xz=0
yz=0
line= 'None'
colorz="None"
inn = ''
speed = 0
servo = 0
rgb = '010'
btn = 1
eold=1
line_orange, line_blue = 0, 0

black_hsv_low = [0, 47, 0]
black_hsv_up = [71,245, 73]
##
lowr=np.array([0,168,92])
upr=np.array([7,212,255])

lowg=np.array([ 73, 90,  55])
upg=np.array( [ 83, 255, 102])

lowor = np.array([0, 81, 64])
upor = np.array([37, 167, 255])

lowblue = np.array([100, 0, 0])
upblue = np.array([180, 255, 255])

lowblack= np.array([0, 0, 0])
upblack = np.array([180, 150, 50])

def telemetria(frame):
     global fps, xz,yz,line,dl,dr,colorz,servo

     cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 0), -1)
     cv2.putText(frame, str("sp=") + str(speed), (0,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("fps=") + str(fps), (0, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("l_b=") + str(line_blue), (0, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("dl=") + str(dl), (100, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("dr=") + str(dr), (100, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("colorz=") + str(colorz), (190, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("ser=") + str(int(servo)), (190, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)

     cv2.putText(frame, str("xz=") + str(xz), (360, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("yz=") + str(yz), (360, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("line=") + str(line), (480, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("button=") + str(btn), (480, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)

# def datz(frame):
#      global lowr,upr,lowg,upg,colorz, xz,yz
#      colorz = "None"
#      dz=frame[200:330, 100:540]
#      #green
#
#      hsv = cv2.cvtColor(dz, cv2.COLOR_BGR2HSV)
#      maskg = cv2.inRange(hsv, lowg, upg)
#
#      imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(maskg,(3,3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#      w_g = 0
#      h_g = 0
#      x_g = 0
#      y_g = 0
#      for contorb1 in contoursd1:
#           x, y, w, h = cv2.boundingRect(contorb1)
#           if w * h > 400 and  y+h > y_g+h_g:
#               w_g=w
#               h_g=h
#               x_g = x
#               y_g = y
#      #red
#
#      maskr = cv2.inRange(hsv, lowr, upr)
#      imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(maskr,(3,3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#      w_r = 0
#      h_r = 0
#      x_r = 0
#      y_r = 0
#      for contorb1 in contoursd1:
#           x, y, w, h = cv2.boundingRect(contorb1)
#           if w * h > 400 and y+h > y_r+h_r:
#                w_r = w
#                h_r = h
#                x_r = x
#                y_r = y
     # if h_r>0 and h_g>0:
     #      if y_r+h_r>y_g+h_g:
     #           colorz = "red"
     #           cv2.rectangle(dz, (x_r, y_r), (x_r + w_r, y_r + h_r), (0, 255, 0), 2)
     #           xz=x_r+w_r//2
     #           yz=y_r+h_r//2
     #      else:
     #           colorz = "green"
     #           cv2.rectangle(dz, (x_g, y_g), (x_g + w_g, y_g + h_g), (0, 0, 255), 2)
     #           xz = x_g + w_g // 2
     #           yz = y_g + h_g // 2
     # else:
     #      if h_r>0:
     #           colorz = "red"
     #           cv2.rectangle(dz, (x_r, y_r), (x_r + w_r, y_r + h_r), (0, 255, 0), 2)
     #           xz = x_r + w_r // 2
     #           yz = y_r + h_r // 2
     #      if h_g>0:
     #           colorz = "green"
     #           cv2.rectangle(dz, (x_g, y_g), (x_g + w_g, y_g + h_g), (0, 0, 255), 2)
     #           xz = x_g + w_g // 2
     #           yz = y_g + h_g // 2
     #
     # cv2.rectangle(frame, (100, 200), (540, 330), (0, 0, 0), 2)

def dlz(frame):
     global dl
     dblz = frame[250:370, 0:150]
     hsv = cv2.cvtColor(dblz, cv2.COLOR_BGR2HSV)
     mask_black = cv2.inRange(hsv, lowblack, upblack)
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_black, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     x1, y1, h1, w1 = 0, 0, 0, 0
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          a1 = cv2.contourArea(contorb1)
          if x + w > x1 + w1 and a1>100:
               x1, w1, y1, h1 = x, w, y, h

     dl = x1 + w1
     cv2.rectangle(dblz, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
     cv2.rectangle(frame, (0, 250), (150, 370), (255, 0, 0), 2)

def drz(frame):
     global dr
     drlz  = frame[250:370, 490:640]
     hsv = cv2.cvtColor(drlz, cv2.COLOR_BGR2HSV)
     mask_black = cv2.inRange(hsv, lowblack, upblack)
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_black, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     x1, y1, h1, w1 = 150, 0, 0, 0
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          a1 = cv2.contourArea(contorb1)
          if 150-x > 150-x1 and a1 > 100:
               x1, w1, y1, h1 = x, w, y, h

     dr = 150-x1
     cv2.rectangle(drlz, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
     cv2.rectangle(frame, (490, 250), (640, 370), (255, 0, 0), 2)

def p():
     global dr, dl, servo, eold
     e = dl-dr
     k = 0.2
     servo=k*e+0.2*(e - eold)
     eold=e
     if servo>60:
          servo=60
     if servo<-60:
          servo=-60

def dlin(frame):
     global lowor, upor, line,upblue,lowblue, line_orange, line_blue
     x, y, w, h = 0, 0, 0, 0
     linz=frame[410:430,295:345]
     line = 'None'
     hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
     mask_orange = cv2.inRange(hsv, lowor, upor)
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          if w * h>200:
               # line_orange += 1
               line = 'orange'
     # blue
     mask_blue = cv2.inRange(hsv, lowblue, upblue)
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          if w * h > 200:
               line = 'blue'
               line_blue += 1
     cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
     cv2.rectangle(frame, (295, 410), (345, 430), (0, 0, 0), 2)

while True:
     fps1 += 1
     if time.time() > fps_time + 1:
          fps_time = time.time()
          fps = fps1
          fps1 = 0

     frame = robot.get_frame(wait_new_frame=1)
     dlin(frame)
     dlz(frame)
     drz(frame)
     # datz(frame)
     if speed>0:
          p()
     else:
          servo=0
     telemetria(frame)


     message = str(int(speed) + 200) + str(int(servo) + 200) + rgb + '$'
     port.write(message.encode('utf-8'))
     if port.in_waiting > 0:
          t = time.time()
          while True:
               a = str(port.read(), 'utf-8')
               if a != '$':
                    inn += a
               else:
                    break
          btn = inn
          inn = ''
          if t + 0.02 < time.time():
               break
     port.reset_input_buffer()

     if btn == '0' and btntime+1 < time.time():
          btntime = time.time()
          if speed==0:
               speed=30
          else:
               speed=0

     robot.set_frame(frame,40)

