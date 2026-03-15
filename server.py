from http.server import BaseHTTPRequestHandler
import json
import logging
import mimetypes
import os
from urllib.parse import parse_qs, urlparse
from src.response import Responses
from src.view.render import Render

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Принимаем, обрабатываем запрос, отдаем контроллеру
class Server(BaseHTTPRequestHandler):
    def __init__(self, controllers: dict, *args, **kwargs):
        self.controllers = controllers
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        return

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-commands', 'GET,POST,PATCH,OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def do_GET(self):
        self._process_request("GET")

    def do_POST(self):
        self._process_request("POST")

    def do_PATCH(self):
        self._process_request("PATCH")

        
    # Заменить command на self.command
    def _process_request(self, command: str):
        logging.debug(f"{self.command} {self.client_address}{self.path}")
        parsed_url = urlparse(self.path)
        path = parsed_url.path.split("/")
        query = parse_qs(parsed_url.query)
        content_length = int(self.headers.get('Content-Length', 0))
        data = parse_qs(self.rfile.read(content_length).decode('utf-8'))

        if path[1] in ("css", "js", "images", "favicon.ico"):
            self._send_response_static()
            return

        if path[1] not in self.controllers:
            message = "К сожалению, сервер не обрабатывает запросы по данному адресу"
            self._send_response(Responses.initial_err(message))
            return
        
        handle_class = self.controllers[path[1]]
        if  command == "GET":
            response = handle_class.do_GET(path, query)
        elif command == "POST":
            response = handle_class.do_POST(path, query, data)
        self._send_response(response)

    def _send_response(self, response: dict):
        if 200 <= response["status_code"] <= 201:
            logging.info("Запрос успешно выполнен")
        
        elif 301 <= response["status_code"] <= 308:
            self.send_response(response["status_code"])
            self.send_header("Location", response["url"])
            self.end_headers()
            return
        else:
            logging.error("Ошибка в ходе выполения запроса")

        self.send_response(response["status_code"])
        self.send_header("Content-Type", "text/html")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(response["data"])
    
    def _send_response_static(self):
        file_path = os.path.join("src/view/static", self.path.lstrip("/"))

        if not os.path.isfile(file_path):
            message = "Статичный файл не найден"
            logging.error(message)
            response = Responses.initial_err(message)
            self.send_response(response["status_code"])
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"code": str(response["status_code"]), 
                        "status": "Ошибка", 
                        "message": response["data"]["message"]}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"  

        # logging.info("Запрос успешно выполнен")
        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        with open(file_path, "rb") as file:
            self.wfile.write(file.read())