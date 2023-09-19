import socket

BYTES_TO_READ = 4096

def get(host, port):
    requests =  b"GET / HTTP/1.1\nHost: www.google.com\n\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Initialize the socket
        s.connect((host, port)) # Connect to Google
        s.send(requests) # Send request
        s.shutdown(socket.SHUT_WR) # Means I'm done sending
        chunk = s.recv(BYTES_TO_READ)
        result = b'' + chunk

        while(len(chunk)>0):
            chunk = s.recv(BYTES_TO_READ)
            result += chunk
        s.close()
        return result
    
print(get("127.0.0.1", 8080))