import socket
import datetime
import random

SERVER_NAME = "MyServer"
HOST = "127.0.0.1"
PORT = 12349

def handle_client(client_socket, client_address):
    print(f"[+] Client connected: {client_address}")
    while True:
        try:
            data = client_socket.recv(4)
            if not data:
                break

            command = data.decode().strip().upper()
            print(f"[{client_address}] Command received: {command}")

            if command == "TIME":
                response = datetime.datetime.now().strftime("%H:%M:%S")
            elif command == "NAME":
                response = SERVER_NAME
            elif command == "RAND":
                response = str(random.randint(1, 10))
            elif command == "EXIT":
                response = "Goodbye!"
                client_socket.sendall(response.encode())
                break
            else:
                response = "Unknown Command"

            client_socket.sendall(response.encode())

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

    client_socket.close()
    print(f"[-] Client disconnected: {client_address}")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[*] Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket, client_address)

if __name__ == "__main__":
    main()
