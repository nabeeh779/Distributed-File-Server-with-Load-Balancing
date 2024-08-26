import socket
import threading
import sys
from itertools import cycle

SERVERS = [("localhost", 8001), ("localhost", 8002)]
BUFFER_SIZE = 1024


def handle_client(client_socket, servers):
    """Handles client requests and distributes them to server instances"""
    server_cycle = cycle(servers)  # will loop on all servers
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            server_address = next(server_cycle)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect(server_address)
                server_socket.sendall(data)

                # Receive response from server
                response = server_socket.recv(BUFFER_SIZE)
                client_socket.sendall(response)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def client_handler(client_socket, servers):
    """Thread worker function to handle a single client"""
    handle_client(client_socket, servers)


def start_load_balancer(host, port, servers):
    """Starts the load balancer service"""

    try:
        load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        load_balancer_socket.bind((host, port))  # Load balancer listens for incoming client connections
        load_balancer_socket.listen(5)
        print(f"Load balancer listening on {host}:{port}")
        while True:
            client_socket, _ = load_balancer_socket.accept()  # waits for an incoming connection
            #  Create new thread to handle the client
            client_thread = threading.Thread(target=client_handler, args=(client_socket, servers))
            client_thread.daemon = True  # automatically exit when the main program exits, even if it's still running
            client_thread.start()
    except Exception as e:
        print(f"Failed to start load balancer: {e}")
        sys.exit(1)


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5000

    start_load_balancer(HOST, PORT, SERVERS)
