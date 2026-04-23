import unittest
import os
import json
import shutil

from quote_manager import (
    add_quote,
    get_random_quote,
    filter_quotes_by_author,
    filter_quotes_by_topic,
    get_unique_authors,
    get_unique_topics,
    save_quotes,
    load_quotes,
    save_history,
    load_history,
    QUOTES_FILE_PATH,
    HISTORY_FILE_PATH,
)


class TestQuoteManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
         """Создает тестовую директорию перед всеми тестами."""
         cls.test_dir_base_quotes = 'tests/data_test/quotes'
         cls.test_dir_base_history = 'tests/data_test/history'
         
         os.makedirs(cls.test_dir_base_quotes + '/data', exist_ok=True)
         os.makedirs(cls.test_dir_base_history + '/data', exist_ok=True)
         
         cls.quotes_test_file_1path  = cls.test_dir_base_quotes + '/data/quotes.json'
         cls.quotes_test_file_2path  = cls.test_dir_base_quotes + '/data/quotes_2.json'
         cls.history_test_file_1path  = cls.test_dir_base_history + '/data/history.json'
         
    @classmethod
    def tearDownClass(cls):
         """Удаляет тестовую директорию после всех тестов."""
         shutil.rmtree('tests/data_test')
    
    def setUp(self):
         """Подготавливает окружение перед каждым тестом."""
         pass

    def tearDown(self):
          """Восстанавливает окружение после каждого теста."""
          pass

    def test_add_quote_success(self):
          """Тест успешного добавления новой цитаты."""
          test_text_1  ="Test quote one."
          test_author_1="Test Author One"
          
          result_1  = add_quote(text=test_text_1 , author=test_author_1 , topic="Test Topic")
          
          self.assertTrue(result_1 , msg="Функция add_quote должна возвращать True при успехе.")
          
          loaded_quotes_1  = load_quotes(custom_path=self.quotes_test_file_1path )
          
          quote_found_1  =(loaded_quotes_1 is not None and len(loaded_quotes_1)>0 and loaded_quotes_1[-1]['text']==test_text_1 and loaded_quotes_1[-1]['author']==test_author_1 )
          
          self.assertTrue(quote_found_1 , msg="Добавленная цитата не найдена в файле.")
    
    def test_add_quote_validation_error_empty_text(self):
          """Тест валидации при пустом тексте."""
          with self.assertRaises(ValueError , msg="Пустой текст должен вызывать ValueError."):
               add_quote(text="" , author="Test Author" , topic="Test")
    
    def test_get_random_quote_success(self):
          """Тест получения случайной цитаты из непустого списка."""
          save_quotes([{"text":"A","author":"B","topic":"C"}] , custom_path=self.quotes_test_file_2path )
          
          loaded_quotes_2  =(load_quotes(custom_path=self.quotes_test_file_2path ) or [])
          
          random_quote_2  =(get_random_quote(loaded_quotes_2))
          
          self.assertIsNotNone(random_quote_2 , msg="Случайная цитата из непустого списка не должна быть None.")
    
    def test_get_random_quote_empty_list(self):
          """Тест получения случайной цитаты из пустого списка."""
          empty_list=[]
          
          random_quote_empty=(get_random_quote(empty_list))
          
          self.assertIsNone(random_quote_empty , msg="Случайная цитата из пустого списка должна быть None.")
    
    def test_filter_by_author_case_insensitive(self):
          """Тест фильтрации по автору без учета регистра."""
          test_data=[{"text":"T1","author":"John Doe","topic":"T"},{"text":"T2","author":"Jane Doe","topic":"T"}]
          
          save_quotes(test_data , custom_path=self.quotes_test_file_2path )
          
          loaded_data=(load_quotes(custom_path=self.quotes_test_file_2path ) or [])
          
          filtered=(filter_quotes_by_author(loaded_data , "john doe"))
          
          expected_len=(len([q for q in test_data if q['author'].lower()=='john doe']))
          
          self.assertEqual(len(filtered), expected_len , msg="Фильтрация по автору должна быть регистронезависимой.")
    
    def test_save_and_load_history(self):
          """Тест сохранения и загрузки истории."""
          history_data=[{"text":"H1","author":"A1","topic":"T1"}]
          
          save_history(history_data , custom_path=self.history_test_file_1path )
          
          loaded_history=(load_history(custom_path=self.history_test_file_1path ) or [])
          
          history_found=(len(loaded_history)>0 and loaded_history[0]['text']=="H1")
          
          self.assertTrue(history_found , msg="История не была корректно сохранена или загружена.")
