# Smart fan project, spring 2023, MIPT

# Проект умного вентилятора, весна 2023, МФТИ 

## Настройка прошивки

Для настройки работы нашего вентилятора требуется сделать несколько простых шагов:

### Включение камеры

В командной строке введите 
\```
sudo raspi-config
\```
В открывшимся окне зайдите в Interfaces, затем в Enable Camera. Вам будет предложено включить камеру, нажмите Enter. Также подключите камеру к соответствующему порту платы.

### Настройка автозапуска

Теперь нужно сделать так, чтобы программа запускалась одновременно с включением малинки. Для этого воспользуемся стандартным для linux профилировщиком cron.

В файле start.sh введите следующее:
```
<путь к интерпретатору> <путь к файлу src/main.py>
```

Теперь введите в терминале команду
```
crontab -e
```
Если вы используете cron впервые, вам будет предложено выбрать редактор для чтения файла. ВЫберите нужный и нажмите Enter.

В конце открывшегося файла добавьте следующую строку
```
@reboot bash <путь к файлу start.sh>
```
Теперь программа будет запускаться одновременно с включением платы.

На этом настройка завершена. Наслаждайтесь лёгким бризом от вашего нового 4 ГБ ОЗУ 1500 МГЦ Вентилятора!