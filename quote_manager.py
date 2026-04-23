import json
import os
import random
from typing import List, Dict, Any

# Переменные для путей к файлам (согласовано с README)
DATA_DIR_DEFAULT = 'data'
QUOTES_FILE_DEFAULT_NAME = 'quotes.json'
QUOTES_FILE_PATH_DEFAULT = os.path.join(DATA_DIR_DEFAULT, QUOTES_FILE_DEFAULT_NAME)


def _get_data_path(custom_path: str | None = None) -> str:
    """
    Возвращает полный путь к файлу данных.
    Приоритет: Переменная окружения -> Значение по умолчанию.
    :param custom_path: Опциональный путь для тестов.
    :return: Путь к файлу JSON.
    """
    env_path = os.getenv('QUOTES_DATA_PATH')
    if env_path:
         return env_path
    
     os.makedirs(DATA_DIR_DEFAULT, exist_ok=True)  # Создаем папку по умолчанию при необходимости
     return QUOTES_FILE_PATH_DEFAULT


def init_data_file(custom_path: str | None = None) -> None:
     """
     Создает файл данных и директорию (если их нет).
     Добавляет предопределенные цитаты при первом запуске.
     :param custom_path: Опциональный путь для тестов.
     """
     path_to_use: str = custom_path if custom_path is not None else _get_data_path()
     
     dir_name: str = os.path.dirname(path_to_use)
     
     try:
          os.makedirs(dir_name, exist_ok=True)
          
          if not os.path.exists(path_to_use):
               # Предопределенные цитаты для начального заполнения базы данных (Шаг 1 инструкции)
               initial_quotes: List[Dict[str, Any]] = [
                   {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "topic": "Мотивация"},
                   {"text": "Единственный способ сделать выдающуюся работу — любить то, чем ты занимаешься.", "author": "Стив Джобс", "topic": "Работа"},
                   {"text": "Жизнь — это то, что происходит с нами, пока мы строим планы на будущее.", "author": "Аллен Сондерс", "topic": "Жизнь"},
                   {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Самосовершенствование"},
                   {"text": "Успех — это переход от одной неудачи к другой без потери энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"}
               ]
               
               with open(path_to_use, 'w', encoding='utf-8') as f:
                    json.dump(initial_quotes + [], f)  # + [] чтобы показать пустой список для истории или добавить их в базу?
                    
     except OSError as e:
          print(f"Ошибка файловой системы при инициализации ({path_to_use}): {e}")


def load_quotes(custom_path: str | None = None) -> List[Dict[str, Any]]:
     """
     Загружает список цитат из JSON-файла.
     Проверяет на пустой файл и возвращает пустой список при ошибке.
     :param custom_path: Опциональный путь для тестов.
     :return: Список словарей с цитатами.
     """
     path_to_use: str = custom_path if custom_path is not None else _get_data_path()
     
     try:
          with open(path_to_use, 'r', encoding='utf-8') as f:
               content: str = f.read().strip()
               if not content:
                    print(f"Файл {path_to_use} пуст. Возвращен пустой список.")
                    return []
               return json.loads(content)
               
     except (FileNotFoundError, json.JSONDecodeError):
          print(f"Файл {path_to_use} не найден или поврежден. Будет создан заново.")
          init_data_file(path_to_use) # Пробуем пересоздать файл с начальными данными
          return []
     except Exception as e:
          print(f"Неизвестная ошибка при чтении файла {path_to_use}: {e}")
          return []


def save_quotes(quotes: List[Dict[str, Any]], custom_path: str | None = None) -> None:
     """
     Сохраняет список цитат в JSON-файл.
     :param quotes: Список словарей с цитатами.
     :param custom_path: Опциональный путь для тестов.
     """
     path_to_use: str = custom_path if custom_path is not None else _get_data_path()
     
     try:
          with open(path_to_use, 'w', encoding='utf-8') as f:
               json.dump(quotes, f, ensure_ascii=False, indent=2)
               print(f"Данные успешно сохранены в {path_to_use}")
               
     except PermissionError as e:
          print(f"Ошибка записи в файл {path_to_use}: Нет прав доступа.")
          raise


def get_random_quote(quotes: List[Dict[str, Any]]) -> Dict[str, Any] | None:
     """
     Возвращает случайную цитату из списка.
     :param quotes: Список доступных цитат.
     :return: Словарь с данными о цитате или None.
     """
     if not quotes:
          return None
     
     try:
          return random.choice(quotes)
     except IndexError:
          return None


def add_quote(text: str, author: str, topic: str | None = "") -> bool:
     """
     Добавляет новую цитату в базу данных с проверкой на пустые строки.
     :param text: Текст цитаты.
     :param author: Автор цитаты.
     :param topic: Тема цитаты (опционально).
     :return: True если добавление прошло успешно.
     :raises ValueError: Если текст или автор пусты.
     """
      if not text or not author:
           raise ValueError("Текст и автор цитаты не могут быть пустыми.")
       
       new_quote = {
           "text": text,
           "author": author,
           "topic": topic if topic else ""
       }
       
       quotes_list = load_quotes()
       quotes_list.append(new_quote)
       save_quotes(quotes_list)
       return True


def filter_quotes_by_author(quotes: List[Dict[str, Any]], author_name: str) -> List[Dict[str, Any]]:
      """
      Фильтрует список цитат по имени автора (без учета регистра).
      :param quotes: Список для фильтрации.
      :param author_name: Имя автора для поиска.
      :return: Отфильтрованный список.
      """
      return [q for q in quotes if q.get('author', '').lower() == author_name.lower()]


def filter_quotes_by_topic(quotes: List[Dict[str, Any]], topic_name: str) -> List[Dict[str, Any]]:
      """
      Фильтрует список цитат по теме (без учета регистра).
      :param quotes: Список для фильтрации.
      :param topic_name: Тема для поиска.
      :return: Отфильтрованный список.
      """
      return [q for q in quotes if q.get('topic', '').lower() == topic_name.lower()]


def get_unique_authors(quotes: List[Dict[str, Any]]) -> List[str]:
      """
      Возвращает отсортированный список уникальных авторов.
      :param quotes: Список цитат.
      :return: Список уникальных имен авторов.
      """
      authors = {q.get('author', '') for q in quotes}
      return sorted([a for a in authors if a]) # Убираем пустые строки


def get_unique_topics(quotes: List[Dict[str, Any]]) -> List[str]:
      """
      Возвращает отсортированный список уникальных тем.
      :param quotes: Список цитат.
      :return: Список уникальных тем.
      """
      topics = {q.get('topic', '') for q in quotes}
      return sorted([t for t in topics if t]) # Убираем пустые строки ("Без темы")
