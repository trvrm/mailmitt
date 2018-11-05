import asyncio
from aiohttp import web
import argparse

from . import smtp_server
from . import web_server
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--smtp-ip', default='127.0.0.1', metavar='IP', help='SMTP ip (default: 127.0.0.1)')
    parser.add_argument('--smtp-port', default=1025, type=int, metavar='PORT', help='SMTP port (deault: 1025)')
    parser.add_argument('--http-ip', default='127.0.0.1', metavar='IP', help='HTTP ip (default: 127.0.0.1)')
    parser.add_argument('--http-port', default=1080, type=int, metavar='PORT', help='HTTP port (deault: 1080)')
    args = parser.parse_args()
    
    loop    = asyncio.get_event_loop()
    loop.run_until_complete(
        loop.create_server(
            smtp_server.factory,
            host=args.smtp_ip,
            port=args.smtp_port
        )
    )
    web.run_app(
        web_server.app,
        host=args.http_ip,
        port=args.http_port
    )
    
if __name__=='__main__':
    main()