import socket
import sys
import threading
import multiprocessing

chunk_size = 1024


def socket_error_handler(exception):
    print(exception)
    sys.exit(1)


def upload_file(client_socket, filename):
    """Uploads a file to the server via the load balancer"""

    def send_data(data):
        try:
            client_socket.sendall(data.encode())  # encode will use auto  UTF-8.
        except Exception as e:
            print(f"Sending {data} Failed\n")
            client_socket.close()
            sys.exit(1)

    try:
        # Opens the file in binary format for
        file = open(filename, 'rb')
    except Exception as e:
        print(f"{filename} File opening failed.\n")
        sys.exit(1)
    # Send fileName First
    send_data(filename)
    # Send fileData as chunks
    chunk = file.read(chunk_size)
    if not chunk:
        # check if file is empty
        print(f"file {file} is empty\n")
        sys.exit(1)
    else:
        while chunk:
            send_data(chunk)
            chunk = file.read(chunk_size)
        print(f"File '{filename}' uploaded successfully.")


def download_file(client_socket, filename):
    """Downloads a file from the server via the load balancer."""

    def send_data(data):
        try:
            client_socket.sendall(data.encode())  # encode will use auto  UTF-8.
        except Exception as e:
            print(f"Sending {data} Failed\n")
            sys.exit(1)

    try:
        # Send a request to DOWNLOAD file
        send_data(f"DOWNLOAD {filename}")
        with open(filename, 'wb') as file:  # Open as binary to write recived data
            while True:  # Receive all file data
                try:
                    data = client_socket.recv(1024)
                except Exception as e:
                    print(f"in download file {e}\n")
                    sys.exit(1)
                if not data:
                    break
                file.write(data)
        print(f"File '{filename}' downloaded successfully.")
    except Exception as e:
        print(f"Failed to download file: {e}")


def handle_response(response):
    """Handles the response from the server"""
    print(response.decode())


def connect_to_load_balancer(serverIP, serverPort):
    """Establishes a connection to the load balancer"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        print("Creating socket failed\n ")
        socket_error_handler(e)
    try:
        client_socket.connect((serverIP, serverPort))
        print(f"Connected to load balancer at {serverIP}:{serverPort}")
    except Exception as e:
        print("Socket connecting failed\n ")
        socket_error_handler(e)
    return client_socket


def main():
    # Connect to load balancer
    serverIP = 'localhost'
    serverPort = 5000  # Loader port
    client_socket = connect_to_load_balancer(serverIP, serverPort)

    action = input("Enter action (upload/download): ").strip().lower()
    filename = input("Enter filename: ").strip()
    if action == 'upload':
        upload_file(client_socket, filename)
    elif action == 'download':
        download_file(client_socket, filename)
    else:
        print("Invalid action. should entered 'upload' or 'download'.")

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    main()
