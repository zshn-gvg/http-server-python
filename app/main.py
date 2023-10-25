import socket
import threading
import os
import sys

RESPONSE_200 = "HTTP/1.1 200 OK\r\n\r\n"
RESPONSE_201 = "HTTP/1.1 201 Resource Created\r\n\r\n"
RESPONSE_404 = "HTTP/1.1 404 Not Found\r\n\r\n"


def extract_path(request):
    request_by_line = request.split("\r\n")
    HTTPmethod, path, _ = request_by_line[0].split( )
    return path

def extract_method(request):
    request_by_line = request.split("\r\n")
    HTTPmethod, path, _ = request_by_line[0].split( )
    return HTTPmethod

def handle_post_file(request, path):
    filename = path.split("/")[2]
    body = request.split("\r\n\r\n")[1]
    dir = sys.argv[-1]
    fd = open(dir + filename, mode="wb")
    fd.write(body.encode())
    return RESPONSE_201 


def extract_user_agent(request):
    request_by_line = request.split("\r\n")
    for line in request_by_line[1:]:
        if line.startswith("User-Agent: "):
            return line.split(":", 1)[1].strip()


def handle_user_agent(req_data):
    user_agent = extract_user_agent(req_data)
    response_head = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n"""
    response = response_head + user_agent
    return response


def handle_echo(path):
    to_echo_string = path[6 :]
    response_head = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(to_echo_string)}\r\n\r\n"""
    response = response_head + to_echo_string
    return response


def handle_files(path):
        filename = path.split("/")[2]
        dir = sys.argv[-1]
        filePath = dir + filename
        if os.path.exists(filePath):
            content = open(filePath).read()
            response_head = f"""HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n"""
            response = response_head + content
            return response
        else:
            response = RESPONSE_404
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
    method = extract_method(req_data)
    if method == "GET":
        if path == "/":
            connection.sendall(RESPONSE_200.encode())
        elif path.startswith("/files"):
            response = handle_files(path)
            connection.sendall(response.encode())
        elif path.startswith("/user-agent"):
            response = handle_user_agent(req_data)
            connection.sendall(response.encode())
        elif path.startswith("/echo/"):
            response = handle_echo(path)
            connection.sendall(response.encode())
        else:
            connection.sendall(RESPONSE_404.encode())
    elif method == "POST":
        if path.startswith("/files"):
            response = handle_post_file(req_data, path)
            connection.sendall(response.encode())
    connection.close()


if __name__ == "__main__":
    main()
