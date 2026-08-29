import ssl
import socket
from threading import Thread

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024)
        print(f"Received: {request}")
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, Secure World!"
        client_socket.sendall(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8443))
    server.listen(5)
    print("Server listening on port 8443")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    while True:
        client_sock, addr = server.accept()
        secure_sock = context.wrap_socket(client_sock, server_side=True)
        print(f"Accepted connection from {addr}")
        client_handler = Thread(target=handle_client, args=(secure_sock,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
