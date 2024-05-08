import logging
import socket
import time
import datetime
import json
import timeit

from Http.HttpServer import HttpServer
from Http.HttpRequest import HttpRequest
from Http.HttpResponse import HttpResponse
from Logger.LoggerFactory import LoggerFactory


logger = LoggerFactory.create_logger(__name__)

class TCPClient:
    def __init__(self, client_id, client_ip, timeout=10):
        self.client_id = client_id
        self.client_ip = client_ip


class TCPServer:
    def __init__(self, host, port, max_clients, max_data_recv, ip_version):
        # self.protocol = protocol # vyberiem aky protokol budem pouzivať
        self.host = host  # ulozim si IP adresu servera
        self.port = port  # ulozim si port na ktorom budem pocuvat na spojenia
        self.ip_version = ip_version
        self.max_clients = max_clients  # kolko clientov sa maximalne moze pripojit, zatial max=1
        self.max_data_recv = max_data_recv  # kolko dat mozem maximalne poslat, zatial to je 1024 bytov
        self.clients = []  # pole na ulkladanie jednotlivych klientov
        self.empty_id = "client_0x0"  # unikatne ID pre klienta
        self.http_server = HttpServer()
        
        # vytvorim objekt typu SOSCKET

        if self.ip_version == 6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind((self.host, self.port))
        logger.info(f"Server is running on: \n\t\t\t\t\t\t IP-> {self.host} \n\t\t\t\t\t\t PORT-> {self.port}")


    def handle_client(self, sock, adress, client):
        # tato funkcia zabezpecuje komunikaciu s klientom
        # try block - nastane chyba
        try:
            while True:
                request = self.__receive_request_message(sock)
                #  if request == "quit":
                #   break
                response = self.__handle_message(request)
                self.__send_response_message(sock, response)

                # vypise sa ak klient prerusi spojenie
                logger.debug(f"The connection was terminated by the client {adress}")

            # ak nastane chyba, tu sa zachyti a vypise
        except OSError as error:
            logger.error(f"Error: {error}")

        finally:
            # tento block sa spusti na konci a skonci komunikaciu s klientom
            sock.close()  # ukonci sa spojenie s klientom
            logger.info(f"Client socket {adress} was closed.")

    def __receive_request_message(self, socket):

        start_time = time.time()

        data_enc = socket.recv(8)  # cakam na prichadzajuce data od klient
        data_len = int(data_enc.decode())  # dekodujem data ktore prisli od klienta na STRING
        encoded_message = b""
        position = 0

        while data_len > len(encoded_message):
            chunk = socket.recv(self.max_data_recv)
            if not chunk:
                break
            encoded_message += chunk

            position += self.max_data_recv

            if position >= data_len:
                break

        end_time = time.time()

        logger.debug(f"Data - length: \'{data_len}\' bytes.")
        logger.debug(f"Time elapsed: \'{(end_time - start_time)}\' seconds.")

        # decode message
        decoded_message = encoded_message.decode('utf-8')
        return json.loads(decoded_message)

    def __handle_message(self, request):
        return self.http_server.handle_request(request)

    def __send_response_message(self, socket, response):
        serialized_response = json.dumps(response, default=HttpResponse.encoder_response)
        socket.sendall(str(len(serialized_response)).zfill(8).encode('utf-8'))
        socket.sendall(serialized_response.encode('utf-8'))

    def waiting_for_client(self):
        # tato funkcia caka na klienta
        logger.debug("Waiting for the client...")

        # waiting for client
        try:
            while True:
                self.sock.listen(self.max_clients)  # caka kym sa nepripoji klient

                client_sock, client_adress = self.sock.accept()  # akceptuje spojenie s klientom
                logger.debug(f"Connection established with {client_adress}")
                new_client = TCPClient("self.get_new_id()", client_adress)  # tato trieda drzi informacie o klientovi
                # ako ID a socket adresu, nie je az tak podstatna ked budu potrebny viacery klienti
                self.clients.append(new_client)  # pridanie klienta do pola, nie je podstatne
                # start_time = timeit.timeit()
                self.handle_client(client_sock, client_adress, new_client)  # zavola sa funkcia ktora zabezpeci
                # end_time = timeit.timeit()
                # komunikaciu s klientom

                # logger.debug(f"Total time: \'{(end_time - start_time)}\' seconds.")

        except KeyboardInterrupt:
            self.shutdown_server()
        except Exception as error:
            logger.error(f"Error")
            
    def shutdown_server(self):
        # tato funkcia zrusi SERVER pri ctrl+c
        logger.debug("Server operation was terminated.")  # Prevádzka servera bola ukončená
        self.sock.close()
