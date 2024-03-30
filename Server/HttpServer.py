from HttpRequest import HttpRequest
from HttpResponse import HttpResponse
import time
import socket
import json

@classmethod
class HttpServer():
    @staticmethod
    def handleRequest(request, sock):
        response = HttpResponse()

        if request.method == "GET" and request.endpoint == "/":
            # nieco urobim
            time.sleep(3)
            response.http_code = 200
            backdata = {"message": "Here´s your data"}
            response.body = json.dumps(backdata)

        elif request.method == "POST" and request.endpoint == "/":
            time.sleep(3)
            response.http_code = 200
            content_length = int(request.headers.get('Content-Length', 0))
            post_data = request.body
            backdata = {"message": "Here's your data for POST", "received_data": post_data}
            response.body = json.dumps(backdata)

        else:
            errormessage = {"Error": "Nothing to see here"}
            response.http_code = 404
            print(response.http_code)
            json_error = json.dumps(errormessage)


        response_data = response.body.encode('utf-8')
        sock.sendall(str(len(response_data)).encode('utf-8') + b'\n')
        sock.sendall(response_data) # posielanie dat
        # posielanie dat klientovi, ktore su zakodovane do typu
        # utf-8
        return response

