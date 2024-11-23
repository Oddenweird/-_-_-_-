import requests

# Так как у меня не получилось найти API для Foursquare, я решил пойти по другому пути и написать код, который будет искать по запросу книгу в Google Book (Google Play store если точнее) и выводить данные про неё.
# Вводить название можно также и на русском. Гуггл к этому равнодушен.

def search_book(title):

    url = f"https://www.googleapis.com/books/v1/volumes?q={title}"
    
      response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Проверяем, есть ли результаты
        if "items" in data:
            print(f"Найдено {len(data['items'])} книг по запросу '{title}':")
            for item in data['items']:
                book_title = item['volumeInfo'].get('title', 'Без названия')
                authors = item['volumeInfo'].get('authors', ['Автор не указан'])
                average_rating = item['volumeInfo'].get('averageRating', 'Нет рейтинга')
                info_link = item['volumeInfo'].get('infoLink', 'Нет ссылки')

                print(f"- {book_title} (Авторы: {', '.join(authors)})")
                print(f"  Рейтинг: {average_rating}")
                print(f"  Ссылка: {info_link}\n")
        else:
            print(f"Книги с названием '{title}' не найдены.")
    else:
        print("Ошибка при обращении к API:", response.status_code)

if __name__ == "__main__":
    book_title = input("Введите название книги: ")
    search_book(book_title)
