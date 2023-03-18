# Тестовое задание для компании Saber Interactive

Данное тестовое задание - это сценарий теста игры .kkrieger.<br />
Скрипт запускает игру, делает скриншот в начале и в конце теста, записывает в файл системную информацию и параметры использования ресурсов ПК.

Для запуска необходимо:
- скачать игру .kkrieger (https://www.old-games.ru/game/download/5169.html)
- скачать программу для получения FPS, в данном тесте используется Fraps (https://fraps.com/download.php)
- клонировать проект <br /> <code>git clone https://github.com/idudnikov/saber_test_task.git</code>
- создать и активировать виртуальное окружение <br /> <code>py -m venv venv</code> <br /> <code>.\venv\Scripts\activate</code>
- установить зависимости <br /> <code>py -m pip install --upgrade pip</code> <br />  <code>pip install -r requirements.txt</code>

Скрипт запускается со следующими аргументами: <br />
<code> python <путь до скрипта> "<путь к исполняемому файлу игры>" -o "<путь к папке сохранения результатов теста>"</code>
<br />Пример команды запуска: <br />
<code> python .\script.py "C:\\...\kkrieger-beta\pno0001.exe\\" -o "C:\\...\saber_test\output\\"</code>
