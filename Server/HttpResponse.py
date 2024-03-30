class HttpResponse:
    def __init__(self, host, accept, http_code, body):
        self.host = host
        self.accept = accept
        self.http_code = http_code
        self.body = body
