import json
import os
import random
from typing import List, Dict, Any, Optional

# Переменные для путей к файлам (согласовано с README)
DATA_DIR_DEFAULT = 'data'
QUOTES_FILE_DEFAULT_NAME = 'quotes.json'
HISTORY_FILE_DEFAULT_NAME = 'history.json'
QUOTES_FILE_PATH_DEFAULT = os.path.join(DATA_DIR_DEFAULT, QUOTES_FILE_DEFAULT_NAME)
HISTORY_FILE_PATH_DEFAULT = os.path.join(DATA_DIR_DEFAULT, HISTORY_FILE_DEFAULT_NAME)
QUOTES_FILE_PATH: str = os.getenv('QUOTES_DATA_PATH', QUOTES_FILE_PATH_DEFAULT)
HISTORY_FILE_PATH: str = os.getenv('HISTORY_DATA_PATH', HISTORY_FILE_PATH_DEFAULT)


def _get_data_path(custom_path: Optional[str]) -> str:
    """
    Возвращает полный путь к файлу данных.
    :param custom_path: Опциональный путь для тестов.
    :return: Путь к файлу JSON.
    """
    return custom_path if custom_path is not None else _get_data_path_default()


def _get_data_path_default() -> str:
    """
    Возвращает путь по умолчанию на основе глобальной переменной.
    Эта функция нужна для передачи в os.makedirs.
    """
    return QUOTES_FILE_PATH


def init_data_file(custom_path: Optional[str] = None) -> None:
    """
    Создает файл данных и директорию (если их нет).
    Добавляет предопределенные цитаты при первом запуске.
    :param custom_path: Опциональный путь для тестов.
    """
    path_to_use: str = custom_path if custom_path is not None else QUOTES_FILE_PATH

    dir_name: str = os.path.dirname(path_to_use) or '.'

    try:
        os.makedirs(dir_name, exist_ok=True)

        if not os.path.exists(path_to_use):
            # Предопределенные цитаты для начального заполнения базы данных
            initial_quotes: List[Dict[str, Any]] = [
                {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "topic": "Мотивация"},
                {"text": "Единственный способ сделать выдающуюся работу — любить то, чем ты занимаешься.", "author": "Стив Джобс", "topic": "Работа"},
                {"text": "Жизнь — это то, что происходит с нами, пока мы строим планы на будущее.", "author": "Аллен Сондерс", "topic": "Жизнь"},
                {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Самосовершенствование"},
                {"text": "Успех — это переход от одной неудачи к другой без потери энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"}
            ]

            with open(path_to_use, 'w', encoding='utf-8') as f:
                json.dump(initial_quotes, f, ensure_ascii=False, indent=2)

    except OSError as e:
        print(f"Ошибка файловой системы при инициализации ({path_to_use}): {e}")


def _load_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Универсальная функция для загрузки JSON-файлов с обработкой ошибок.
    :param file_path: Путь к файлу.
    :return: Список словарей (пустой список при ошибке).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content: str = f.read().strip()
            if not content:
                print(f"Файл {file_path} пуст. Возвращен пустой список.")
                return []
            return json.loads(content)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Будет создан при первой записи.")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}. Файл может быть поврежден.")
        return []
    except PermissionError as e:
        print(f"Нет прав на чтение файла {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла {file_path}: {e}")
        return []


