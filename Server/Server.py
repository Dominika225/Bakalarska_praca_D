from Http.HttpServer import HttpServer
from TCPServer import TCPServer
from Arguments import Arguments
from UDP_S import UDPServer

if __name__ == "__main__":

    # extrahujem argumenty
    args = Arguments.parse_arguments()
    
    if args.protocol == 'TCP':
        http_server = TCPServer(args.host, args.port, max_data_recv=args.max_data, ip_version=args.ip_version,
                                max_clients=args.max_clients)
    else:
        htt_server = UDPServer(args.host, args.port, max_data_recv=args.max_data, ip_version=args.ip_version)
                                # max_clients=args.max_clients)
    
    try:
        http_server.waiting_for_client()
    except:
        print("Something is not right!!!")
