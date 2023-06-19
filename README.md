# Структура репозитория:<br>
1.3D – папка содержащая 3D модели, которые использовались для создания робота<br>
2.Src –  папка с файлами, которые используются для описания в README.md<br>
3.Видео – папка содержит видео работа нашей модели, которая проезжает по полю квалификацию и файлик с названием: «ссылка на ютьюб». Это ссылка ведет на наше видео про обьяснение работы робота и его составных частей в общем плане.<br>
4.Код – папка содержит код, который используется при работе робота<br>
	4.1 kvalifikacia.py– файл который используется для проезда трассы на этапе квалификации. В нем считывается изображение с камеры и передается управляющее воздействие на пайборд<br>
	4.2 main.py – загружаем его на пайборд. В нем приводятся в работу компоненты подключенные к пайборду на основе сообщения полученного с расберри<br>
	4.3 final.py – код находится в папке Код, используется для проезда финальной трассы<br>
	4.4 autostart- файл, который загружается при запуске расберри<br>
4.5 start_robot.py – программа для упрощенной работы с роботом<br>
	4.6 robotAPI.py  - программа используется для упрощенной работы с камерой робота. <br>
5.Технический журнал – папка хранит в себе три файла формата docx, файлы представляют собой документации и тщательное обьяснение работы робота. <br>
6.Фото – папка содержит фотографию разработчиков робота.<br>
# Обьяснение кода<br>
main.py – файл формата python, загружается на пайборд, с целью управления нижней части робота или же ходовкой. Немало важный смысл программы, это прием сообщений с расберри, в сообщении храниться информация о том с какой скоростью должен ехать робот, с каким углом поворачивать и включение светодиода. Конец каждого сообщения заканчивается символом $ этот символ означает конец предложения. Это программа является обязательной для загрузки иначе следуйщий код работать не будет.<br><br>
kvalifikacia.py – этот файл используется для загрузки в расберри. Предназначен для того что бы проехать голую трассу, без обьезда красных и зеленых препятствий, программа проезжает 12 кругов и останавливается в том месте, откуда начинала движение.<br><br>
final.py – файл используется для проезда трассы, загружается в расберри. Предназначен для того что бы роехать 12 кругов и обьехать красные припятствия с правой стороны, а зеленые с левой стороны. <br><br>
robot_API.py – файл используется в качестве помошника в управлении камерой. Эта программа позволяет выделать на датчиках робота области интереса, обводить контуры и считывать определять hsv.<br><br>
 start_robot.py – программа позволяет увидеть всё то что видит робот, рассмотреть области интереса и обводимые контуры. Программа используется для удобной работы с роботом и его отладки. С помощью программы мы загружаем в робота программу.<br><br>
autostart - программа хранится на расбери и хранит в себе небольшой код, в котором указывается программа которую нужно включить. <br>

# Загрузка программы на пайборд<br>
На пайборд загружается только одна программа с названием main.py. Этот файл отвечает за получение сообщения для пайборда от расберри. Загрузка файла main.py является обязательной, для того что бы работали дальнейшие программы. Что бы загрузить на пайборд программу мы делаем:<br>
	1. Скачиваем файл main.py с нашего гитхаба:<br>
		Путь до файла: Код/main.py<br>
2. Подключаем пайборд к компьютеру с помощью микро usb, в проводнике пайборд называется PYBFLASH: <br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/pyboard.PNG)<br>
3. Открываем в проводнике наш пайборд:<br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/PYBFLASH.PNG)<br>
4. Перекидываем файл main.py, если в вашем пайборде уже есть файл main.py, как случилось у нас, то просто скопируте код с нашего файла main.py на гитхабе и вставьте его в файл main.py, который уже стоит у вас на пайборде. Если файла main.py на пайборде нет, то перекидывайте его на пайборд:<br>
<br>

# Загрузка файла на расберри с компьютера<br>
На расберии у нас загружаются две программы kvalifikacia.py или final.py взависимоти от типа заезда, квалификации или финала. Они загружаются по одному алгоритму. Разберем его на примере загрузки квалификации, описанном ниже.
1. Сначала скачиваем бесплатную программу PyCharm с официального сайта. <br>
2. Скачиваем с нашего гитхаба файл start_robot.py, RobotAPI.py и файл kavalifikacia.py<br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/Git.PNG)<br>
ВАЖНОЕ ПРИМЕЧАНИЕ! Скаченные файлы должны лежать в одной папке, советую создать отдельную папку и загрузит туда скаченные файлы!<br>
3.  С помощью правой кнопки мыши открываем файл start_robot.py в программе PyCharm. <br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/Statr.PNG)<br>
4. Когда программа открыла код, нужно скачать библиотеки, которых у вас нет.<br>
5. Теперь с помощью правой кнопки мыши нажимаем на зеленную кнопку старта.<br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/Pr.PNG)<br>
6. У нас открывается окно. Теперь нужно подключиться к нашему роботу по wi-fi. Что бы это сделать запускаем робота и ожидаем его название в сети, наш робот называется Team1.<br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/web.PNG)<br>
7. когда произошло сопряжение с роботом нажимаем на кнопку connection и в выпадающем списке выбираем нашего робота.<br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/connect.PNG)<br>
8. Программа подключилась к роботу, теперь откроем файл kavalifikacia.py. Что бы это сделать нажимаем кнопку Load, выбираем нужный файл kavalifikacia.py, нажимаем ОК.<br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/load_kv.PNG)<br>
9. Теперь код загружен на нашего робота, что бы проверить код в действии нужно нажать в окне на кнопку video, что бы видеть то что на экране робота и запустить робота на поле, нажав на кнопку на его плате.<br>
![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/video_kv.PNG)<br>
<br>
Автоматическая загрузка файла на расберри<br>
Для того чтобы нужный файл запускался на расберри сразу после включения робота, у нас существует файл autostart.py.<br>
Внутри него нужно импортировать нужный файл:<br>
import kvalifikacia - для квалификации,<br>
import final - для финала.<br>

![alt text](https://github.com/igor-k07/FE-2023-Inside/blob/main/src/autostart.PNG)<br>
В случае на картинке выше импортируется файл kvalifikacia.py, а импорт другого файла закомментирован.<br>
Загрузка autostart.py происходит по тому же алгоритму, как и при загрузке остальных файлов на расберри. После его загрузки, при запуске робота, на нем уже будет та программа которую мы импортировали. Остаётся лишь запустить её.