def load_quotes(custom_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает список предопределенных цитат из JSON-файла.
    :param custom_path: Опциональный путь для тестов.
    :return: Список словарей с цитатами.
    """
    path_to_use: str = custom_path if custom_path is not None else QUOTES_FILE_PATH
    return _load_json_file(path_to_use)


def load_history(custom_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Загружает историю сгенерированных пользователем цитат из JSON-файла.
    :param custom_path: Опциональный путь для тестов.
    :return: Список словарей с историей.
    """
    path_to_use: str = custom_path if custom_path is not None else HISTORY_FILE_PATH
    return _load_json_file(path_to_use)


def save_quotes(quotes: List[Dict[str, Any]], custom_path: Optional[str] = None) -> None:
    """
    Сохраняет список предопределенных цитат в JSON-файл.
    :param quotes: Список словарей с цитатами.
    :param custom_path: Опциональный путь для тестов.
    """
    path_to_use: str = custom_path if custom_path is not None else QUOTES_FILE_PATH

    try:
        dir_name = os.path.dirname(path_to_use) or '.'
        os.makedirs(dir_name, exist_ok=True)
        with open(path_to_use, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)
            print(f"Данные успешно сохранены в {path_to_use}")
    except PermissionError as e:
        print(f"Ошибка записи в файл {path_to_use}: Нет прав доступа.")
        raise


def save_history(history: List[Dict[str, Any]], custom_path: Optional[str] = None) -> None:
    """
    Сохраняет историю сгенерированных пользователем цитат в JSON-файл.
    :param history: Список словарей с историей.
    :param custom_path: Опциональный путь для тестов.
    """
    path_to_use: str = custom_path if custom_path is not None else HISTORY_FILE_PATH

    try:
        dir_name = os.path.dirname(path_to_use) or '.'
        os.makedirs(dir_name, exist_ok=True)
        with open(path_to_use, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            print(f"История успешно сохранена в {path_to_use}")
    except PermissionError as e:
        print(f"Ошибка записи в файл {path_to_use}: Нет прав доступа.")
        raise


def get_random_quote(quotes: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Возвращает случайную цитату из списка.
    :param quotes: Список доступных цитат.
    :return: Словарь с данными о цитате или None.
    """
    if not quotes or not isinstance(quotes, list):
        return None

    try:
        return random.choice(quotes)
    except (IndexError, Exception):
        return None


def add_quote(text: str, author: str, topic: Optional[str] = "") -> bool:
    """
    Добавляет новую цитату в базу данных с проверкой на пустые строки.
    :param text: Текст цитаты.
    :param author: Автор цитаты.
    :param topic: Тема цитаты (опционально).
    :return: True если добавление прошло успешно.
    :raises ValueError: Если текст или автор пусты.
    """
    if not isinstance(text, str) or not isinstance(author, str):
        raise ValueError("Текст и автор должны быть строками.")

    if not text.strip() or not author.strip():
        raise ValueError("Текст и автор цитаты не могут быть пустыми.")

    new_quote = {
        "text": text.strip(),
        "author": author.strip(),
        "topic": topic.strip() if topic and isinstance(topic, str) else ""
    }

    quotes_list = load_quotes() or []
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
    if not quotes or not author_name or not isinstance(author_name, str):
        return []

    author_lower = author_name.lower().strip()
    return [q for q in quotes if q.get('author', '').lower().strip() == author_lower]


def filter_quotes_by_topic(quotes: List[Dict[str, Any]], topic_name: str) -> List[Dict[str, Any]]:
    """
    Фильтрует список цитат по теме (без учета регистра).
    :param quotes: Список для фильтрации.
    :param topic_name: Тема для поиска.
    :return: Отфильтрованный список.
    """
    if not quotes or not topic_name or not isinstance(topic_name, str):
        return []

    topic_lower = topic_name.lower().strip()
    return [q for q in quotes if q.get('topic', '').lower().strip() == topic_lower]


def get_unique_authors(quotes: List[Dict[str, Any]]) -> List[str]:
    """
    Возвращает отсортированный список уникальных авторов.
    :param quotes: Список цитат.
    :return: Список уникальных имен авторов.
    """
    if not quotes or not isinstance(quotes, list):
        return []

    authors_set = {q.get('author', '') for q in quotes}
    authors_cleaned_sorted = sorted([a for a in authors_set if a and a.strip()])
    return authors_cleaned_sorted


def get_unique_topics(quotes: List[Dict[str, Any]]) -> List[str]:
    """
    Возвращает отсортированный список уникальных тем.
    :param quotes: Список цитат.
    :return: Список уникальных тем.
    """
    if not quotes or not isinstance(quotes, list):
        return []

    topics_set = {q.get('topic', '') for q in quotes}
    topics_cleaned_sorted = sorted([t for t in topics_set if t and t.strip()])
    return topics_cleaned_sorted
