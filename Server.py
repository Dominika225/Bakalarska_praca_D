import argparse
import socket
import TCP
                                                # from LoggerFactory import LoggerFactory
                                                   # import logging

HOST = TCP.TCPServer.host
PORT = TCP.TCPServer.post



if __name__ == "__main__":
    #logger = LoggerFactory.get_logger()
    #logger.debug('This message should go to the log file')
    # logger.info('So should this')
    #logger.warning('And this, too')
    #logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
    # logger.critical('Critical message from the moon')

    print(f'port {TCP.TCPServer}.')
    tcp_server = TCP(HOST,PORT)  # vytvorim objekt, teda nas server
    tcp_server.server_configuration()  # nastavim ho na spravnu IP a PORT
    #tcp_server.waiting_for_client()  # zacnem cakat na pripojenie klienta
