# Uncomment this to pass the first stage
import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening on localhost:4421")

    connection, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    req_data = connection.recv(1024).decode()
    print(f"Received data:\n{req_data}")

    data = req_data.split()

    if len(data) >0 and data[0] == "GET":
        path = data[1]
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

if __name__ == "__main__":
    main()
