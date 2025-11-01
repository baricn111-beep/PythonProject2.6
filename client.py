import socket
import logging
import sys

HOST = "127.0.0.1"
PORT = 12349

# --- Logging configuration ---
logging.basicConfig(
    filename="client_log.txt",   # All logs will be saved in this file
    level=logging.INFO,          # Log info, warnings, and errors
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("Client starting...")

    # Try to connect to the server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        logging.info(f"Connected to server at {HOST}:{PORT}")
    except Exception as e:
        logging.error(f"Connection failed: {e}")
        sys.exit(1)

    print("Connected to server. Commands: TIME, NAME, RAND, EXIT")

    # Main communication loop
    while True:
        cmd = input("Enter command: ").upper()
        logging.info(f"User entered command: {cmd}")

        # Make sure command length is exactly 4 characters
        if len(cmd) < 4:
            cmd = cmd.ljust(4)
            logging.debug("Command padded to 4 characters")
        elif len(cmd) > 4:
            cmd = cmd[:4]
            logging.debug("Command truncated to 4 characters")

        # Send command to the server
        try:
            client_socket.sendall(cmd.encode())
            logging.info(f"Command '{cmd}' sent to server")
        except Exception as e:
            logging.error(f"Failed to send command: {e}")
            break

        # Receive server response
        try:
            data = client_socket.recv(1024).decode()
            print("Server response:", data)
            logging.info(f"Server response: {data}")
        except Exception as e:
            logging.error(f"Error receiving server response: {e}")
            break

        # If the command is EXIT, end the session
        if cmd.strip() == "EXIT":
            logging.info("EXIT command received. Closing connection.")
            break

    client_socket.close()
    logging.info("Connection closed. Client terminated.")
    print("Disconnected.")


if __name__ == "__main__":
    main()
