import urllib.request
import re
import csv
import codecs
import time
from progress.bar import Bar


# Главная фукция, собирает все данные и отправляет на запись
def main():
    sleep_data = float(input('Введите время задержки в секундах: '))
    start_input = input(
        'Принято время в ' + str(sleep_data) + ' секунды(-у)!\nНажмите на Enter для начала работы скрипта\n')
    headers = {'a': 'URL', 'b': 'Общая цена', 'c': "Цена доставки", 'd': "Ссылка картинки", 'f': "Название", 'e': 'Имя'}
    write_csv_headers(headers)
    urls_names = get_urls_names()
    urls = get_urls(urls_names)
    names = get_names(urls_names)
    names_len = len(names)
    global bar
    bar = Bar('Процесс: ', max=names_len)
    const_c = -1
    for url in enumerate(urls):
        try:
            price_data = get_price(get_html(url[1]))
        except:
            price_data = 'none'
        try:
            now_url = get_url(url[1])
        except:
            now_url = 'none'
        try:
            images = get_images(get_html(url[1]))
        except:
            images = 'none'
        try:
            shipping_data = get_price_shipping(get_html(url[1]))
        except:
            shipping_data = 'none'
        const_c += 1
        if(now_url !='none' and price_data !='none' and shipping_data != 'none' and images != 'none'):
            data = {'name': names[const_c], 'url': now_url, 'price': price_data, 'shipping_price': shipping_data, 'images': images}
            write_csv(data)
            time.sleep(sleep_data)
    bar.finish()
    print("Закончено!")

# получение всех имён и url
def get_urls_names():
    try:
        file = codecs.open("names_urls.txt", 'r', 'utf-8')
        line = file.readlines()
    finally:
        file.close()
    return line

# получение всех url
def get_urls(urls_names):
    urls = ''.join(urls_names)
    s = re.findall('http://[^\r\n]+', urls)
    return s

def get_names(urls_names):
        name = []
        for i in range(len(urls_names)):
            names = re.search('[а-я, А-Я, 0-9, A-Z, a-z]*[^http://+(\\r\\n)]', urls_names[i]).group(0)
            name.append(names)
        return(name)

# получение html кода страницы
def get_html(url):
    f = urllib.request.urlopen(url) 
    html = f.read().decode('utf-8')  
    return html 

# получение "чисотого" url
def get_url(url):
    Url = urllib.request.urlopen(url).geturl()
    return Url

# получаем цену
def get_price(html):
    get_price = re.findall(r'"formatedPrice":"[^"]*"',
                           html)
    price = ''.join(get_price) 
    return price.split('"')[3]

# получаем ссылки на изображения
def get_images(html):
    image_get = re.search('"skuPropertyImagePath":"https://ae01.alicdn.com/kf/[^^]*640x640.jpg', html).group(0)
    image = image_get.split('"')
    return(image[-1])

# получаем цену за доставку
def get_price_shipping(html):
    price_shipping = re.search('"formatedAmount":"[^&]*руб',
                               html).group()
    price_shipping = price_shipping.split("\"")
    if price_shipping[-1] == "0,00 руб":
        price_shipping[-1] = "Бесплатная доставка!"
    return price_shipping[-1]

# записываем заголовки для csv
def write_csv_headers(headers):
    with open("file.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow((headers['e'],
                         headers['b'],
                         headers['c'],
                         headers['a'],
                         headers['d']))

# записываем данные в cvs
def write_csv(data):
    if data['url'] != 'none': 
        with open("file.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow((data['name'],
                             data['price'],
                             data['shipping_price'],
                             data['url'],
                             data['images']))
        bar.next()
if __name__ == '__main__':
    main()
