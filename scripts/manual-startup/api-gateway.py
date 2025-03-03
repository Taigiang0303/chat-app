#!/usr/bin/env python
"""
Simple API Gateway for Chat Application
This script creates a basic API Gateway that routes requests to the appropriate microservices.
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import json
import sys
from urllib.parse import urlparse, parse_qs

# Service endpoints
SERVICE_ROUTES = {
    '/api/auth': 'http://localhost:8001',
    '/api/chat': 'http://localhost:8002',
    '/api/notifications': 'http://localhost:8003',
}

class APIGatewayHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def route_request(self, method):
        # Parse the URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query

        # Find the appropriate service
        target_service = None
        for route, service_url in SERVICE_ROUTES.items():
            if path.startswith(route):
                target_service = service_url
                service_path = path[len(route):]
                if not service_path.startswith('/'):
                    service_path = '/' + service_path
                break

        # If no service found, return 404
        if not target_service:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Service not found'}).encode())
            return

        # Construct the target URL
        target_url = f"{target_service}{service_path}"
        if query:
            target_url += f"?{query}"

        print(f"Routing {method} request from {path} to {target_url}")

        # Get request body for POST/PUT requests
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Create the request
        req = urllib.request.Request(
            target_url,
            data=body,
            headers={k: v for k, v in self.headers.items() if k.lower() not in ['host', 'content-length']},
            method=method
        )

        try:
            # Forward the request
            with urllib.request.urlopen(req) as response:
                # Copy the response status and headers
                self.send_response(response.status)
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding', 'connection']:
                        self.send_header(header, value)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                # Copy the response body
                self.wfile.write(response.read())

        except urllib.error.HTTPError as e:
            # Handle HTTP errors from the target service
            self.send_response(e.code)
            for header, value in e.headers.items():
                if header.lower() not in ['transfer-encoding', 'connection']:
                    self.send_header(header, value)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(e.read())

        except Exception as e:
            # Handle other errors
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_GET(self):
        self.route_request('GET')

    def do_POST(self):
        self.route_request('POST')

    def do_PUT(self):
        self.route_request('PUT')

    def do_DELETE(self):
        self.route_request('DELETE')

def run_server(port=8000):
    server_address = ('', port)
    httpd = socketserver.TCPServer(server_address, APIGatewayHandler)
    print(f"Starting API Gateway on port {port}...")
    print(f"Routes configured:")
    for route, service in SERVICE_ROUTES.items():
        print(f"  {route} -> {service}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port) 