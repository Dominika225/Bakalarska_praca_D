#import argparse
from argparse import ArgumentParser, Namespace

parser = ArgumentParser()

if __name__ == "__main__":
    parser.add_argument('-ht', '--host', dest='host', help='IP address', type=str, default="127.0.0.1")
    parser.add_argument('-pt', '--port', dest='port', help='Port server', type=int, default=65432)
    parser.add_argument('-m', '--method', dest='method', help='POST, GET, PUT, DELETE', type=str, default= "GET")
#parser.add_argument('-to', '--to', dest='timeout', help='Čas, po ktorý sa klient pokúša o spojenie ', type=int, default=60)
# parser.add_argument('-rpt', '--repeat', dest='repeat', help='Opakovanie poslania spravy ak je veľkosť vacsia ako u servera ', type=int, default=1024)
# --- Ak budem poznat velkost spravy u oboch

args: Namespace = parser.parse_args()

print(args.host)
print(args.port)
print(args.method)
