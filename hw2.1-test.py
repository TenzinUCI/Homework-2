import requests
import time
import subprocess
import os
import sys
import socket

def run_server():
    """ Function to run the server script. """
    # Run the server script in a separate process
    if len(sys.argv) != 2:
        print("Usage: python hw2.1-test.py </path/to/your/server_script>")
        exit(1)

    server_script = sys.argv[1]
    if not os.path.exists(server_script):
        print(f"Error: {server_script} not found.")
        exit(1)
    process = subprocess.Popen(['python', server_script])

    # Wait for the server to start
    time.sleep(1)
    return process

def test_server_response():
    """ Function to test the HTTP responses from the server, focusing on If-Modified-Since caching. """
    print("Starting server tests...")
    
    root_url = 'http://localhost:45411/'  # URL of the server
    try:
        # Initial request to root path
        initial_response = requests.get(root_url)
        print("Testing root path...")
        if initial_response.status_code == 200 and initial_response.text.strip() == "Hello, World!":
            print("PASS: Root path returned 200 OK and 'Hello, World!'")
        else:
            print(f"FAIL: Root path response was incorrect, got {initial_response.status_code} and '{initial_response.text.strip()}'")

        # Request to a nonexistent path
        print("Testing 404 Not Found for nonexistent path...")
        nonexistent_url = root_url + 'nonexistent'
        response_404 = requests.get(nonexistent_url)
        if response_404.status_code == 404:
            print("PASS: Nonexistent path correctly returned 404 Not Found")
        else:
            print(f"FAIL: Nonexistent path returned {response_404.status_code}")

        # Request with unsupported method (POST)
        print("Testing 405 Method Not Allowed for POST request...")
        response_405 = requests.post(root_url)
        if response_405.status_code == 405:
            print("PASS: POST method correctly returned 405 Method Not Allowed")
        else:
            print(f"FAIL: POST method returned {response_405.status_code}")

        # Testing caching with If-Modified-Since
        print("Testing caching with If-Modified-Since...")
        last_modified = initial_response.headers.get('Last-Modified')
        headers = {'If-Modified-Since': last_modified}
        cached_response = requests.get(root_url,headers = headers)
        if cached_response.status_code == 304:
            print("PASS: Server correctly responded with 304 Not Modified when using If-Modified-Since")
        else:
            print(f"FAIL: Expected 304 Not Modified, got {cached_response.status_code}")

        # Testing cache expiration
        print("Testing cache expiration...")
        time.sleep(10.5)  # Wait longer than the cache TTL to ensure it has expired
        expired_response = requests.get(root_url)
        new_last_modified = expired_response.headers.get('Last-Modified')
        if new_last_modified != last_modified:
            print("PASS: Cache expiration confirmed, Last-Modified header changed")
        else:
            print("FAIL: Cache may not have expired correctly; Last-Modified did not change")

        # Testing 400 Bad Request for malformed request line
        print("Testing 400 Bad Request for malformed request...")
        with socket.create_connection(("localhost", 45411)) as s:
            s.sendall(b"GET /onlypath\r\n\r\n")  # Malformed request line (no HTTP version)
            response = s.recv(1024).decode()

        if "400 Bad Request" in response:
            print("PASS: Malformed request correctly returned 400 Bad Request")
        else:
            print(f"FAIL: Malformed request returned unexpected response:\n{response}")

        print("Testing 505 HTTP Version Not Supported for HTTP/1.0 request...")
        with socket.create_connection(("localhost", 45411)) as s:
            # Manually send an HTTP/1.0 request
            s.sendall(b"GET / HTTP/1.0\r\nHost: localhost\r\n\r\n")
            response = s.recv(1024).decode()

        if "505 HTTP Version Not Supported" in response:
            print("PASS: HTTP/1.0 request correctly returned 505 HTTP Version Not Supported")
        else:
            print(f"FAIL: HTTP/1.0 request returned unexpected response:\n{response}")


    except Exception as e:
        print(f"Exception during tests: {e}")

if __name__ == '__main__':
    server_process = run_server() # Start the server 
    test_server_response()
    if server_process:
        server_process.kill()  # Kill the server process
