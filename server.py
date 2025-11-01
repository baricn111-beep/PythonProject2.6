
import socket
import datetime
import random
import logging
import threading

# ========== CONFIGURATION ==========
SERVER_NAME = "MyServer"
HOST = "127.0.0.1"
PORT = 16767
LOG_FILE = "server_log.txt"

# ========== LOGGING SETUP ==========
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ========== CLIENT HANDLER ==========
def handle_client(client_socket, client_address):
    """
    Handle a single client connection: read commands, process them, and send responses.
    """
    logging.info(f"Client connected: {client_address}")
    print(f"[+] Client connected: {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            command = data.decode().strip().upper()
            logging.info(f"Command received from {client_address}: {command}")
            print(f"[{client_address}] Command received: {command}")

            # Handle commands
            if command == "TIME":
                response = datetime.datetime.now().strftime("%H:%M:%S")

            elif command == "NAME":
                response = SERVER_NAME

            elif command == "RAND":
                num = random.randint(1, 10)
                # 🧠 ASSERT to ensure number is in the expected range
                assert 1 <= num <= 10, f"Random number {num} out of range!"
                response = str(num)
                logging.info(f"Generated random number {num} for {client_address}")

            elif command == "EXIT":
                response = "Goodbye!"
                logging.info(f"Client {client_address} sent EXIT, closing connection.")
                client_socket.sendall(response.encode())
                break

            else:
                response = "Unknown Command"
                logging.warning(f"Unknown command from {client_address}: {command}")

            client_socket.sendall(response.encode())
            logging.info(f"Response sent to {client_address}: {response}")

    except AssertionError as ae:
        logging.error(f"Assertion failed: {ae}")
        print(f"[ASSERTION ERROR] {ae}")

    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
        print(f"Error handling client {client_address}: {e}")

    finally:
        client_socket.close()
        logging.info(f"Client disconnected: {client_address}")
        print(f"[-] Client disconnected: {client_address}")


# ========== MAIN SERVER FUNCTION ==========
def main():
    """
    Start the TCP server, accept incoming connections, and spawn threads for each client.
    """
    logging.info("Starting server...")
    print(f"[*] Starting server on {HOST}:{PORT}")

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        logging.info(f"Server started successfully on {HOST}:{PORT}")
        print(f"[*] Server started on {HOST}:{PORT}")

    except OSError as e:
        logging.critical(f"Failed to bind socket: {e}")
        print(f"[ERROR] Could not start server: {e}")
        return

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            logging.info(f"Accepted connection from {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

        except KeyboardInterrupt:
            print("\n[!] Server shutting down.")
            logging.info("Server manually stopped by user.")
            break

        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            print(f"[ERROR] {e}")
            continue

    server_socket.close()
    logging.info("Server closed.")


# ========== ENTRY POINT ==========
if __name__ == "__main__":
    main()
