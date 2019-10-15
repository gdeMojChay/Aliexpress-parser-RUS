import urllib.request
import re
import csv
import codecs
import time
# Главная фукция, собирает все данные и отправляет на запись
def main():
    sleep_data = float(input('Введите время задержки в секундах: '))
    start_input = input(
        'Принято время в ' + str(sleep_data) + ' секунды(-у)!\nНажмите на Enter для начала работы скрипта\n')
    headers = {'a': 'URL', 'b': 'Общая цена', 'c': "Цена доставки", 'd': "Ссылка картинки", 'f': "Название", 'e': 'Имя'}
    write_csv_headers(headers)
    urls_names = get_urls_names()
    urls = get_urls(urls_names)
    names= get_names(urls_names)
    const_c = -1
    for url in enumerate(urls):
        print(url[1])
        try:
            price_data = get_price(get_html(url[1]))
            # print(price_data)
        except:
            price_data = 'none'
        try:
            now_url = get_url(url[1])
            # print(now_url)
        except:
            now_url = 'none'
        try:
            images = get_images(get_html(url[1]))
        except:
            images = 'none'
        try:
            shipping_data = get_price_shipping(get_html(url[1]))
            print(shipping_data)
        except:
            shipping_data = 'none'
        const_c += 1
        # print(names[const_c])
        if(now_url !='none' and price_data !='none' and shipping_data != 'none' and images != 'none'):
            data = {'name': names[const_c], 'url': now_url, 'price': price_data, 'shipping_price': shipping_data, 'images': images}
            write_csv(data)
            time.sleep(sleep_data)
    print("Закончено!")

# получение всех имён и url
def get_urls_names():
    try:
        file = codecs.open("names_urls.txt", 'r', 'utf-8')
        # for i in file:
        line = file.readlines()
        print(line)
    finally:
        file.close()
    return line

# получение всех url
def get_urls(urls_names):
    urls = ''.join(urls_names)
    s = re.findall('http://[^\r\n]+', urls)
    print(s)
    return s

def get_names(urls_names):
        name = []
        # print(urls_names[0])
        for i in range(len(urls_names)):
            names = re.search('[а-я, А-Я, 0-9, A-Z, a-z]*[^http://+(\\r\\n)]', urls_names[i]).group(0)
            name.append(names)
        # print(name)
        # print(len(name))
        return(name)

# получение html кода страницы
def get_html(url):
    f = urllib.request.urlopen(url)  # \получем сам
    html = f.read().decode('utf-8')  # /html код
    return html  # возвращаем его

# получение "чисотого" url
def get_url(url):
    Url = urllib.request.urlopen(url).geturl()
    return Url

# получаем цену
def get_price(html):
    get_price = re.findall(r'"formatedPrice":"[^"]*"',
                           html)  # получаем списком необработанную цену (командой re.search не хочет нормально работать)
    price = ''.join(get_price)  # из списка делаем строку
    # print(price.split('"')[3])                             # дебаг
    return price.split('"')[3]  # возвращаем чисто цену

# получаем ссылки на изображения
def get_images(html):
    image_get = re.search('"skuPropertyImagePath":"https://ae01.alicdn.com/kf/[^^]*640x640.jpg', html).group(0)  # получаем опять списком (ну не виноват я) необработанные url'ы (дико написано) фотографий
    # print(image_get)
    image = image_get.split('"')
    # print(image[-1])
    # all_images_get = ''.join(all_images_get)  # как не странно делаем из списка строку
    # all_images_get = all_images_get.split('"')  # и... разделяем строку, делая из неё список
    # dowland_images = []  # создаём список для скачиваний фоток
    # dowland_images.append(all_images_get.pop(3))  # \ добавляем в новый список
    # # dowland_images.append(all_images_get.pop(4))  # / url'ы из первого, а именно два первых
    # print(dowland_images)  # для проверки
    # return dowland_images
    return(image[-1])

# получаем цену за доставку
def get_price_shipping(html):
    price_shipping = re.search('"formatedAmount":"[^&]*руб',
                               html).group()  # получаем цену, и да, тут нормально работает только search
    price_shipping = price_shipping.split("\"")  # разбиваем строку
    if price_shipping[-1] == "0,00 руб":
        price_shipping[-1] = "Бесплатная доставка!"
    return price_shipping[-1]  # ну и возращаем данные о цене доставки

# записываем заголовки для csv
def write_csv_headers(headers):
    with open("table.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow((headers['e'],
                         headers['b'],
                         headers['c'],
                         headers['a'],
                         headers['d']))

# записываем данные в cvs
def write_csv(data):
    if data['url'] != 'none': #отсекаем ненужные, "пустые" данные
        # print(data)
        with open("biznes.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow((data['name'],
                             data['price'],
                             data['shipping_price'],
                             data['url'],
                             data['images']))
        # print("acsses!")
if __name__ == '__main__':  # \запускаем
    main()  # /функцию main()
