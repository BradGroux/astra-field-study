#!/usr/bin/env python3
"""Serve the public evidence package locally, including working source-data links."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

CASE=Path(__file__).resolve().parents[1]/'evidence/study-0001-v1'


class ReaderHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        path=urlsplit(self.path).path
        aliases={'/':'/reader/explorer.html','/explorer.html':'/reader/explorer.html'}
        if path in aliases:
            self.send_response(302)
            self.send_header('Location',aliases[path])
            self.end_headers()
            return
        super().do_GET()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8767)
    args=parser.parse_args()
    handler=partial(ReaderHandler,directory=str(CASE))
    with ThreadingHTTPServer(('127.0.0.1',args.port),handler) as server:
        print(f'Public evidence preview: http://127.0.0.1:{args.port}/reader/explorer.html',flush=True)
        try:server.serve_forever()
        except KeyboardInterrupt:pass

if __name__=='__main__':main()
