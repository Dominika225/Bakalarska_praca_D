from argparse import ArgumentParser


class Arguments:

    @staticmethod
    def parse_arguments():
        # vytvorim parser
        parser = ArgumentParser()
        # samotne argumenty parsera
        parser.add_argument('-ht', '--host', dest='host',
                            help='IP address', type=str, default="127.0.0.1")
        parser.add_argument('-pt', '--port', dest='port',
                            help='Port server', type=int, default=65432)
        parser.add_argument('-i', '--ip_version', dest='ip_version', type=int,
                            choices=[4, 6], default=4, help='Verzia IP protocolu (4 alebo 6)')
        parser.add_argument('-m', '--mc', dest='max_clients',
                            help='Maximum number of clients', type=int, default=1)
        parser.add_argument('-d', '--max_data', dest='max_data',
                            help='Maximum number of data', type=int, default=1024)
        parser.add_argument('-r', '--protocol', dest='protocol',
                            help='Protocol TCP or UDP', type=str, default='TCP')
        # parsujem argumenty
        args = parser.parse_args()
        # validajem argumenty
        Arguments.validate_arguments(args)
        return args

    @staticmethod
    def validate_arguments(args):
        valid_ip_version = [4, 6]
        valid_protocol = ["TCP", "UDP"]
        if args.ip_version not in valid_ip_version:
            raise Exception("INVALID: IP_version is not in proper form.")
        if args.max_data not in range(0, 65535) and valid_protocol == "TCP":
            raise Exception("INVALID: The maximum size of a TCP packet is 65535 [64K]")
        if args.protocol not in valid_protocol:
            raise Exception("INVALID: Protocol is not in proper form.")
        pass
