class HttpRequest:
  def __init__(self, method, endpoint, host, body, protocol = "HTTP/1.1",):
    self.method = method
    self.endpoint = endpoint
    self.protocol = protocol
    self.host = host
    self.body = body