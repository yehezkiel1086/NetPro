import socket
from multiprocessing import Process

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024)
        print(f"Received: {request}")
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!"
        client_socket.sendall(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    print("Server listening on port 8080")

    while True:
        client_sock, addr = server.accept()
        print(f"Accepted connection from {addr}")
        process = Process(target=handle_client, args=(client_sock,))
        process.start()
        client_sock.close()

if __name__ == "__main__":
    start_server()
