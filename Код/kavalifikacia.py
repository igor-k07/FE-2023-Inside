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

# lowor = np.array([7, 110, 64])
# upor = np.array([21, 255, 255])
lowor = np.array([9, 100, 100])
upor = np.array([30, 255, 255])

# lowblue = np.array([82, 63, 0])
# upblue = np.array([180, 255, 255])
lowblue = np.array([88, 49, 0])
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
     cv2.putText(frame, str("circle=") + str(circle), (490, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("speed=") + str(speed), (490, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     cv2.putText(frame, str("fps=") + str(fps), (460, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
     # cv2.putText(frame, str("c_time=") + str(last_cube_time), (460, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)



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
        imd1, contoursd1, hod1 = cv2.findContours(m, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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
def drz(frame):
     global dr, drm
     for i in range(0, -200, -10):
          dbrz = frame[230:290, 640 + i - 10:640 + i]
          hsv = cv2.cvtColor(dbrz, cv2.COLOR_BGR2HSV)
          mask_black = cv2.inRange(hsv, lowblack, upblack)
          mask_blue = cv2.bitwise_not(cv2.inRange(hsv, lowblue, upblue))
          m = cv2.bitwise_and(mask_black, mask_blue)
          imd1, contoursd1, hod1 = cv2.findContours(m, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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

def pdl():
     global dr, dl, servo, eold, direct, dlm, drm, max_servo

     #находим ошибку
     e = dl-8
     if -1 <= e <= 1:
          e = 0
     #обьявляем коэффициент
     kp = 3
     kd = 0.4
     #используем формулу пд регулятора
     servo = kp*e + kd*(e - eold)
     #записываем старую ошибку
     eold=e



def pdr():
     global dr, dl, servo, eold, direct, dlm, drm, max_servo

     #находим ошибку
     e = 8-dr
     if -1 <= e <= 1:
          e = 0
     #обьявляем коэффициент
     kp = 3
     kd = 0.4
     #используем формулу пд регулятора
     servo = kp*e + kd*(e - eold)
     #записываем старую ошибку
     eold=e


#Функция отвечает за движене робота на основе регулятора
def pd():
     global dr, dl, servo, eold, direct
     #находим ошибку
     e = dl-dr
     if -1 <= e <= 1:
          e = 0
     #обьявляем коэффициент
     kp = 2
     kd = 1
     # 2, 1
     #используем формулу пд регулятора
     servo = kp*e + kd*(e - eold)
     #записываем старую ошибку
     eold=e
     #предохраниние от резких поворотов
     if servo>60:
          servo=60
     if servo<-60:
          servo=-60
     #если датчики не видят черных контуров
     if dl == 0 and dr>2:
          servo = -30
          if direct == 'None':
               pdr()
     if dr == 0 and dl>2:
          servo = 30
          if direct == 'None':
               pdl()

     #находим направение нашего робота
     if dr == 0 and dl == 0:
          if direct == "blue":
               servo = -30
          if direct == "orange":
               servo = 30
          if direct == 'None':
               servo = 0




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
          imd1, contoursd1, hod1  = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
          # поиск оранжевых контуров
          for contorb1 in contoursd1:
               x, y, w, h = cv2.boundingRect(contorb1)
               if w * h>70:
                    line_orange += 1
                    line = 'orange'
                    direct = "orange"
          # накладываем серую маску на наше изображение для нахождения голубых контуров
          mask_blue = cv2.inRange(hsv, lowblue, upblue)
          imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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
               imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_blue, (3, 3)), cv2.RETR_TREE,
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
               imd1, contoursd1, hod1 = cv2.findContours(cv2.blur(mask_orange, (3, 3)), cv2.RETR_TREE,
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

#цикл проигрывает наши функции
while True:

     fps1 += 1
     if time.time() > fps_time + 1:
          fps_time = time.time()
          fps = fps1
          fps1 = 0
     # запускаем функции
     frame = robot.get_frame(wait_new_frame=1)
     # cv2.rectangle(frame, (0, 0), (640, 100), (0, 0, 0), -1)
     dlin(frame)
     dlz(frame)
     drz(frame)
     # условие если скорость робота больше 0
     if speed>0:
          pd()
     # иначе серво не двигается
     else:
          servo=0
     # условие проверки кол-во кругов
     if circle >= 12:
          # остановка если круги достигли 12
          if time.time() > time_stop + stop[0] * 0.6:
               speed = 0
     else:
          time_stop = time.time()

     if direct == 'None' and speed!=0:
          speed = 50
     elif direct!="None" and speed != 0:
          speed = 80
     # отправляем сообщения на пайборд для того что бы включились моторы

     message = str(int(speed) + 200) + str(int(servo) + 200) + rgb + '$'
     # выводим телемитрию
     telemetria(frame)
     # обрисовываем область интереса правого и левого датчика черного
     # cv2.rectangle(frame, (460, 250), (640, 310), (255, 0, 0), 2)
     # cv2.rectangle(frame, (0, 250), (180, 310), (255, 0, 0), 2)
     port.write(message.encode('utf-8'))
     try:
          if port.in_waiting > 0:
               t = time.time()
               inn = ''
               while True:
                    a = str(port.read(), 'utf-8')
                    if a != '$':
                         inn += a
                    else:
                         break
                    if t + 0.02 < time.time():
                         break
               btn = inn
               port.reset_input_buffer()
          # проверка нажата кнопка или нет
     except ValueError:
          print('err')
     if btn == '0' and btntime+1 < time.time():
          btntime = time.time()
          # устанавлеваем скорость в 60 если кнопка нажата
          if speed==0:
               speed=80
          else:
               speed=0

     # cv2.rectangle(frame, (120, 190), (520, 350), (0, 0, 0), 2)
     # обновление экрана
     # cv2.rectangle(frame, (640, 230), (640 - 10 * (dr - 1), 290), (255, 255, 255), -1)
     cv2.rectangle(frame, (440, 230), (640, 290), (255, 0, 0), 2)
     # cv2.rectangle(frame, (0, 230), (0 + 10 * (dl - 1), 290), (255, 255, 255), -1)
     cv2.rectangle(frame, (0, 230), (200, 290), (255, 0, 0), 2)
     cv2.rectangle(frame, (295, 380), (345, 420), (0, 0, 0), 2)
     robot.set_frame(frame,40)

