import requests
from bs4 import BeautifulSoup
import json
import re

# создадим функцию для скэпинга книг
def scrape_books():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html" 
    all_books = [] #словарь для всех книг
    page_number = 1 #с какой стр. начать скрэпинг

    while True: # начинает бесконечный цикл, пока статус кода равен 200
        print(f"Скрейпинг страницы {page_number}...")
        response = requests.get(base_url.format(page_number))

        if response.status_code != 200:
            break  # Выход из цикла, если страница не найдена

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        if not books:
            break  # Выход из цикла, если книги не найдены

        for book in books:
            title = book.h3.a['title'] #обращение к HTML структуре странице внутри тега "'article"->"h3"->"a"
            price = book.find('p', class_='price_color').text[1:] 
        
            in_stock_text = book.find('p', class_='instock availability').text.strip()

            # Извлекаем количество в наличии с помощью регулярного выражения
            in_stock_match = re.search(r'(\d+)', in_stock_text) #достаточно сложное для меня выражение, до которого сам бы не дошел. Но в нем происходит поиск совпадений по шаблону (библ ре.сёрч)
            # Если находится совпадение, берём первое число в группе (группа совпадений). Где \d - Это метасимвол, который соответствует любой цифре (0-9), + дает понять, что ищем элемент Д один и более раз.
            in_stock = int(in_stock_match.group(1)) if in_stock_match else 0  # Если не найдено, устанавливаем 0

            description = ""  # Описание здесь не доступно на странице списка, нужно будет получить отдельно

            # Ссылка на страницу книги для получения описания
            book_link = book.h3.a['href']
            book_page_url = f"http://books.toscrape.com/catalogue/{book_link}"

            # Получаем описание книги
            book_response = requests.get(book_page_url)
            book_soup = BeautifulSoup(book_response.text, 'html.parser')
            description = book_soup.find('meta', attrs={'name': 'description'})['content'].strip()

            all_books.append({
                'title': title,
                'price': price,
                'in_stock': in_stock,
                'description': description
            })

        page_number += 1

    # Сохраняем данные в JSON-файл
    with open('books_data.json', 'w', encoding='utf-8') as f: #создает новый файл для записи данных книг и именует его Ф
        json.dump(all_books, f, ensure_ascii=False, indent=4)

    print(f"Скрейпинг завершен. Всего книг: {len(all_books)}")

if __name__ == "__main__":
    scrape_books()
