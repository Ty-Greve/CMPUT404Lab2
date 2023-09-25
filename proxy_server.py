import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1" # Your computers IP. Writing localhost here also works as it refers to your computer
PROXY_SERVER_PORT = 8080

# Send some data (request) to host:port
def send_request(host, port, request):

    # Create a new socket in the with-block to ensure it's closed once we're done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: # Initialize the client socket
        # Connect the socket to host:port
        client_socket.connect((host, port))
        # Send the request through the connected socket.
        client_socket.send(request)
        # Shut the socket to further writes. Tells server we're done sending
        client_socket.shutdown(socket.SHUT_WR)

        # Assemble response, be careful here, recall that recv(bytes) blocks until it receives data
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: # Keep reading data until connection terminates
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        # Return response
        return result
    
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ) # Wait for a request and receive it 
            if not data: # If the socket has been closed to further writes, break
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request) # Send it as a request to www.google.com
        conn.sendall(response) # Return the response from www.google.com back to the client

# Start single-threaded proxy server
def start_server():
    '''
    Create the socket in the with-block to ensure it gets auto-closed once we are done
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: # Initialize the socket
        # Bind the server to a specific host and port on this machine
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        '''
        Allow us to reuse this socket address during linger, as well as other implications
        '''
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) # Allow a backlog of up to two connections. For example: queue -> [waiting conn1, waiting conn2]
        '''
        Wait for incoming connection, and when one arrives, accept it and create a new socket called 'conn' to interact with it.
        '''
        conn, addr = server_socket.accept() # Accepting the client connection | conn variable takes client socket | addr variable takes IP, port of client
        
        handle_connection(conn, addr) # Pass 'conn' off to handle_connection to do some logic

# Start multi-threading proxy server
def start_threaded_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: # Initialize the socket
            server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.listen(2) # Allow a backlog of up to two connections. For example: queue -> [waiting conn1, waiting conn2]
            while True:
                 conn, addr = server_socket.accept()
                 thread = Thread(target=handle_connection, args=(conn, addr))
                 thread.run()

# start_server()
start_threaded_server()