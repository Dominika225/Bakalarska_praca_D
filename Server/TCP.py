import socket
import datetime
import json
import time
import HttpResponse
import HttpRequest
import Arguments_S
from HttpServer import HttpServer

class TCPClient:
    def __init__(self, client_id, client_ip, timeout=10):
        self.client_id = client_id
        self.client_ip = client_ip
        #self.timeout = timeout


class TCPServer:
    def __init__(self, host, port, max_clients=1, max_data_recv=512, ip_version = 4):
        #self.protocol = protocol # vyberiem aky protokol budem pouzivať
        self.host = Arguments_S.parser.host  # ulozim si IP adresu servera
        self.port = Arguments_S.parser.port  # ulozim si port na ktorom budem pocuvat na spojenia
        self.ip_version = (ip_version)
        self.max_clients = max_clients  # kolko clientov sa maximalne moze pripojit, zatial max=1
        self.max_data_recv = max_data_recv  # kolko dat mozem maximalne poslat, zatial to je 1024 bytov
        self.clients = []  # pole na ulkladanie jednotlivych klientov
        self.empty_id = "client_0x0"  # unikatne ID pre klienta
        self.sock = None  # referencia na SOCK objekt ktory zabezpeci komunikaciu

    @staticmethod
    def print_info(message):
        # tato dunkcia vypise cas a lubovlmu spravu ktora pride ako argument "message"
        curr_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{curr_date}] {message}")


    #def protocol(self):

    def server_configuration(self):
        # tato funkcia nastavi server bud ipv6 alebo ipv4
        if self.ip_version == 6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)  # vytvorim objekt typu SOSCKET
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind((self.host, self.port))
        self.print_info(f"Server je naviazany na: \n\t IP-> {self.host} \n\t PORT-> {self.port}")


    def handle_client(self, sock, adress, client):
        # tato funkcia zabezpeci komunikaciu s klientom
        # try block je pre pripad ze nastane chyba
        try:
            data_enc = sock.recv(64)  # cakam na prichadzajuce data od klient
            data_len = int(data_enc.decode().strip())  # dekodujem data ktore prisli od klienta na STRING
            encoded_message = b""
            position = 0

            while data_len > len(encoded_message):
              chunk = sock.recv(512)
              if not chunk:
                  break
              encoded_message += chunk

              position += 512

              if position >= data_len:
                  break

            #decode message
            decoded_message = encoded_message.decode('utf-8')
            http_request = json.loads(decoded_message)

            self.print_info(f"[REQUEST od {client.client_id} je: {decoded_message}]")  # vypis do konzoly
            self.print_info(f"[RESPONSE ku {client.client_id} je: {response}]")  # vypis do konzoly ??????

            response = HttpServer.handleRequest(http_request)
            sock.sendall(str(len(response)).encode('utf-8'))
            sock.sendall(response.encode('utf-8'))

            # vypise sa ak klient prerusi spojenie
            self.print_info(f"The connection was terminated by the client {adress}")
            # teda while concision

            # ak nastane chyba, tu sa zachyti a vypise
        except OSError as error:
            self.print_info(f"Error: {error}")

        finally:
            # tento block sa spusti na konci a skonci komunikaciu s klientom
            sock.close()  # ukonci sa spojenie s klientom
            self.print_info(f"Client socket {adress} was closed.")

    def shutdown_server(self):
        # tato funkcia zrusi SERVER pri ctrl+s
        self.print_info("Server operation was terminated.") #Prevádzka servera bola ukončená
        self.sock.close()

    def waiting_for_client(self):
        # tato funkcia caka na klienta
        self.print_info("Cakam na spojenia...")

        # waiting for client
        try:
            self.sock.listen(self.max_clients)  # caka kym sa nepripoji klient

            client_sock, client_adress = self.sock.accept()  # akceptuje spojenie s klientom
            self.print_info(f"Spojenie naviazané s {client_adress}")
            new_client = TCPClient(self.get_new_id(), client_adress)  # tato trieda drzi informacie o klientovi
            # ako ID a socket adresu, nie je az tak podstatna ked budu potrebny viacery klienti
            self.clients.append(new_client)  # pridanie klienta do pola, nie je podstatne
            self.handle_client(client_sock, client_adress, new_client)  # zavola sa funkcia ktora zabezpeci
            # komunikaciu s klientom

        except KeyboardInterrupt:
            self.shutdown_server()
