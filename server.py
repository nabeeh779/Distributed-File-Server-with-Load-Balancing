import socket
import threading
import multiprocessing
import sys
import os

HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 1024
FILE_DIR = './server_files/'  # Directory to save uploaded files


def save_file(client_socket, filename):
    """Receives a file from the client and saves it"""
    try:
        file_path = os.path.join(FILE_DIR, filename)    # Open folder to save file
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(BUFFER_SIZE)  # Getting data
                if not data:
                    break
                file.write(data)
        client_socket.sendall(b"File uploaded successfully")
    except Exception as e:
        print(f"Error saving file: {e}")
        client_socket.sendall(b"Error saving file")


def send_file(client_socket, filename):
    """Sends a file to the client"""
    try:
        file_path = os.path.join(FILE_DIR, filename)
        if not os.path.isfile(file_path):
            client_socket.sendall(b"File not found")
            return

        with open(file_path, 'rb') as file:
            while chunk := file.read(BUFFER_SIZE):
                client_socket.sendall(chunk)
        client_socket.sendall(b"File download complete")
    except Exception as e:
        print(f"Error sending file: {e}")
        client_socket.sendall(b"Error sending file")


def handle_client(client_socket):
    """Handles client requests for file uploads and downloads"""
    try:
        # Receive the filename and decide whether to upload or download
        filename = client_socket.recv(BUFFER_SIZE).decode()
        if filename.startswith("UPLOAD"):
            filename = filename[len("UPLOAD "):]
            save_file(client_socket, filename)
        elif filename.startswith("DOWNLOAD"):
            filename = filename[len("DOWNLOAD "):]
            send_file(client_socket, filename)
        else:
            client_socket.sendall(b"Invalid request")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def client_worker(client_socket):
    """Thread worker function to handle a single client"""
    handle_client(client_socket)


def start_server():
    """Starts the server service"""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, _ = server_socket.accept()
            # Start a new thread for each client connection
            client_thread = threading.Thread(target=client_worker, args=(client_socket,))
            client_thread.start()

    except Exception as e:
        print(f"Failed to start server: {e}")


def run_server_process():
    """Runs the server process"""
    start_server()


if __name__ == "__main__":
    # Create multiple server processes
    num_processes = 2  # Number of server processes to run
    processes = []

    for _ in range(num_processes):
        process = multiprocessing.Process(target=run_server_process)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
