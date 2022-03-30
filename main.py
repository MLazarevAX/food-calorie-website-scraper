import time
from bs4 import BeautifulSoup
import requests
import os
from services.service import writefile, sub_items_in_string, write_json, read_json, write_to_csv

# Constants
BASE_URL = r'https://health-diet.ru'
URL = r'https://health-diet.ru/table_calorie'
FILE_NAME_BASE_PAGE = "path_to_doc"
FILE_EXTENCION = ".txt"

# Иммитируем передачу параметров реального браузера в headers
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}


def main():
    # Получаем исходную страницу и записываем ее в файл
    if FILE_NAME_BASE_PAGE not in os.listdir('data'):
        page_html = requests.get(URL, headers=headers).text

        writefile(FILE_NAME_BASE_PAGE, page_html, FILE_EXTENCION)

    # Открываем исходный html из которого достанем все ссылки на таблицы каллорийностей продуктов
    with open(f"data/{FILE_NAME_BASE_PAGE}{FILE_EXTENCION}", encoding='utf-8') as file:
        src = file.read()

    # Получаем объект soup для дальнейшего парсинга
    soup = BeautifulSoup(src, "lxml")

    # Получаем все ссылки и добавляем в словарь, складывая его с базовым url .
    hrefs_all_product = soup.findAll(class_="mzr-tc-group-item-href")
    all_hrefs_categories = {item.text: BASE_URL + item.get("href") for item in hrefs_all_product}

    # Записываем полученный словарь в json файл
    write_json('all_categories_dict.json', "w", all_hrefs_categories, indent=4, ensure_ascii=False, encoding="utf-8-sig")

    all_hrefs_categories = read_json('all_categories_dict.json')

    iteration_count = int(len(all_hrefs_categories)) - 1
    count = 0
    print(f"Всего итераций: {iteration_count}")
    try:
        for category_name, category_href in all_hrefs_categories.items():
            category_name = sub_items_in_string(category_name, character="_")

            page_html = requests.get(category_href, headers=headers).text
            writefile(category_name, page_html, '.html')

            with open(f'data/{category_name}.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")

            # проверка страницы на наличие таблицы с продуктами
            alert_block = soup.find(class_="uk-alert-danger")
            if alert_block is not None:
                continue

            # собираем заголовки таблицы
            table_headers = soup.find(class_='mzr-tc-group-table').find('tr').findAll('th')


            product = table_headers[0].text
            calories = table_headers[1].text
            proteins = table_headers[2].text
            fats = table_headers[3].text
            carbohydrates = table_headers[4].text
            tables_fields = (
                        product,
                        calories,
                        proteins,
                        fats,
                        carbohydrates,
                            )
            write_to_csv(f'data/{category_name}.csv', tables_fields, 'w', encoding="utf-8-sig")

            # Собираем данные продуктов
            products_data = soup.find(class_='mzr-tc-group-table').find('tbody').findAll('tr')
            product_info = []

            # Собираем данные из таблицы и записываем в файл
            for item in products_data:
                product_td = item.find_all_next('td')

                product = product_td[0].find('a').text
                calories = product_td[1].text
                proteins = product_td[2].text
                fats = product_td[3].text
                carbohydrates = product_td[4].text

                tables_fields_values = (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates,
                )
                product_info.append(
                    {
                        "Продукт": product,
                        "Категории": calories,
                        "Белки": proteins,
                        "Жиры": fats,
                        "Углеводы": carbohydrates,
                    }
                )
                write_to_csv(f'data/{category_name}.csv', tables_fields_values, mode='a', encoding="utf-8-sig")
                write_json(f'data/{category_name}.json', 'a', product_info, indent=4, ensure_ascii=False, encoding="utf-8-sig")
            time.sleep(3)
            count += 1
            print(f"# Итерация {count}. {category_name} записан...")
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()
