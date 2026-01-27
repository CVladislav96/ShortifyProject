#!/usr/bin/env python3
"""
Simple development server for Shortify frontend.
Serves static files and routes all requests to index.html for SPA routing.
"""

import os
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class SPAHandler(SimpleHTTPRequestHandler):
    """Handler that routes all requests to index.html for SPA routing support."""
    
    def do_GET(self):
        # Get the file path
        path = self.translate_path(self.path)
        
        # Check if it's a static file with an extension
        if os.path.isfile(path):
            # Serve the file
            return super().do_GET()
        
        # Check if it's a directory
        if os.path.isdir(path):
            # Try to serve index.html from the directory
            index_path = os.path.join(path, 'index.html')
            if os.path.isfile(index_path):
                self.path = os.path.join(self.path, 'index.html').replace('\\', '/')
                return super().do_GET()
        
        # For all other requests (SPA routes), serve index.html
        self.path = '/index.html'
        return super().do_GET()
    
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        return super().end_headers()


def run_server(port=8080):
    """Run the development server."""
    # Change to the frontend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the server
    server_address = ('', port)
    httpd = HTTPServer(server_address, SPAHandler)
    
    print(f'🚀 Starting Shortify frontend dev server on http://localhost:{port}')
    print(f'📁 Serving files from: {os.getcwd()}')
    print(f'ℹ️  All requests will route through index.html for SPA routing')
    print(f'⛔ Press Ctrl+C to stop the server\n')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n\n✅ Server stopped')
        httpd.server_close()


if __name__ == '__main__':
    run_server(port=8080)
