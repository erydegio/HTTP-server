import socket
import signal
import sys
from threading import Thread
from tracemalloc import start

class TCPServer:

    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
    
    def async_start(self):
        thread = Thread(target = self.start, args = ())
        thread.daemon = True

        thread.start()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.listen(5)
                print("Listening at", s.getsockname())
                while True:
                    print("Waiting for connections..")
                    conn, addr = s.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        data = conn.recv(1024)
                        response = self.handle_request(data)
                        conn.sendall(response)
                        print(data)
            except Exception as e:
                print(e)
                pass


def handle_request(self, data):
    return data


class HTTPServer(TCPServer):
    headers = {
        "Server": "TomorrowDevs Server",
        "Content-Type": "text/html",
    }
    status_codes = {
        200: "OK",
        501: "Not Implemented",
    }

    def handle_request(self, data):
        request = HTTPRequest(data)
        try:
            handler = getattr(self, f"handle_{request.method}")
        except AttributeError:
            handler = self.handle_unknown_method

        response = handler(request)

        return response

    def handle_unknown_method(self, request):
        response_line = self.response_line(status_code=501)
        response_headers = self.response_headers()
        blank_line = b"\r\n"
        response_body = b"<h1>501 Not Implemented</h1>"
        return b"".join([response_line, response_headers, blank_line, response_body])

    def handle_GET(self, request):
        response_line = self.response_line(status_code=200)
        response_headers = self.response_headers()
        blank_line = b"\r\n"
        response_body = b"""
            <html>
                <body>
                    <h1>Hi, I'm TomorrowDevs Server!</h1>
                </body>
            </html>
            """
        return b"".join([response_line, response_headers, blank_line, response_body])

    def response_line(self, status_code):
        line = f"HTTP/1.1 {status_code} {self.status_codes[status_code]}"
        return line.encode()

    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy()
        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""
        for h in headers:
            headers += f"{h}:{headers_copy[h]}"
        return headers.encode()


class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.1"
        self.parse(data)

    def parse(self, data):
        lines = data.split(b"\r\n")
        request_line = lines[0]
        words = request_line.split(b" ")
        self.method = words[0].decode()

        if len(words) > 1:
            self.uri = words[1].decode()
        if len(words) > 2:
            self.http_version = words[2]


if __name__ == "__main__":
    server = HTTPServer()

    server.async_start()
    
    def signal_handler(sig, frame):
        print('Stopping...')
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    input('Press Ctrl+C to stop the server')