# Тестовое задание на вакансию Разработчик в тестировании.

### Установка
### Пункт 1.<a id='STEP_ONE'></a>
Скачать проект в локальную директорию. В текущей директории будет создана папка `test_case_simbirsoft`

```bash
git clone https://github.com/Jugern/Pytest-Selenium-Allure.git
```

### Пункт 2.<a id='STEP_TWO'></a>
Перейдите в папку с проектом:
```bash
cd test_case_simbirsoft
```
### Далее есть 3 варианта запуска тестов.
1) `Pytest`, `Allure` и `Selenium grid` [установлены локально на компьютере](#step_3_1)
2) `Pytest`, `Allure` установлены локально, `Selenium grid` [будет запускаться через Docker](#step_3_2)
3) `Pytest`, `Allure` и `Selenium grid` [будут запущены через Docker](#step_3_3)
___

### 3.1) Запуск тестов локально с предустановленными программами.<a id='step_3_1'></a>
    
Создайте виртуальное окружение и активируйте его,
потом обновить pip и установить зависимости:
#### <br>на windows
```bash
python -m venv venv & .venv\Scripts\activate & pip install &
python -m pip install –upgrade pip & pip install -r requirements.txt
```
#### на linux 
```bash
python3 -m venv .venv && source ./venv/bin/activate &&
pip3 install --upgrade pip && pip install -r requirements.txt
```
На linux сразу нужно сделать скрипт запускаемым `wait-for-it.sh`
```bash
sudo chmod +x ./wait-for-it.sh
```


#### Настраиваем конфигурацию тестов<a id='config'></a>
Открываем файл `.env` и прописываем параметры.
```dotenv
number_test=1  # кол-во random тестов (запускаются на Chrome, Edge, Firefox)
url_selenium_grid=http://<ip-address>  # url адресс selenium grid  
port_selenium_grid=:4444  # порт selenium_grid
selector=/wd/hub  # адресная строка для selenium_grid
# все вместе получится 
# http://<ip-address>:port/wd/hub
```
[//]: # (Для ускорения выполнения тестов, а так же для запуска тестов в docker контейнере или CI/CD нужно отключить `headless` режим. Для это нужно раскомментировать следующую строчку `# options.add_argument&#40;"--headless"&#41;` в файле `conftest.py`)

[//]: # (Если при попытке выполнить тесты в Браузере FireFox на Ubuntu выскакивает ошибка: "Your Firefox profile cannot be loaded. It may be missing or inaccessible." То необходимо переустановить FireFox, подробности [тут]&#40;https://stackoverflow.com/questions/72405117/selenium-geckodriver-profile-missing-your-firefox-profile-cannot-be-loaded&#41; и [тут]&#40;https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04&#41;)


### Запуск тестов

1. Так как в `pytest.ini` прописана команда `--alluredir=allure-results` 
запуск тестов выгрузкой файлов для allure-отчета производится без дополнительных передач аргументов:
```bash
pytest -sv
```
2. Генерация готового отчета выполняется командой:
```bash
allure generate --clean
```
3. Открываем сгенерированный отчет командой
```
allure open 
````
После чего в командной строке появиться `http://<ip-адрес>:порт` 
<br>Переходим на данный адрес, получаем отчет тестирования.
___

### 3.2) Запуск тестов и создание отчетов будет локально, <br>selenium grid будет запускаться через Docker.<a id='step_3_2'></a>
 
!!! Подразумевается что вы уже находитесь в папке с проектом. Если это не так, выполните
[Пункт1](#STEP_ONE) и [Пункт №2](#STEP_TWO) 

Настраиваем файл `.env`.
```dotenv
number_test=1  # кол-во random тестов (запускаются на Chrome, Edge, Firefox)
url_selenium_grid=<ip-address>  # url адресс selenium grid  
port_selenium_grid=:4444  # порт selenium_grid
selector=/wd/hub  # адресная строка для selenium_grid
# все вместе получится 
# <ip-address>:port/wd/hub
```

Запускаем selenium-grid через docker compose:

```bash
docker-compose -f docker-compose-selenium.yml up
```
* Команда `docker compose`(раздельно) используется в новых версиях Докера, в старых, необходимо использовать `docker-compose`(через дефис)

Далее выполняем все действия [Пункта 3.1](#step_3_1), кроме действия по [настройке](#config) `.env` файла.

### 3.3) Запуск тестов, создание отчетов и selenium grid будет запускаться через Docker.<a id='step_3_3'></a>

!!! Подразумевается что вы уже находитесь в папке с проектом. Если это не так, выполните
[Пункт1](#STEP_ONE) и [Пункт №2](#STEP_TWO) 

Настраиваем файл `all.env`
```dotenv
number_test=1  # кол-во random тестов (запускаются на Chrome, Edge, Firefox)
port_selenium_grid=4444
```
* port_selenium_grid, меняем если порт занят другой программой.
* обратите внимание: url_selenium_grid и selector для точки ввхода убраны.

##### Запуск docker-compose: 
```bash
docker-compose -f docker-compose-all.yml up
```
Или с флагом `-d` для запуска в фоновом режиме
```bash
docker-compose -f docker-compose-all.yml up -d 
```
После инициализации и прохождения всех тестов, отчет будет доступен по адресу http://localhost:9999

Остановить контейнеры можно командой:
```bash
docker-compose -f docker-compose-all.yml down 
```
___

