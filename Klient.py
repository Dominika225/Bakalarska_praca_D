import socket
import json
from HttpRequestCl import HttpRequest
# import Arguments_C from Arguments_C

HOST = "127.0.0.1"
PORT = 65433
# TIMEOUT = 10
# MESSAGE_SIZE = 1024  # Maximálna veľkosť správy pre recv


if __name__ == "__main__":

    if HOST == "::1":
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)  # vytvorim objekt typu SOSCKET
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # s.settimeout(TIMEOUT)
    user_data = HttpRequest(host="120", endpoint="/kti", method="GET")
    serialized_user_data = json.dumps(user_data)

    try:
        s.connect((HOST, PORT))  # pripojim sa na server
        s.sendall(str(len(serialized_user_data)).encode('utf-8'))

        if len(user_data) == 0:  # ak nezadam nic a stlacim iba enter, vtedy je problem preto sa namiesto prazdneho STRINGU posle "exit" aby server vedel ze chcem prerusit spojenie
            user_data = "exit"
        s.sendall(user_data.encode(
            'utf-8'))  # poslem zakodovane data, nemozem poslat cisto STRING, je to potreba premenit na BYTE

        data = s.recv(1024)  # cakam na prichadzajuce data

        print('DATA uncensored:', data)
        length = data.decode()
        print('Dlzka incoming spravy:', length)
        data = s.recv(int(length))  # cakam na prichadzajuce data
        print('Odpoved od servera:', data.decode())


    finally:
        s.close()  # Ujistím sa, že socket je vždy zatvorený
