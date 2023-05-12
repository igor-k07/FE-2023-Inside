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
fps = 0
fps1 = 0
fps_time = 0
btntime = time.time()
znaktime = time.time()
dl=0
dr=0
xz=0
yz=0
hz = 0
wz = 0
xo = 0
line= 'None'
colorz="None"
color1 = 0
inn = ''
speed = 0
servo = 0
rgb = '010'
btn = 1
eold=1
eold1=1
line_orange, line_blue = 0, 0
circle = 0
direct = "None"
sum=0

stop_time=0
stop = [0,0,0,0]
index=1
stop_flag=False

time_line = time.time()
time_stop = time.time()
time_data = time.time()

#обьявляем массивы hsv для оранжевого голубого и черного
# lowr=np.array([0,150,50])
# upr=np.array([5,255,255])
lowr=np.array([0,122,90])
upr=np.array([5,255,255])

# lowg=np.array([ 66, 150,  52])
# upg=np.array( [ 83, 255, 255])
lowg=np.array([ 71, 185,  38])
upg=np.array( [ 81, 255, 255])

# lowor = np.array([7, 110, 64])
# upor = np.array([21, 255, 255])
lowor = np.array([7, 110, 64])
upor = np.array([21, 255, 255])

# lowblue = np.array([82, 63, 0])
# upblue = np.array([180, 255, 255])
lowblue = np.array([105, 73, 0])
upblue = np.array([180, 255, 255])

lowblack= np.array([0, 95, 0])
# upblack = np.array([180, 255, 30])
upblack = np.array([180, 255, 30])

