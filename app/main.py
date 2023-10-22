# Uncomment this to pass the first stage
import socket
import threading

def handle_requests(connection):
        req_data = connection.recv(1024).decode()
        data = req_data.split()
        if len(data) > 1 and data[0] == "GET":
            path = data[1]
            if path == "/":
                response = "HTTP/1.1 200 OK\r\n\r\n"
            elif path.startswith("/echo/"):
                rndm_string = path[6:]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(rndm_string)}\r\n\r\n{rndm_string}"
            elif path.startswith("/user-agent") and data[5] == "User-Agent:":
                agent_value = data[6]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(agent_value)}\r\n\r\n{agent_value}"
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
        connection.sendall(response.encode())
        connection.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(10)
    print("Server listening on localhost:4421")

    while True:
        connection, address = server_socket.accept()
        print(f"Accepted connection from {address}")

        req_data = connection.recv(1024).decode()
        print(f"Received data:\n{req_data}")

        thread = threading.Thread(target=handle_requests, args=(connection,))
        thread.start()


if __name__ == "__main__":
    main()
