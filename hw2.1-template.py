import socket
import time
from email.utils import formatdate, parsedate_to_datetime

# Cache dictionary to store responses with their last modified times
cache = {}

def create_http_response(status_code, body, last_modified=None):
    """
    Implement the HTTP response formatting.

    Parameters:
        status_code (int): The HTTP status code to return.
        body (str): The body of the response.
        last_modified (str): The string representation of the last modified time,
                             formatted as an RFC 2822 date string.
    
    Returns:
        bytes: The complete HTTP response in bytes, ready to be sent over the network.
    
    Example of a formatted last_modified string: 'Tue, 15 Nov 1994 12:45:26 GMT'
    This is the standard format for HTTP date/time values.
    """
    # TO DO: Create the complete HTTP response including status line, headers, and body.
    # Use the provided parameters: status_code, body, last_modified
    # Ensure to properly format the Last-Modified header using the example format.
    pass

def handle_if_modified_since(request_headers, path):
    """ Handle the If-Modified-Since header to determine if a 304 response should be returned. """
    # TO DO: Implement the handling of If-Modified-Since header.
    # Parse the If-Modified-Since header value and compare with the cached last_modified time.
    pass

def main():
    HOST, PORT = 'localhost', 45411  # Server configuration
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Serving HTTP on port {PORT} ...")

    try:
        while True:
            client_connection, client_address = server_socket.accept()
            request = client_connection.recv(1024).decode('utf-8')
            request_headers = request.split('\r\n')
            first_line = request_headers[0]
            parts = first_line.split()

            # TO DO: Implement the logic to check the request method and path, handle GET requests and If-Modified-Since.
            
            client_connection.close()
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
