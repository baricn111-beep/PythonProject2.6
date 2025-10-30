import socket

HOST = "127.0.0.1"
PORT = 12349

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Connected to server. Commands: TIME, NAME, RAND, EXIT")


    while True:
        cmd = input("Enter command: ").upper()

        if len(cmd) < 4:
            cmd = cmd.ljust(4)
        elif len(cmd) > 4:
            cmd = cmd[:4]

        client_socket.sendall(cmd.encode())

        data = client_socket.recv(1024).decode()
        print("Server response:", data)

        if cmd.strip() == "EXIT":
            break

    client_socket.close()
    print("Disconnected.")

if __name__ == "__main__":
    main()
