from dataclasses import dataclass


@dataclass
class HttpRequest:
    method: str
    endpoint: str
    host: str
    body: str
    protocol: str = "HTTP/1.1"
    
    def encoder_request(request):
        if isinstance(request, HttpRequest):
            return {'method': request.method,
                    'endpoint': request.endpoint,
                    'host': request.host,
                    'body': request.body,
                    'protocol': request.protocol}
