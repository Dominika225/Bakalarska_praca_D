from dataclasses import dataclass


@dataclass 
class HttpResponse:
    host: str
    accept: str
    http_code: str
    body: str
    
    def encoder_response(response):
        if isinstance(response, HttpResponse):
            return {'host': response.host,
                    'accept': response.accept,
                    'http_code': response.http_code,
                    'body': response.body}
