import logging
import socket
import time
import datetime
import json
from Http.HttpServer import HttpServer
from Http.HttpRequest import HttpRequest
from Http.HttpResponse import HttpResponse
from Logger.LoggerFactory import LoggerFactory

logger = LoggerFactory.create_logger(__name__)


class UDPClient:
    def __init__(self, client_id, client_ip, timeout=10):
        self.client_id = client_id
        self.client_ip = client_ip


class UDPServer:
    def __init__(self, host, port, max_data_recv, ip_version):
        self.host = host
        self.port = port
        self.max_data_recv = max_data_recv
        self.http_server = HttpServer()

        # Create a UDP socket
        if ip_version == 6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock.bind((self.host, self.port))
        logger.info(f"Server is running on: \n\t\t\t\t\t\t IP -> {self.host} \n\t\t\t\t\t\t PORT -> {self.port}")

    def handle_client(self, data, address):
        try:
            request = json.loads(data.decode('utf-8'))
            response = self.http_server.handle_request(request)
            serialized_response = json.dumps(response, default=HttpResponse.encoder_response)
            self.sock.sendto(serialized_response.encode('utf-8'), address)
        except OSError as error:
            logger.error(f"Error: {error}")
        finally:
            logger.info(f"Handled request from {address}")

    def waiting_for_client(self):
        logger.debug("Waiting for clients...")
        try:
            while True:
                data, client_address = self.sock.recvfrom(self.max_data_recv)
                logger.debug(f"Received data from {client_address}")
                self.handle_client(data, client_address)
        except KeyboardInterrupt:
            self.shutdown_server()
        except Exception as error:
            logger.error(f"Error: {error}")

    def shutdown_server(self):
        logger.debug("Server operation was terminated.")
        self.sock.close()

