import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" # Your computers IP. Writing localhost here also works as it refers to your computer
PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ) # Wait for a request and receive it 
            if not data:
                break
            print(data)
            conn.sendall(data)

# Start single threaded echo server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Initialize the socket
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen() # Listen for incoming connections
        conn, addr = s.accept() # Accepting the client connection | conn variable takes client socket | addr variable takes IP, port of client
        handle_connection(conn, addr) # Send it a response

# Start multithreaded echo server
def start_threaded_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Initialize the socket
            s.bind((HOST, PORT))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.listen(2) # Allow a backlog of up to two connections. For example: queue -> [waiting conn1, waiting conn2]
            while True:
                 conn, addr = s.accept()
                 thread = Thread(target=handle_connection, args=(conn, addr))
                 thread.run()


#start_server()
start_threaded_server()