#Функция отвечает вывод на изображение необходимых для нас переменных, за изменением которых нам нужно следить
def telemetria(frame):
     # объявляем глобальные переменные
     global fps, xz,yz,line,dl,dr,colorz,servo, circle
     # поочередно выводим на экран количество fps; кол-во увиденных синих или оранжевых линий;
     # цвет линии, по направлению которой едет робот
     cv2.putText(frame, str("sp=") + str(message), (0,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("fps=") + str(fps), (0, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("l_b=") + str(circle), (0, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("line=") + str(direct), (480, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)

# функция, которая отвечает за нахождение контуров знаков (красных и зеленых)
def datz(frame):
     #объявляем глобальные переменные
     global lowr,upr,lowg,upg,colorz, xz,yz, hz, wz, znaktime, color1
     # задаем область интереса для нашего датчика
     # dz=frame[190:380, 100:540]
     dz = frame[190:380, 100:540]
     hsv = cv2.cvtColor(dz, cv2.COLOR_BGR2HSV)
     # Ищем зеленый цвет
     maskg = cv2.inRange(hsv, lowg, upg)
     # Находим контуры зеленого
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(maskg,(3,3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     w_g = 0
     h_g = 0
     x_g = 0
     y_g = 0
     # Отбираем подходящие по размеру контуры
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          if w * h > 800 and  y+h > y_g+h_g:
              w_g=w
              h_g=h
              x_g = x
              y_g = y

     #Ищем красный цвет
     maskr = cv2.inRange(hsv, lowr, upr)
     # Находим контуры красногго
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(maskr,(3,3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     w_r = 0
     h_r = 0
     x_r = 0
     y_r = 0
     # Ищем подходящие по размерам контуры
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          # выделяем самый большой контур
          if w * h > 700 and y+h > y_r+h_r:
               w_r = w
               h_r = h
               x_r = x
               y_r = y

     # Если не увидели знак, то цвет = None
     if h_r == 0 and h_g == 0:
          if znaktime + 0.1 < time.time():
               colorz = "None"
               xz, yz, wz, hz = 0,0,0,0
          if znaktime + 0.5 < time.time():
               color1 = "None"
     # Если нашли контуры нужного цвета
     else:
          # Задаем таймер для увиденного знака
          znaktime = time.time()
          # Если увидели оба знака
          if h_r>0 and h_g>0:
               # Выбираем тот, контур которого больше
               if y_r+h_r > y_g+h_g:
                    colorz = "red"
                    # Обводим его контур
                    cv2.rectangle(dz, (x_r, y_r), (x_r + w_r, y_r + h_r), (0, 255, 0), 2)
                    xz, yz, wz, hz =  x_r, y_r, w_r, h_r
                    if yz + hz > 50:
                         color1 = colorz
               else:
                    colorz = "green"
                    # Обводим его контур
                    cv2.rectangle(dz, (x_g, y_g), (x_g + w_g, y_g + h_g), (0, 0, 255), 2)
                    xz, yz, wz, hz =  x_g, y_g, w_g, h_g
                    if yz+hz> 50:
                        color1 = colorz
          # Если увидели только один знак
          else:
              # Красный
               if h_r>0:
                    colorz = "red"
                    cv2.rectangle(dz, (x_r, y_r), (x_r + w_r, y_r + h_r), (0, 255, 0), 2)
                    xz, yz, wz, hz =  x_r, y_r, w_r, h_r
                    if yz+hz> 50:
                        color1 = colorz
               # Зеленый
               if h_g>0:
                    colorz = "green"
                    cv2.rectangle(dz, (x_g, y_g), (x_g + w_g, y_g + h_g), (0, 0, 255), 2)
                    xz, yz, wz, hz =  x_g, y_g, w_g, h_g
                    if yz + hz > 50:
                         color1 = colorz

     # Отрисовываем рамку, в области которой работает наш датчик
     cv2.rectangle(frame, (100, 190), (540, 380), (0, 0, 0), 2)

#Функция отвечает за нахождение черных контуров на левом датчике
def dlz(frame):
     global dl
     # обьявлям область интереса
     dblz = frame[250:310, 0:180]
     hsv = cv2.cvtColor(dblz, cv2.COLOR_BGR2HSV)
     mask_black = cv2.inRange(hsv, lowblack, upblack)
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_black, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     x1, y1, h1, w1 = 0, 0, 0, 0
     # находим черные контуры#находим черные контуры
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          a1 = cv2.contourArea(contorb1)
          # выделяем самый большой контур
          if x + w > x1 + w1 and a1>250:
               x1, w1, y1, h1 = x, w, y, h

     dl = x1 + w1
     # cv2.rectangle(dblz, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

#Функция отвечает за нахождение черных контуров на правом датчике
def drz(frame):
     global dr
     # обьявлям область интереса
     drlz  = frame[250:310, 460:640]
     hsv = cv2.cvtColor(drlz, cv2.COLOR_BGR2HSV)
     mask_black = cv2.inRange(hsv, lowblack, upblack)
     imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_black, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     x1, y1, h1, w1 = 180, 0, 0, 0
     # находим черные контуры
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          a1 = cv2.contourArea(contorb1)
          # выделяем самый большой контур
          if 180-x > 180-x1 and a1 > 250:
               x1, w1, y1, h1 = x, w, y, h

     dr = 180-x1
     # cv2.rectangle(drlz, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

#Функция отвечает за движене робота на основе регулятора
def p():
     global dr, dl, servo, eold, direct
     #находим ошибку
     e = dl-dr
     #обьявляем коэффициент
     kp = 0.3
     kd = 0.15
     #используем формулу пд регулятора
     servo = kp*e + kd*(e - eold)
     #записываем старую ошибку
     eold=e
     #предохраниние от резких поворотов
     if servo>50:
          servo=50
     if servo<-50:
          servo=-50
     #если датчики не видят черных контуров
     if dl==0:
          servo=-50
     if dr==0:
          servo=50
     #находим направение нашего робота
     if dr == 0 and dl == 0:
          if direct == "blue":
               servo = -30
          if direct == "orange":
               servo = 30
     # Условия для объезда сложных препятствий
     if direct == "blue" and color1 == 'red':
          if time_data + 0.3 > time.time():
               servo = -50
     # if direct == "orange" and color1 == 'red':
     #      if time_data + 0.7 > time.time():
     #           servo = -10
     if direct == "orange" and color1 == 'green':
          if time_data + 0.3 > time.time():
               servo = 50



# Функция для объезда красного знака
def pdzr():
     global xz, yz, wz, hz, servo, eold1
     # рассчет перспективы
     xo = 270 - (yz+hz)*1.2
     e = (xz+wz) - xo
     k = 0.2
     servo = k*e + 0.2*(e - eold1)
     eold1=e



# Функция для объезда зеленого знака
def pdzg():
     global xz, yz, wz, hz, servo, eold1
     # рассчет перспективы
     xo = 210 + (yz + hz)*1.24
     e = xz - xo
     k = 0.2
     servo = k*e + 0.2*(e - eold1)
     eold1=e

#Функция отвечает за остановку робота и за счет кругов
def dlin(frame):
     global lowor, upor, line,upblue,lowblue, line_orange, line_blue, direct, circle, time_line, stop, stop_flag, stop_time, index
     line = 'None'
     # условие если оранжевые или голубые контуры не найдены, находим направление движения нашего робота
     if direct == "None":
          x, y, w, h = 0, 0, 0, 0
          # выделяем область интереса
          linz=frame[410:430,295:345]
          # накладываем серую маску на наше изображение для нахождения оранжевых контуров
          hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
          mask_orange = cv2.inRange(hsv, lowor, upor)
          imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          # поиск оранжевых контуров
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
          # оюводим найденные контуры
          cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)

          if direct != "None":
               circle += 1
               time_line = time.time()
     # если контуры уже найдены и известно направление робота
     else:
          # если первым контуром попался голубой
          if direct == "blue":
               x, y, w, h = 0, 0, 0, 0
               # обьявление области интереса
               linz = frame[410:430, 295:345]
               hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
               mask_blue = cv2.inRange(hsv, lowblue, upblue)
               imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE,
                                                         cv2.CHAIN_APPROX_NONE)
               # поиск контуров
               for contorb1 in contoursd1:
                    x, y, w, h = cv2.boundingRect(contorb1)
                    if w * h > 100:
                         line = 'blue'
               # обводим найденные контуры
               cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
               #условие считает круги
               if line == "blue" and time_line + 0.5 < time.time():
                    # записываем круг
                    circle += 1
                    # в массив записываем средние значение проезда круга
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
               imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE,
                                                         cv2.CHAIN_APPROX_NONE)
               # находим оранжевые контуры
               for contorb1 in contoursd1:
                    x, y, w, h = cv2.boundingRect(contorb1)
                    if w * h > 100:
                         line = 'orange'
               # обводим найденные контуры
               cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
               # если увидели оранжевый то считаем круг
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

     # обводим область интереса
     cv2.rectangle(frame, (295, 410), (345, 430), (0, 0, 0), 2)

#цикл проигрывает наши функции
while True:

     fps1 += 1
     if time.time() > fps_time + 1:
          fps_time = time.time()
          fps = fps1
          fps1 = 0
     # запускаем функции
     frame = robot.get_frame(wait_new_frame=1)
     cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 0), -1)
     dlin(frame)
     dlz(frame)
     drz(frame)
     datz(frame)
     # условие проверки кол-во кругов
     if circle == 12:
          # остановка если круги достигли 12
          if time.time()>time_stop+stop[0]*0.6:
               speed=0
     else:
          time_stop = time.time()

     # условие если скорость робота больше 0
     if speed>0:
          if colorz == 'None':
               p()
          elif colorz=='red':
               time_data = time.time()
               pdzr()
          elif colorz == 'green':
               time_data = time.time()
               pdzg()
     # иначе серво не двигается
     else:
          # p()
          servo=0

     if servo > 50:
          servo = 50
     if servo < -50:
          servo = -50

     # servo = 0
     # отправляем сообщения на пайборд для того что бы включились моторы
     message = str(int(speed) + 200) + str(int(servo) + 200) + rgb + '$'
     telemetria(frame)
     cv2.rectangle(frame, (490, 250), (640, 310), (255, 0, 0), 2)
     cv2.rectangle(frame, (0, 250), (180, 310), (255, 0, 0), 2)
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
     # проверка нажата кнопка или нет
     if btn == '0' and btntime+1 < time.time():
          btntime = time.time()
          # устанавлеваем скорость в 60 если кнопка нажата
          if speed==0:
               speed=60
          else:
               speed=0

     # обновление экрана
     robot.set_frame(frame,40)

