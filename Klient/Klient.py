from Http.HttpRequest import HttpRequest
from Http.HttpResponse import HttpResponse
from Http.HttpClient import HttpClient
from Logger.LoggerFactory import LoggerFactory
from Arguments import Arguments
import time


if __name__ == "__main__":
    # vytvorim si logger
    logger = LoggerFactory.create_logger(__name__)
    
    # vyextrahujem argumenty a ulozim si ich do args
    args = Arguments.parse_arguments()

    # vytvorim http clienta - instancia tiedy
    http_client = HttpClient(arguments=args)
        
    # vytvorim http request s parametrami h,endp,m,b
    http_request = HttpRequest(
        host=http_client.get_host(),
        endpoint=args.endpoint,
        method=args.method,
        body=args.body)

    try:
        # zaznamenam si zaciatok
        start_time = time.time()
        # otvaram pripojenie na server a posielam/prijimam spravu
        http_client.open_connection(args.host, args.port)

        for _ in range(args.repeat):
            # odosielam HTTP poziadavku
            http_client.send_message(http_request)
            # prijimanie odpovede
            http_response: HttpResponse = http_client.receive_message()
        # zaznamenam si koniec

            logger.debug(f'HTTP \'{args.method}\' request on \'{args.endpoint}\' elapsed {time.time() - start_time} seconds.')
            logger.debug(f'HTTP response: {http_response["http_code"]} Message: {http_response["body"]}')
        end_time = time.time()
        logger.info(f"Total elapsed time for {args.repeat} requests: {end_time - start_time} seconds")
    except Exception as e:
        logger.error(f"Communication failed due to: {e}")
    finally:
        # Ujistim sa, že socket je vzdy zatvoreny
        http_client.close_connection()
