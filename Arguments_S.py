#import argparse
from argparse import ArgumentParser, Namespace


parser = ArgumentParser()

if __name__ == "__main__":
    #parser.add_argument('-m', '--mc', dest='max_clients', help='Maximum number of clients', type=int, default=1)
    # parser.add_argument('-d', '--md', dest='max_data', help='Maximum number of data', type=int, default=1024)
    parser.add_argument('-ht', '--host', dest='host', help='IP address', type=str, default="127.0.0.1")
    #parser.add_argument('-ipv', '--ip_version', dest='ip_version', type=int, choices=[4, 6], default=4,help='Verzia IP protocolu (4 alebo 6)')
    parser.add_argument('-pt', '--port', dest='port', help='Port server', type=int, default=65432)
    #parser.add_argument('-pl', '--proto', dest='protocol', help='UDP or TCP protocol', type=str, default="tcp")
    #parser.add_argument('-m', '--method', dest='method', help='HTTP POST, GET, PUT, DELETE', type=str, default= "GET")
    # parser.add_argument('-to', '--to', dest='timeout', help='Čas, po ktorý sa klient pokúša o spojenie ', type=int, default=60)
    # parser.add_argument('-r', '--repeat', dest='repeat', help='Opakovanie poslania spravy ak je veľkosť vacsia ako u servera ', type=int, default=1024)

args: Namespace = parser.parse_args()

#print(args.max_clients)
#print(args.max_data)
#print(args.host)
#print(args.port)
#print(args.ip_version)
#print(args.protocol)

