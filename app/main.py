# Uncomment this to pass the first stage
import socket
import re

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening on localhost:4421")

    connection, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    data = connection.recv(1024).decode()
    print(f"Received data:\n{data}")

    path = data.split()[1]
    match = re. match = re.match(r"/echo/(\w+)", path)
    if match:
        rnd_string = match.group(1)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(rnd_string)}\r\n\r\n{rnd_string}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    
    connection.sendall(response.encode())
    connection.close()

if __name__ == "__main__":
    main()
