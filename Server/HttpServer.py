from Http.HttpRequest import HttpRequest
from Http.HttpResponse import HttpResponse
import time
import json


class HttpServer():
        
    def handle_request(self, request: HttpRequest):
        response = HttpResponse(accept="json/application+json", host="host-ip-todo", body=None, http_code="200")

        # https://peps.python.org/pep-0636/

        match request["method"]:
            case "GET":
                match request["endpoint"]:
                    case "/":
                        # urob nieco
                        response.body = '{Here´s your data KTI}'
                        response.http_code = "200"
                        pass
                    case "/data":
                        # vrat data
                        response.body = '{Here is your data: Test report KTI.}'
                        response.http_code = "200"
                        pass
            
            case "POST":
                match request["endpoint"]:
                    case "/data":
                        # nastav data
                        response.body = '{Here your data for POST: Test report KTI}'
                        response.http_code = "201"
                        pass
            
        return response

"""
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

        return response
"""
