# Uncomment this to pass the first stage
import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening on localhost:4421")

    connection, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    data = connection.recv(1024).decode("utf-8")
    print(f"Received data:\n{data}")

    path = data.split()[1]

    if path == "/":
       response = "HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    
    connection.sendall(response.encode())
    connection.close()

if __name__ == "__main__":
    main()
