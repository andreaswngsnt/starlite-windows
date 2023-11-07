import socket

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 12345        # Port to connect to

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Displays a message to the user
print("\nMy Starlite Account")

# Prompting the user for a username and password:

# Requesting a username from the user
username = input('' + "Please enter your username: ")
# Send username to server
client_socket.send(username.encode('utf-8'))

# Requesting a password from the user
password = input("Please enter your password: ")
# Send password to server
client_socket.send(password.encode('utf-8'))

# Receiving the server's response
response = client_socket.recv(1024).decode('utf-8')

def main():
    # If the login is successful, enter a destination address
    if "successful" in response:
        print(response)
        destination = input("Please enter the destination address: ")
        client_socket.send(destination.encode('utf-8'))
    else:
        print(response)
if __name__ == "__main__":
    main()
    # Close the socket
    client_socket.close()
