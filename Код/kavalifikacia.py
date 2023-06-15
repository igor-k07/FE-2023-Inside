#обьявление нужных библиотек
import cv2, time
import RobotAPI as rapi
import numpy as np
import serial
#Создаем обьект камеры
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)
port = serial.Serial('/dev/ttyS0', baudrate = 115200, stopbits=serial.STOPBITS_ONE)
#Обьявляем перемнные
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
circle = 0
direct = "None"
sum=0
stop_time=0
stop = [0,0,0,0]
dlm = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
drm = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
index=1
stop_flag=False
time_line = time.time()
time_stop = time.time()
max_servo = 50

fps = 0
fps1 = 0
fps_time = 0
#обьявляем массивы hsv для оранжевого голубого и черного

# lowor = np.array([7, 110, 64])
# upor = np.array([21, 255, 255])
lowor = np.array([7, 113, 140])
upor = np.array([28, 255, 255])

# lowblue = np.array([82, 63, 0])
# upblue = np.array([180, 255, 255])
lowblue = np.array([105, 98, 0])
upblue = np.array([180, 255, 255])

lowblack= np.array([0, 0, 0])
# upblack = np.array([180, 255, 30])
upblack = np.array([180, 255, 25])
#Функция отвечает за нахождение черных контуров на левом датчике


