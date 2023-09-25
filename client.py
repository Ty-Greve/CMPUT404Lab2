import socket

BYTES_TO_READ = 4096

def get(host, port):
    requests =  b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Opened up a socket here | socket.AF_INET means use IPv4 | socket.SOCK_STREAM means use TCP
    s.connect((host, port)) # Connect to Google
    s.send(requests) # Send request
    s.shutdown(socket.SHUT_WR) # Means I'm done sending
    result = s.recv(BYTES_TO_READ) # Keep reading incoming data
    while(len(result)>0):
        print(result)
        result = s.recv(BYTES_TO_READ)
    
    s.close()

#get("wwww.google.com", 80)
get("localhost", 8080)