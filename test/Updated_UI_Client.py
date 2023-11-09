import tkinter as tk
import socket
import threading
import keyboard

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Application")
        self.root.geometry("400x300")  # Set the size of the login window

        self.label_username = tk.Label(root, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        self.label_password = tk.Label(root, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show="*")  # Show asterisks for the password
        self.entry_password.pack()

        self.login_button = tk.Button(root, text="Login", command=self.authenticate)
        self.login_button.pack()

        self.response_label = tk.Label(root, text="")
        self.response_label.pack()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = '127.0.0.1'  # Server's IP address
        self.server_port = 12345
        self.username = None
        self.password = None

        self.response_check_thread = None

        # Initiate the connection when the application starts
        self.initiate_connection()

    def initiate_connection(self):
        try:
            # Connect to the server
            self.client_socket.connect((self.server_address, self.server_port))
        except Exception as e:
            self.response_label.config(text=f"Error: {str(e)}")

    def authenticate(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        try:
            # Send username and password to the server
            self.client_socket.send(self.username.encode('utf-8'))
            self.client_socket.send(self.password.encode('utf-8'))

            # Start a thread to continuously check for the response
            if self.response_check_thread is None or not self.response_check_thread.is_alive():
                self.response_check_thread = threading.Thread(target=self.wait_for_response)
                self.response_check_thread.start()

        except Exception as e:
            self.response_label.config(text=f"Error: {str(e)}")

    def wait_for_response(self):
        response = self.client_socket.recv(1024).decode('utf-8')
        if response == "Correct":
            self.open_robot_control_window()
        elif response == "Wrong":
            self.response_label.config(text="Incorrect username or password")

    def open_robot_control_window(self):
        # Close the login window
        self.root.withdraw()  # Hide the login window

        robot_control_window = tk.Toplevel()
        robot_control_window.title("Robot Control")
        robot_control_window.geometry("600x200")  # Set the size of the window

        camera_button = tk.Button(robot_control_window, text="Camera", width=10, height=3)
        camera_button.grid(row=0, column=0, padx=10, pady=10)

        location_button = tk.Button(robot_control_window, text="Location", width=10, height=3)
        location_button.grid(row=0, column=1, padx=10, pady=10)

        navigation_button = tk.Button(robot_control_window, text="Navigation", width=10, height=3)
        navigation_button.grid(row=0, column=2, padx=10, pady=10)

        # Bind the close event of the robot control window to close the client
        robot_control_window.protocol("WM_DELETE_WINDOW", self.close_client)

        print("Press 'Q' to quit.")
    
        # Create a set to keep track of currently pressed keys
        pressed_keys = set()
    
        while True:
            event = keyboard.read_event()
        
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                if key == 'q':
                    break
                pressed_keys.add(key)
                self.client_socket.send(key.encode('utf-8'))
            elif event.event_type == keyboard.KEY_UP:
                key = event.name
                pressed_keys.discard(key)
        
            print(f"Pressed keys: {', '.join(pressed_keys)}")
        

    def close_client(self):
        # Close the client socket and the root window
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()

