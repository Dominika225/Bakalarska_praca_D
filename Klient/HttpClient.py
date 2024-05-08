import socket
import json
from Http.HttpRequest import HttpRequest
from Http.HttpResponse import HttpResponse


class HttpClient:

    def __init__(self, arguments):
        # vytvorim objekt typu SOSCKET
        if str.__contains__(arguments.host, ":"):
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        self.socket.settimeout(arguments.timeout)

    def get_host(self):
        # zatvorim socket so serverom
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    def open_connection(self, host, port):
        # pripojim sa na server
        self.socket.connect((host, port))

    def close_connection(self):
        # zatvorim socket so serverom
        self.socket.close()

    def send_message(self, http_request):
        # serializujem http request na string
        serialized_http_request = json.dumps(http_request, default=HttpRequest.encoder_request)
        # poslem dlzku http requestu
        self.socket.sendall(str(len(serialized_http_request)).zfill(8).encode('utf-8'))
        # poslem http request v json formate
        # poslem zakodovane data, nemozem poslat cisto STRING, je to potreba premenit na BYTE
        self.socket.sendall(serialized_http_request.encode('utf-8'))  

    def receive_message(self):  
        # cakam na prichadzajuce data od klienta
        data_enc = self.socket.recv(8)
        # dekodujem data ktore prisli od klienta na STRING
        data_len = int(data_enc.decode().strip())
        encoded_message = b""
        position = 0

        # citam data po 512 bytoch pokial nenacitam vsetky data
        while data_len > len(encoded_message):
            chunk = self.socket.recv(512)
            if not chunk:
                break
            encoded_message += chunk

            position += 512

            if position >= data_len:
                break

        # decodujem spravu zo stringu na http response
        decoded_message = encoded_message.decode('utf-8')
        return json.loads(decoded_message)
