from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
            return

        # Обработка статических файлов (CSS/JS)
        if self.path.startswith('/css/') or self.path.startswith('/js/'):
            try:
                file_path = '.' + self.path  # Относительный путь
                with open(file_path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/css' if self.path.endswith('.css') else 'application/javascript')
                self.end_headers()
                self.wfile.write(content)
                return
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                return

        # Основная страница
        try:
            with open('contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Сервер запущен на http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
