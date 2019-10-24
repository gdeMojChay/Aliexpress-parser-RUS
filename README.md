# Aliexpress-parser-RUS
Скрипт созданный для парсинга названия товара из .txt файла, общей цены с учётом доставки, цену самой доставки (если доставка бесплатна то пишется "Бесплатная доставка!", "чистой" ссылки на страницу и ссылку на заглавное изображение товара в разрешение 640x640

Начало работы:
1) Установите файл Aliexpress-parser-RUS.py и поместите его в отдельную папку;
2) Убедитесь в том, что все библиотеки (urllib.request, re, csv, codecs, time, progress) установлены и корректно работают;
3) Создайте файл names_urls.txt
4) Заполните созданный файл следующим образом (количество ссылок неограниченно): ИМЯ ССЫЛКА
ИМЯ ССЫЛКА
ИМЯ ССЫЛКА
Имя не обязательно указывать;
5) Сохраните файл;
6) Запустите Aliexpress-parser-RUS.py;
7) Введите целочисленное число или число с точкой (1.5) для установки время "сна" парсера после обработки одной ссылки;
8) В конце работы в консоли будет выводено "Закончено!" и в папке будет файл table.csv;
9) Открывайте table.csv любым для вас удобным способом и пользуйтесь данными.
