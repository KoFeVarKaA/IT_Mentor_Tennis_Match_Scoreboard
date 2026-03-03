import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import unittest
import requests

from http.server import HTTPServer
from server import Server  
from src.roters.roter import controller_factory 

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Запускаем сервер перед выполнением тестов."""
        cls.host = 'localhost'
        cls.port = 8000 
        cls.server = HTTPServer(
            (cls.host, cls.port),
            lambda *args, **kwargs: Server(controller_factory(), *args, **kwargs)
        )
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True  
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        """Останавливаем сервер после выполнения тестов."""
        cls.server.shutdown()
        cls.server.server_close()

    def test_index(self):
        """GET запрос по адресу "/", ожидаем положительный код ответа."""
        url = f"http://{self.host}:{self.port}/"
        response = requests.get(url)
        self.assertTrue(response.ok, f"Ошибка: {response.status_code}")

    def test_matches(self):
        """GET запрос по адресу "/matches", ожидаем положительный код ответа."""
        url = f"http://{self.host}:{self.port}/matches?page=1"
        response = requests.get(url)
        self.assertTrue(response.ok, f"Ошибка: {response.status_code}")
    
    def test_new_match(self):
        """GET запрос по адресу "/new-match", ожидаем положительный код ответа."""
        url = f"http://{self.host}:{self.port}/new-match"
        response = requests.get(url)
        self.assertTrue(response.ok, f"Ошибка: {response.status_code}")
    

if __name__ == "__main__":
    unittest.main()