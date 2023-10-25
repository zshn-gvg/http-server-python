import socket
import threading

RESPONSE_200 = "HTTP/1.1 200 OK\r\n\r\n"
RESPONSE_404 = "HTTP/1.1 404 Not Found\r\n\r\n"


def extract_path(request):
    request_by_line = request.split("\r\n")
    HTTPmethod, path, _ = request_by_line[0].split()
    return path


def extract_user_agent(request):
    request_by_line = request.split("\r\n")
    for line in request_by_line[1:]:
        if line.startswith("User-Agent: "):
            return line.split(":", 1)[1].strip()


def handle_user_agent(req_data):
    user_agent = extract_user_agent(req_data)
    response_head = f"""{RESPONSE_200}Content-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n"""
    response = response_head + user_agent
    return response


def handle_echo(path):
    to_echo_string = path[len("/echo/"):]
    response_head = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(to_echo_string)}\r\n\r\n"""
    response = response_head + to_echo_string
    return response


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(5)
    print("Server listening on localhost:4421")
    while True:
        connection, _ = server_socket.accept()
        # print(f"Accepted connection from {address}")
        # req_data = connection.recv(1024).decode()
        # print(f"Received data:\n{req_data}")
        thread = threading.Thread(target=handle_requests, args=(connection,))
        thread.start()


def handle_requests(connection):
    req_data = connection.recv(1024).decode("utf-8")
    path = extract_path(req_data)
    if path == "/":
        connection.sendall(RESPONSE_200.encode())
    elif path.startswith("/files"):
        response = RESPONSE_200 + "todo"
        connection.sendall(response.encode())
    elif path.startswith("user-agent"):
        response = handle_user_agent(req_data)
        connection.sendall(response.encode())
    elif path.startswith("/echo/"):
        response = handle_echo(req_data)
        connection.sendall(response.encode())
    else:
        connection.sendall(RESPONSE_404.encode())
    connection.close()


if __name__ == "__main__":
    main()
