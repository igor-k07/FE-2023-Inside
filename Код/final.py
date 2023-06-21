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
flag_povorot = False
state = 0
time_state = time.time()

stop_time=0
stop = [0,0,0,0]
index=1
stop_flag=False
dlm = [0] * 20
drm = [0] * 20

time_line = time.time()
time_stop = time.time()
time_data = time.time()

index_cube = 0
index_place=0
list_cube = [["","",""], ["","",""],["", "", ""],["","",""]]
list_flag=True
list_time=time.time()

cube_color="None"
cube_time=time.time()
cube_flag=False
index_time = time.time()
flag_pov = False
last_cube_time=0
pl_time = 0
pl_list = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
pl_index_place = 0
pl_index_time = 0
pl_flag = False
#обьявляем массивы hsv для оранжевого голубого и черного
# lowr=np.array([0,150,50])
# upr=np.array([5,255,255])
lowr=np.array([0,66,69])
upr=np.array([8,255,255])

# lowg=np.array([ 66, 150,  52])
# upg=np.array( [ 83, 255, 255])
lowg=np.array([ 65, 192,  37])
upg=np.array( [ 89, 255, 255])

# lowor = np.array([7, 110, 64])
# upor = np.array([21, 255, 255])
lowor = np.array([9, 100, 100])
upor = np.array([30, 255, 255])

# lowblue = np.array([82, 63, 0])
# upblue = np.array([180, 255, 255])
lowblue = np.array([84, 63, 0])
upblue = np.array([180, 255, 255])

lowblack= np.array([0, 0, 0])
# upblack = np.array([180, 255, 30])
upblack = np.array([180, 255, 40])

#Функция отвечает вывод на изображение необходимых для нас переменных, за изменением которых нам нужно следить
def telemetria(frame):
     # объявляем глобальные переменные
     global fps, xz,yz,line,dl,dr,colorz,servo, circle, dl, dr, list_cube, list_flag, last_cube_time
     # поочередно выводим на экран количество fps; кол-во увиденных синих или оранжевых линий;
     # # цвет линии, по направлению которой едет робот
     # cv2.putText(frame, str(index_cube) + str(circle), (0,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str("time=") + str(round(pl_time,2)), (0, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str("flag=") + str(pl_list[3]), (0, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str("") + str(list_cube[2]), (280, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str("") + str(list_cube[1]), (280, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str("list=") + str(list_cube[0]), (280, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255),2)
     # cv2.putText(frame, str("") + str(list_cube[3]), (280, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str(pl_list), (0, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str(stop), (0, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("p=") + str(circle), (490, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("dir=") + str(direct), (490, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("fps=") + str(fps), (460, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("c_time=") + str(last_cube_time), (460, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("color=") + str(cube_color), (460, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)

