#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./app.py [<port>]
"""
from http.server import SimpleHTTPRequestHandler , HTTPServer
import logging


def run(server_class=HTTPServer, handler_class= SimpleHTTPRequestHandler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting .... \n service running on http://localhost:'+str(port)+'...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
