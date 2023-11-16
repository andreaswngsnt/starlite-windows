import socket
import threading

HOST = '0.0.0.0'  # Listen on all available network interfaces
TCP_PORT = 12345  # Port to listen on for TCP

def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if data == "quit":
                break
            if not data:
                break  # If no data is received, close the connection

            # print the received data
            print(f"{data}")

        except ConnectionResetError:
            break

    client_socket.close()

def start_server():
    server_socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_TCP.bind((HOST, TCP_PORT))
    server_socket_TCP.listen(5)

    print("Server is listening on...")
    print("IP Address: %s" % HOST)
    print("Port: %d" % TCP_PORT)

    while True:
        client_socket, _ = server_socket_TCP.accept()
        print("\nStatus Alert: A user is logging into the server.")

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()