# функция, которая отвечает за нахождение контуров знаков (красных и зеленых)
def datz(frame):
     #объявляем глобальные переменные
     global lowr,upr,lowg,upg,colorz, xz,yz, hz, wz, znaktime, color1, index_cube, index_place, list_cube, list_flag, cube_time, cube_color, cube_time, cube_flag, index_time, flag_pov, pl_time, pl_index_time, pl_index_place, pl_flag, stop
     # задаем область интереса для нашего датчика
     # dz=frame[190:380, 100:540]
     dz = frame[190:350, 120:520]
     hsv = cv2.cvtColor(dz, cv2.COLOR_BGR2HSV)
     # Ищем зеленый цвет
     maskg = cv2.inRange(hsv, lowg, upg)
     # Находим контуры зеленого
     contoursd1, hod1 = cv2.findContours(cv2.blur(maskg,(3,3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     w_g = 0
     h_g = 0
     x_g = 0
     y_g = 0
     # Отбираем подходящие по размеру контуры
     for contorb1 in contoursd1:
          x, y, w, h = cv2.boundingRect(contorb1)
          if w * h > 700 and  y+h > y_g+h_g:
              w_g=w
              h_g=h
              x_g = x
              y_g = y

     #Ищем красный цвет
     maskr = cv2.inRange(hsv, lowr, upr)
     # Находим контуры красногго
     contoursd1, hod1 = cv2.findContours(cv2.blur(maskr,(3,3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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
          if znaktime + 0.05 < time.time():
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
     if yz + hz > 150 and cube_time+1<time.time() and circle < 8:
          cube_time = time.time()
          cube_color = colorz
          cube_flag = True
          if colorz != "None" and direct != "None" and list_flag == True and circle<5 and pl_flag==False:
              pl_time = cube_time - time_line
              pl_list[pl_index_place][pl_index_time] = round(pl_time,2)
              pl_index_time += 1
              if pl_index_time > 2:
                  pl_index_place += 1
                  pl_index_time = 0
                  if pl_index_place > 3:
                      pl_index_place = 0
              list_cube[index_cube][index_place] = colorz
              index_place += 1
              if index_place > 2:
                  index_cube += 1
                  index_place = 0

     if flag_pov == True and pl_flag== False:
          index_cube += 1
          index_place=0
          pl_index_place+=1
          pl_index_time = 0
          flag_pov = False
          if index_cube == 4:
              index_cube = 0
          if pl_index_place == 4:
              pl_index_place = 0
     if circle == 5:
          pl_flag = True

     if pl_flag == True:
          for i in range(0,4):
              if list_cube[i][0] != '' and list_cube[i][1] != '':
                list_cube[i][2] = list_cube[i][1]
                list_cube[i][1] = ""
              elif list_cube[i][0] != '':
                if pl_list[i][0] > 0.33 * stop[i] and pl_list[i][0] < 0.66 * stop[i]:
                    list_cube[i][1] = list_cube[i][0]
                    list_cube[i][0] = ''
                if pl_list[i][0] >  0.66 * stop[i]:
                    list_cube[i][2] = list_cube[i][0]
                    list_cube[i][0] = ''
          pl_flag = 2
     if colorz == "None" and pl_flag== False:
          list_flag = True



     # Отрисовываем рамку, в области которой работает наш датчик

#Функция отвечает за нахождение черных контуров на левом датчике
def dlz(frame):
    global dl, dlm

    for i in range(0, 200, 10):
        dblz = frame[230:290, i:(i + 10)]
        hsv = cv2.cvtColor(dblz, cv2.COLOR_BGR2HSV)
        mask_black1 = cv2.inRange(hsv, lowblack, upblack)
        mask_blue = cv2.bitwise_not(cv2.inRange(hsv, lowblue, upblue))
        m = cv2.bitwise_and(mask_black1, mask_blue)
        contoursd1, hod1 = cv2.findContours(m, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x1, y1, h1, w1 = 0, 0, 0, 0
        # находим черные контуры#находим черные контуры
        dlm[i//10] = 0
        for contorb1 in contoursd1:
            x, y, w, h = cv2.boundingRect(contorb1)
            a1 = cv2.contourArea(contorb1)
            # выделяем самый большой контур
            if x + w > x1 + w1 and a1 > 40 and h > 20:
                x1, w1, y1, h1 = x, w, y, h
                dlm[i // 10] = 1
                cv2.rectangle(frame, (i, 230), ((i + 10), 290), (255, 255, 255), -1)

    dl = 0
    for i in range(20):
         if dlm[19 - i] == 1:
              dl = 20 - i
              break

    # cv2.rectangle(frame, (0, 230), (200, 290), (255, 0, 0), 2)

#Функция отвечает за нахождение черных контуров на правом датчике
#Функция отвечает за нахождение черных контуров на правом датчике
def drz(frame):
     global dr, drm
     for i in range(0, -200, -10):
          dbrz = frame[230:290, 640 + i - 10:640 + i]
          hsv = cv2.cvtColor(dbrz, cv2.COLOR_BGR2HSV)
          mask_black = cv2.inRange(hsv, lowblack, upblack)
          mask_blue = cv2.bitwise_not(cv2.inRange(hsv, lowblue, upblue))
          m = cv2.bitwise_and(mask_black, mask_blue)
          contoursd1, hod1 = cv2.findContours(m, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          x1, y1, h1, w1 = 0, 0, 0, 0
          # находим черные контуры#находим черные контуры
          drm[((200 + i) // 10) - 1] = 0
          for contorb1 in contoursd1:
               x, y, w, h = cv2.boundingRect(contorb1)
               a1 = cv2.contourArea(contorb1)
               # выделяем самый большой контур
               if x + w > x1 + w1 and a1 > 40 and h > 20:
                    x1, w1, y1, h1 = x, w, y, h
                    drm[((200 + i) // 10) - 1] = 1
                    cv2.rectangle(frame, ((640 + i - 10), 230), ((640 + i), 290), (255, 255, 255), -1)

     dr = 0
     for i in range(20):
          if drm[i] == 1:
               dr = 20 - i
               break

     # cv2.rectangle(frame, (440, 230), (640, 290), (255, 0, 0), 2)

# def pdl():
#      global dr, dl, servo, eold, direct, dlm, drm, max_servo
#
#      #находим ошибку
#      e = dl-8
#      if -1 <= e <= 1:
#           e = 0
#      #обьявляем коэффициент
#      kp = 3
#      kd = 0.4
#      #используем формулу пд регулятора
#      servo = kp*e + kd*(e - eold)
#      #записываем старую ошибку
#      eold=e
#      #предохраниние от резких поворотов
#      if servo>50:
#           servo=max_servo
#      if servo<-50:
#           servo=-max_servo
#
# def pdr():
#      global dr, dl, servo, eold, direct, dlm, drm, max_servo
#
#      #находим ошибку
#      e = 8-dr
#      if -1 <= e <= 1:
#           e = 0
#      #обьявляем коэффициент
#      kp = 3
#      kd = 0.4
#      #используем формулу пд регулятора
#      servo = kp*e + kd*(e - eold)
#      #записываем старую ошибку
#      eold=e
#      #предохраниние от резких поворотов
#      if servo>50:
#           servo=max_servo
#      if servo<-50:
#           servo=-max_servo

#Функция отвечает за движене робота на основе регулятора
def pd():
     global dr, dl, servo, eold, direct
     #находим ошибку
     e = dl-dr
     if -1 <= e <= 1:
          e = 0
     #обьявляем коэффициент
     kp = 3
     kd = 0.4
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
     if dl == 0 and dr>2:
          servo = -25
          # if direct == 'None':
          #      # pdr()
     if dr == 0 and dl>2:
          servo = 25
          # if direct == 'None':
          #      # pdl()
     #находим направение нашего робота
     if dr == 0 and dl == 0:
          if direct == "blue":
               servo = -30
          if direct == "orange":
               servo = 30
          if direct == 'None':
               servo = 0
     # Условия для объезда сложных препятствий
     if direct == "blue" and color1 == 'red':
          if time_data + 0.4 > time.time():
               servo = -40
     # if direct == "orange" and color1 == 'red':
     #      if time_data + 0.7 > time.time():
     #           servo = -10
     if direct == "orange" and color1 == 'green':
          if time_data + 0.3 > time.time():
               servo = 40



# Функция для объезда красного знака
def pdzr():
     global xz, yz, wz, hz, servo, eold1
     # рассчет перспективы
     xo = 230 - (yz+hz)*1.1
     e = (xz+wz) - xo
     k = 0.2
     servo = k*e + 0.2*(e - eold1)
     eold1=e



# Функция для объезда зеленого знака
def pdzg():
     global xz, yz, wz, hz, servo, eold1
     # рассчет перспективы
     xo = 170 + (yz + hz)*1.3
     e = xz - xo
     k = 0.2
     servo = k*e + 0.2*(e - eold1)
     eold1=e

#Функция отвечает за остановку робота и за счет кругов
def dlin(frame):
     global lowor, upor, line,upblue,lowblue, line_orange, line_blue, direct, circle, time_line, stop, stop_flag, stop_time, index, cube_flag, cube_time, last_cube_time, flag_pov, last_cube_time
     line = 'None'
     # условие если оранжевые или голубые контуры не найдены, находим направление движения нашего робота
     if direct == "None":
          x, y, w, h = 0, 0, 0, 0
          # выделяем область интереса
          linz=frame[380:420,295:345]
          # накладываем серую маску на наше изображение для нахождения оранжевых контуров
          hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
          mask_orange = cv2.inRange(hsv, lowor, upor)
          contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          # поиск оранжевых контуров
          for contorb1 in contoursd1:
               x, y, w, h = cv2.boundingRect(contorb1)
               if w * h>70:
                    line_orange += 1
                    line = 'orange'
                    direct = "orange"
          # накладываем серую маску на наше изображение для нахождения голубых контуров
          mask_blue = cv2.inRange(hsv, lowblue, upblue)
          contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          # поиск голубых контуров
          for contorb1 in contoursd1:
               x, y, w, h = cv2.boundingRect(contorb1)
               if w * h > 80:
                    line = 'blue'
                    direct = "blue"
                    line_blue += 1
          # оюводим найденные контуры
          cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)

          if direct != "None":
               flag_pov = True
               if cube_flag == True and circle<8:
                   last_cube_time = time.time()- cube_time
                   cube_flag=False
               circle += 1
               time_line = time.time()
     # если контуры уже найдены и известно направление робота
     else:
          # если первым контуром попался голубой
          if direct == "blue":
               x, y, w, h = 0, 0, 0, 0
               # обьявление области интереса
               linz = frame[380:420, 295:345]
               hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
               mask_blue = cv2.inRange(hsv, lowblue, upblue)
               contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE,
                                                         cv2.CHAIN_APPROX_NONE)
               # поиск контуров
               for contorb1 in contoursd1:
                    x, y, w, h = cv2.boundingRect(contorb1)
                    if w * h > 80:
                         line = 'blue'
               # обводим найденные контуры
               cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
               #условие считает круги
               if line == "blue" and time_line + 0.5 < time.time():
                    # записываем круг
                    circle += 1
                    if cube_flag == True and circle<8:
                        last_cube_time = time.time() - cube_time
                        cube_flag = False
                    flag_pov = True
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
               linz = frame[380:420, 295:345]
               hsv = cv2.cvtColor(linz, cv2.COLOR_BGR2HSV)
               mask_orange = cv2.inRange(hsv, lowor, upor)
               contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE,
                                                         cv2.CHAIN_APPROX_NONE)
               # находим оранжевые контуры
               for contorb1 in contoursd1:
                    x, y, w, h = cv2.boundingRect(contorb1)
                    if w * h > 70:
                         line = 'orange'
               # обводим найденные контуры
               cv2.rectangle(linz, (x, y), (x + w, y + h), (0, 255, 0), 2)
               # если увидели оранжевый то считаем круг
               if line == "orange" and time_line + 0.5 < time.time():
                    # добавляем один круг
                    circle += 1
                    if cube_flag == True and circle<8:
                        last_cube_time = time.time() - cube_time
                        cube_flag = False
                    flag_pov = True
                    #записывае в массив среднее значения проезда участка
                    stop[index] = round(time.time() - time_line, 2)
                    index += 1
                    # если идекс достиг 4, то обнуляем его
                    if index == 4:
                         index = 0
                    time_line = time.time()
     # обводим область интереса
     # cv2.rectangle(frame, (295, 380), (345, 420), (0, 0, 0), 2)

def razvorot():
     global flag_povorot, state, speed, servo, direct, time_state, circle
     p = 1
     flag_povorot = True
     if direct == 'orange':
          p = -1

     if state == 0:
          speed = 0
          time_state = time.time()
          state = 1
     if direct == 'orange' or (direct == 'blue' and last_cube_time < 1):
          if state == 1:
               servo = 45 * p
               speed = 30
               if time_state + 1.8 < time.time():
                    state = 2
                    time_state = time.time()
          if state == 2:
               servo = -50 * p
               speed = -30
               if time_state + 0.7 < time.time():
                    state = 3
                    speed = 0
                    time_state = time.time()
          if state == 3:
               if last_cube_time < 1:
                    speed = -30
               else:
                    speed = 30
               if time_state + 1 < time.time():
                    flag_povorot = False
                    if p == 1:
                         direct = 'orange'
                    else:
                         direct = 'blue'
                    circle += 1
                    state = 4
                    speed = 60

#цикл проигрывает наши функции
while True:

     fps1 += 1
     if time.time() > fps_time + 1:
          fps_time = time.time()
          fps = fps1
          fps1 = 0
     # запускаем функции
     frame = robot.get_frame(wait_new_frame=1)
     cv2.rectangle(frame, (0, 0), (640, 100), (0, 0, 0), -1)
     if flag_povorot == False:
          dlin(frame)
          dlz(frame)
          drz(frame)
          datz(frame)

     # условие если скорость робота больше 0
     if speed>0:
          # Если не увидели знак, то едем по обычному регулятору
          if colorz == 'None':
               pd()
          # Если увидели красный знак, то едем по функции объезда красного знака
          elif colorz=='red':
               time_data = time.time()
               pdzr()
               list_time=time.time()
          # Если увидели кзеленый знак, то едем по функции объезда зеленого знака
          elif colorz == 'green':
               time_data = time.time()
               pdzg()
               list_time = time.time()
     # иначе серво не двигается
     else:
          servo=0
     # ограничения на поворот
     if servo > 50:
          servo = 50
     if servo < -50:
          servo = -50

     if circle == 8 and cube_color == 'red':
          razvorot()

     # условие проверки кол-во кругов
     if circle >= 12:
          if cube_color == 'red':
               if time.time() > time_stop + stop[0] * 0.2:
                    speed = 0
          else:
               # остановка если круги достигли 12
               if time.time() > time_stop + stop[0] * 0.6:
                    speed = 0
     else:
          time_stop = time.time()


     # отправляем сообщения на пайборд для того что бы включились моторы
     message = str(int(speed) + 200) + str(int(servo) + 200) + rgb + '$'
     # выводим телемитрию
     telemetria(frame)
     # обрисовываем область интереса правого и левого датчика черного
     # cv2.rectangle(frame, (460, 250), (640, 310), (255, 0, 0), 2)
     # cv2.rectangle(frame, (0, 250), (180, 310), (255, 0, 0), 2)
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

     cv2.rectangle(frame, (120, 190), (520, 350), (0, 0, 0), 2)
     # обновление экрана
     # cv2.rectangle(frame, (640, 230), (640 - 10 * (dr - 1), 290), (255, 255, 255), -1)
     cv2.rectangle(frame, (440, 230), (640, 290), (255, 0, 0), 2)
     # cv2.rectangle(frame, (0, 230), (0 + 10 * (dl - 1), 290), (255, 255, 255), -1)
     cv2.rectangle(frame, (0, 230), (200, 290), (255, 0, 0), 2)
     cv2.rectangle(frame, (295, 380), (345, 420), (0, 0, 0), 2)
     robot.set_frame(frame,40)