def dlz(frame):
    global dl, dlm
    for i in range(0, 180, 9):
        dblz = frame[250:310, i:(i + 9)]
        hsv = cv2.cvtColor(dblz, cv2.COLOR_BGR2HSV)
        mask_black = cv2.inRange(hsv, lowblack, upblack)
        mask_blue = cv2.bitwise_not(cv2.inRange(hsv, lowblue, upblue))
        mask_black = cv2.bitwise_and(mask_black, mask_blue)
        imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_black, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x1, y1, h1, w1 = 0, 0, 0, 0
        # находим черные контуры#находим черные контуры
        dlm[i//9] = 0
        for contorb1 in contoursd1:
            x, y, w, h = cv2.boundingRect(contorb1)
            a1 = cv2.contourArea(contorb1)
            # выделяем самый большой контур
            if x + w > x1 + w1 and a1 > 100 and h > 40:
                x1, w1, y1, h1 = x, w, y, h
                dlm[i // 9] = 1
                cv2.rectangle(frame, (i, 250), ((i + 9), 310), (255, 255, 255), -1)

    dl = 0
    for i in range(20):
         if dlm[19 - i] == 1:
              dl = 20 - i
              break
#Функция отвечает за нахождение черных контуров на правом датчике
def drz(frame):
     global dr, drm
     for i in range(0, -180, -9):
          dbrz = frame[250:310, 640+i-9:640+i]
          hsv = cv2.cvtColor(dbrz, cv2.COLOR_BGR2HSV)
          mask_black = cv2.inRange(hsv, lowblack, upblack)
          mask_blue = cv2.bitwise_not(cv2.inRange(hsv, lowblue, upblue))
          mask_black = cv2.bitwise_and(mask_black, mask_blue)
          imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_black, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          x1, y1, h1, w1 = 0, 0, 0, 0
          # находим черные контуры#находим черные контуры
          drm[((180 + i) // 9) - 1] = 0
          for contorb1 in contoursd1:
               x, y, w, h = cv2.boundingRect(contorb1)
               a1 = cv2.contourArea(contorb1)
               # выделяем самый большой контур
               if x + w > x1 + w1 and a1 > 100 and h > 40:
                    x1, w1, y1, h1 = x, w, y, h
                    drm[((180 + i) // 9) - 1] = 1
                    cv2.rectangle(frame, ((640+i-9), 250), ((640+i), 310), (255, 255, 255), -1)

     dr = 0
     for i in range(20):
          if drm[i] == 1:
               dr = 20 - i
               break






#Функция отвечает за движене робота на основе регулятора
def p():
     global dr, dl, servo, eold, direct, dlm, drm, max_servo

     #находим ошибку
     e = dl-dr
     if -1 <= e <= 1:
          e = 0
     #обьявляем коэффициент
     kp = 2.5
     kd = 0.2
     #используем формулу пд регулятора
     servo = kp*e + kd*(e - eold)
     #записываем старую ошибку
     eold=e
     #предохраниние от резких поворотов
     if servo>50:
          servo=max_servo
     if servo<-50:
          servo=-max_servo
     #если датчики не видят черныхконтуров
     if dl==0:
          servo=-30
     if dr==0:
          if direct == "orange":
               servo=18
          else:
               servo=20
     #находим направение нашего робота
     if dr == 0 and dl == 0:
          if direct == "blue":
               servo = -20
          if direct == "orange":
               servo = 20
     # cv2.putText(frame, str(dlm) + '  ' + str(dl), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
     # cv2.putText(frame, str(drm) + '  ' + str(dr), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
     # cv2.putText(frame, str(servo) + '  ' + str(e), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

#Функция отвечает за остановку робота и за счет кругов
def dlin(frame):
     global lowor, upor, line,upblue,lowblue, line_orange, line_blue, direct, circle, time_line, stop, stop_flag, stop_time, index
     line = 'None'
     # условие если оранжевые или голубые контуры не найдены, находим направление движения нашего робота
     if direct == "None":
          x, y, w, h = 0, 0, 0, 0
          #выделяем область интереса
          linz=frame[410:430,295:345]
          #накладываем серую маску на наше изображение для нахождения оранжевых контуров
          hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
          mask_orange = cv2.inRange(hsv, lowor, upor)
          imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          #поиск оранжевых контуров
          for contorb1 in contoursd1:
               x, y, w, h = cv2.boundingRect(contorb1)
               if w * h>100:
                    line_orange += 1
                    line = 'orange'
                    direct = "orange"
          # накладываем серую маску на наше изображение для нахождения голубых контуров
          mask_blue = cv2.inRange(hsv, lowblue, upblue)
          imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          # поиск голубых контуров
          for contorb1 in contoursd1:
               x, y, w, h = cv2.boundingRect(contorb1)
               if w * h > 100:
                    line = 'blue'
                    direct = "blue"
                    line_blue += 1
          #оюводим найденные контуры
          cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
          #
          if direct != "None":
               circle += 1
               time_line = time.time()
     # если контуры уже найдены и известно направление робота
     else:
          # если первым контуром попался голубой
          if direct == "blue":
               x, y, w, h = 0, 0, 0, 0
               #обьявление области интереса
               linz = frame[410:430, 295:345]
               hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
               mask_blue = cv2.inRange(hsv, lowblue, upblue)
               imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
               # поиск контуров
               for contorb1 in contoursd1:
                    x, y, w, h = cv2.boundingRect(contorb1)
                    if w * h > 100:
                         line = 'blue'
               # обводим найденные контуры
               cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
               #условие считает круги
               if line == "blue" and time_line + 0.5 < time.time():
                    #записываем круг
                    circle += 1
                    #в массив записываем средние значение проезда круга
                    stop[index]=round(time.time()-time_line,2)
                    index+=1
                    #ибнуляем индекс и записываем в массив значенияпо новой
                    if index==4:
                         index=0
                    time_line = time.time()
          # если первым контуром попался оранжевый
          if direct == "orange":
               x, y, w, h = 0, 0, 0, 0
               # выделяем область интереса
               linz = frame[410:430, 295:345]
               hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
               mask_orange = cv2.inRange(hsv, lowor, upor)
               imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
               # находим оранжевые контуры
               for contorb1 in contoursd1:
                    x, y, w, h = cv2.boundingRect(contorb1)
                    if w * h > 100:
                         line = 'orange'
               #обводим найденные контуры
               cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
               #если увидели оранжевый то считаем круг
               if line == "orange" and time_line + 0.5 < time.time():
                    # добавляем один круг
                    circle += 1
                    #записывае в массив среднее значения проезда участка
                    stop[index] = round(time.time() - time_line, 2)
                    index += 1
                    # если идекс достиг 4, то обнуляем его
                    if index == 4:
                         index = 0
                    time_line = time.time()
     #обводим область интереса
     cv2.rectangle(frame, (295, 410), (345, 430), (0, 0, 0), 2)

#цикл проигрывает наши функции
while True:

     fps1 += 1
     if time.time() > fps_time + 1:
          fps_time = time.time()
          fps = fps1
          fps1 = 0

     #запускаем функции
     frame = robot.get_frame(wait_new_frame=1)
     dlin(frame)
     dlz(frame)
     drz(frame)
     # условие проверки кол-во кругов
     if circle == 12:
          #остановка если круги достигли 12
          if time.time()>time_stop+stop[0]*0.6:
               speed=0
     else:
          time_stop = time.time()
     # условие если скорость робота больше 0
     if speed>0:
          p()
     # иначе серво не двигается
     else:
          servo=0
     #отправляем сообщения на пайборд для того что бы включились моторы

     # servo = 0
     message = str(int(speed) + 200) + str(int(servo-5) + 200) + rgb + '$'
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
     #проверка нажата кнопка или нет
     if btn == '0' and btntime+1 < time.time():
          btntime = time.time()
          #устанавлеваем скорость в 60 если кнопка нажата
          if speed==0:
               speed=80
          else:
               speed=0

     cv2.putText(frame, str("fps=") + str(fps), (0, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("line=") + str(direct), (480, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("c=") + str(circle), (0, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("dl=") + str(dl), (100, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("dr=") + str(dr), (100, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.rectangle(frame, (640, 250), (640 - 9 * (dr - 1), 310), (255, 255, 255), -1)
     cv2.rectangle(frame, (460, 250), (640, 310), (255, 0, 0), 2)
     cv2.rectangle(frame, (0, 250), (0 + 9 * (dl - 1), 310), (255, 0, 0), 2)
     cv2.rectangle(frame, (0, 250), (180, 310), (255, 0, 0), 2)
     #обновление экрана
     robot.set_frame(frame,40)
