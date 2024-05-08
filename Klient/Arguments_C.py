from argparse import ArgumentParser


class Arguments:

    @staticmethod
    def parse_arguments():
        # vytvorim parser
        parser = ArgumentParser()
        # argumenty parsera
        parser.add_argument('-ht', '--host', dest='host',
                            help='IP address', type=str, default="127.0.0.1")
        parser.add_argument('-pt', '--port', dest='port',
                            help='Server port', type=int, default=65432)
        parser.add_argument('-m', '--method', dest='method',
                            help='POST, GET', type=str, default="GET")
        parser.add_argument('-e', '--endpoint', dest='endpoint',
                            help='Method endpoint', type=str)
        parser.add_argument('-b', '--body', dest='body',
                            help='Method body', type=str, default="KTI")
        parser.add_argument('-t', '--timeout', dest='timeout',
                            help='Time the client tries to connect.', type=int,default=60)
        parser.add_argument('-p', '--protocol', dest='protocol',
                            help='Protocol TCP or UDP', type=str, default='TCP')
        parser.add_argument('-d', '--max_data', dest='max_data',
                            help='Maximum number of data', type=int, default=1024)
        parser.add_argument('-r', '--repeat', dest='repeat',
                            help='Repeating the request.', type=int, default=1)

        # parsujem argumenty
        args = parser.parse_args()
        # validajem argumenty
        Arguments.validate_arguments(args)
        return args
    
    @staticmethod
    def validate_arguments(args):
        valid_method = ["GET", "POST"]
        valid_protocol = ["TCP", "UDP"]
        if args.method not in valid_method:
            raise Exception("INVALID: Method is not in proper form")
        if args.max_data not in range(0, 65535) and valid_protocol == "TCP":
            raise Exception("INVALID: The maximum size of a TCP packet is 65535 [64K]")
        if args.protocol not in valid_protocol:
            raise Exception("INVALID: Protocol is not in proper form.")
        pass
