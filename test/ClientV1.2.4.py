import keyboard
import socket
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import folium
from tkinter import Toplevel, Frame, Label

from PIL import ImageTk
from tkhtmlview import HTMLLabel
import tkintermapview
from tkinter import *

#Camera Feed:
import cv2
import pickle
import struct

"""
Useful Links:
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter Most useful in my opinion
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
https://www.youtube.com/watch?v=HjNHATw6XgY&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
"""

# You can also use a pandas dataframe for transaction_history.
# you can convert the dataframe using df.to_numpy.tolist()
transaction_history = []

frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP

class LoginPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#708090", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")

        self.geometry("626x431")  # Sets window size to 626w x 431h pixels
        self.resizable(0, 0)  # This prevents any resizing of the screen
        title_styles = {"font": ("Trebuchet MS Bold", 16), "background": "blue"}

        text_styles = {"font": ("Verdana", 14),
                       "background": "blue",
                       "foreground": "#E1FFFF"}

        frame_login = tk.Frame(main_frame, bg="blue", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.30, relx=0.17, height=130, width=400)

        label_title = tk.Label(frame_login, title_styles, text="Login Page")
        label_title.grid(row=0, column=1, columnspan=1)

        label_user = tk.Label(frame_login, text_styles, text="Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(frame_login, text_styles, text="Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(frame_login, width=45, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(frame_login, width=45, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_login, text="Login", command=lambda: getlogin())
        button.place(rely=0.70, relx=0.50)

        signup_btn = ttk.Button(frame_login, text="Register", command=lambda: get_signup())
        signup_btn.place(rely=0.70, relx=0.75)

        def get_signup():
            SignupPage()

        def getlogin():
            username = entry_user.get()
            password = entry_pw.get()
            # if your want to run the script as it is set validation = True
            validation = validate(username, password)
            if validation:
                try:
                    self.server_address = '127.0.0.1'
                    self.server_port = 12345

                    # Connect to the server
                    client_socket.connect((self.server_address, self.server_port))
                except Exception as e:
                    self.response_label.config(text=f"Error: {str(e)}")
                    
                tk.messagebox.showinfo("Login Successful",
                                       "Welcome {}".format(username))
                root.deiconify()
                top.destroy()
            else:
                tk.messagebox.showerror("Information", "The Username or Password you have entered are incorrect ")

        def validate(username, password):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username and line[3] == password:
                            return True
                    return False
            except FileNotFoundError:
                print("You need to Register first or amend Line 71 to     if True:")
                return False


class SignupPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
        # pack_propagate prevents the window resizing to match the widgets
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")

        self.geometry("250x150")
        self.resizable(0, 0)

        self.title("Registration")

        text_styles = {"font": ("Verdana", 10),
                       "background": "#3F6BAA",
                       "foreground": "#E1FFFF"}

        label_user = tk.Label(main_frame, text_styles, text="New Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(main_frame, text_styles, text="New Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(main_frame, width=20, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(main_frame, width=20, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(main_frame, text="Create Account", command=lambda: signup())
        button.grid(row=4, column=1)

        def signup():
            # Creates a text file with the Username and password
            user = entry_user.get()
            pw = entry_pw.get()
            validation = validate_user(user)
            if not validation:
                tk.messagebox.showerror("Information", "That Username already exists")
            else:
                if len(pw) > 3:
                    credentials = open("credentials.txt", "a")
                    credentials.write(f"Username,{user},Password,{pw},\n")
                    credentials.close()
                    tk.messagebox.showinfo("Information", "Your account details have been stored.")
                    SignupPage.destroy(self)

                else:
                    tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

        def validate_user(username):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username:
                            return False
                return True
            except FileNotFoundError:
                return True

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="My Account", menu=menu_file)
        menu_file.add_command(label="Transaction History", command=lambda: parent.show_frame(Some_Widgets))
        menu_file.add_separator()
        menu_file.add_command(label="Log Out", command=lambda: parent.Quit_application())

        menu_orders = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Place A New Order", command=lambda: parent.frames[Some_Widgets].place_new_order())

        menu_pricing = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Track An Existing Order", menu=menu_pricing)
        menu_pricing.add_command(label="Map Location", command=lambda: parent.Mapview())
        menu_pricing.add_command(label="Live Camera Feed", command=lambda: parent.CameraFeed())

        menu_operations = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Setting", menu=menu_operations)
        menu_positions = tk.Menu(menu_operations, tearoff=0)
        menu_operations.add_cascade(label="Control Setting", menu=menu_positions)
        menu_positions.add_command(label="Enable Autonomous Navigation", command=lambda: parent.show_frame(PageThree))
        menu_positions.add_command(label="Enable Manual Navigation", command=lambda: parent.enable_manual_control())

        menu_help = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Support", menu=menu_help)
        menu_help.add_command(label="Frequently-Asked Questions", command=lambda: parent.OpenNewWindow())

class PlaceOrderPage(tk.Toplevel):
    order_number = 1  # Global variable to keep track of the order number

    def __init__(self, parent, some_widgets_frame):
        tk.Toplevel.__init__(self, parent)
        self.title("Place a New Order")

        self.some_widgets_frame = some_widgets_frame  # Reference to the Some_Widgets frame

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels
        ttk.Label(frame, text="Recipient:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(frame, text="Delivery Address:").grid(row=1, column=0, sticky=tk.W)

        # Entry widgets
        recipient_entry = ttk.Entry(frame, width=30)
        recipient_entry.grid(row=0, column=1, sticky=tk.W)

        address_entry = ttk.Entry(frame, width=30)
        address_entry.grid(row=1, column=1, sticky=tk.W)

        # Button to submit the order
        ttk.Button(frame, text="Submit Order", command=lambda: self.submit_order(recipient_entry.get(), address_entry.get())).grid(row=2, column=0, columnspan=2, pady=10)

    def submit_order(self, recipient, address):
        # Increment the order number
        order_number = PlaceOrderPage.order_number

        # Add the order details to the transaction history
        transaction_history.append((order_number, recipient, address))

        # Update the order number for the next order
        PlaceOrderPage.order_number += 1

        # Refresh the data in the "Most Recent Orders" tree view
        self.some_widgets_frame.refresh_data()

        # Close the order placement window
        self.destroy()

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=1024)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) prevents the app from being resized
        # self.geometry("1024x600") fixes the applications size
        self.frames = {}
        pages = (Some_Widgets, PageOne, PageTwo, PageThree, PageFour)
        for F in pages:
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Some_Widgets)
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def OpenNewWindow(self):
        OpenNewWindow()

    def Mapview(self):
        map_thread = threading.Thread(target=Mapview)
        map_thread.start()

    def CameraFeed(self):
        camera_thread = threading.Thread(target=CameraFeed)
        camera_thread.start()

    def MainMenu(self):
        main_menu_thread = threading.Thread(target=MyApp)
        main_menu_thread.start()

    def enable_manual_control(self):
        def keyboard_listener():
            try:
                
                print("Manual Control Activated...")
                print("Press 'P' to quit.")

                client_socket.send("\nStatus Alert: Manual control has been activated.".encode('utf-8'))  # Notify the server

                # Variable to keep track of keys pressed
                keys_pressed = set()

                while True:
                    event = keyboard.read_event()
                    key = event.name
                    stop_key = ' '

                    if event.event_type == keyboard.KEY_DOWN:
                        if key not in keys_pressed:
                            client_socket.send(f"{key}".encode('utf-8'))
                            continue
                    elif event.event_type == keyboard.KEY_UP:
                        client_socket.send(f"{stop_key}".encode('utf-8'))
                        continue

                    if key == 'p':
                        break  # Quit the loop when 'P' is pressed

                print("Manual Control Stopped.")
                
            except Exception as e:
                print(f"Error: {str(e)}")

        # Start the keyboard listener in a separate thread
        keyboard_thread = threading.Thread(target=keyboard_listener)
        keyboard_thread.start()

    def stop_keyboard_listener(self):
        keyboard.unhook_all()  # Unhook all events
        print("Manual Control Stopped.")

    def Quit_application(self):
        # Inform the server that the client is disconnecting
        client_socket.send("quit".encode('utf-8'))
        client_socket.close()
        self.destroy()  # Close the window

class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=600, width=1024)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


class Some_Widgets(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        frame1 = tk.LabelFrame(self.main_frame, frame_styles, text="Most Recent Orders")
        frame1.place(rely=0.05, relx=0.02, height=400, width=400)

        # Create tv1 as an instance attribute
        self.tv1 = ttk.Treeview(frame1)
        column_list_account = ["Order Number", "Recipient", "Delivery Address"]
        self.tv1['columns'] = column_list_account
        self.tv1["show"] = "headings"  # removes empty column
        for column in column_list_account:
            self.tv1.heading(column, text=column)
            self.tv1.column(column, width=50)
        self.tv1.place(relheight=1, relwidth=0.995)
        treescroll = tk.Scrollbar(frame1)
        treescroll.configure(command=self.tv1.yview)
        self.tv1.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")

        frame2 = tk.LabelFrame(self.main_frame, frame_styles, text="Instructions")
        frame2.place(rely=0.05, relx=0.45, height=500, width=500)

    def load_data(self):
        for row in transaction_history:
            self.tv1.insert("", "end", values=row)

    def refresh_data(self):
        # Deletes the data in the current treeview and reinserts it.
        self.tv1.delete(*self.tv1.get_children())  # *=splat operator
        self.load_data()

    def place_new_order(self):
        # This method should handle the logic for placing a new order
        # For example, it can open a new window with textboxes for order details
        # and then update the transaction_history and refresh the treeview

        # Create a new Toplevel window for order placement
        order_window = tk.Toplevel(self)
        order_window.title("Place a New Order")

        frame = ttk.Frame(order_window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels
        ttk.Label(frame, text="Recipient:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(frame, text="Delivery Address:").grid(row=1, column=0, sticky=tk.W)

        # Entry widgets
        recipient_entry = ttk.Entry(frame, width=30)
        recipient_entry.grid(row=0, column=1, sticky=tk.W)

        address_entry = ttk.Entry(frame, width=30)
        address_entry.grid(row=1, column=1, sticky=tk.W)

        # Button to submit the order
        ttk.Button(frame, text="Submit Order", command=lambda: self.submit_order(order_window, recipient_entry, address_entry)).grid(row=2, column=0, columnspan=2, pady=10)

    def submit_order(self, order_window, recipient_entry, address_entry):
        # Get the values from the entry widgets
        recipient = recipient_entry.get()
        address = address_entry.get()

        if not recipient or not address:
            # Display an error message if either field is empty
            tk.messagebox.showerror("Error", "Both Recipient and Address must be filled")
        else:
            # Increment the order number
            order_number = len(transaction_history) + 1

            # Add the order details to the transaction history
            new_order = [order_number, recipient, address]
            transaction_history.append(new_order)

            # Refresh the data in the "Most Recent Orders" tree view
            self.refresh_data()

            # Display a success message
            tk.messagebox.showinfo("Success", "Order placed successfully!")

            # Clear the entry widgets
            recipient_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)

class PageOne(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Page One")
        label1.pack(side="top")


class PageThree(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Page Three")
        label1.pack(side="top")


class PageFour(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Page Four")
        label1.pack(side="top")

class PageTwo(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="Page Two")
        label1.pack(side="top")


class Mapview(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        map_frame = tk.Frame(self)
        map_frame.pack_propagate(0)
        map_frame.pack(fill="both", expand="true")
        self.title("Mapview")
        self.geometry("900x700")

        # create map widget
        map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=0)

        # set current widget position and zoom
        map_widget.set_position(33.64, -117.84)
        map_widget.set_zoom(15)
        map_widget.pack()

        self.buttonCloseWindow = tk.Button(self, text='Close Window', command=lambda: self.quit_map())
        self.buttonCloseWindow.pack()

        self.mainloop()

    def quit_map(self):
        self.withdraw()
        self.quit()
        self.destroy()

class CameraFeed(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        data = b""
        payload_size = struct.calcsize("L")

        while True:
            while len(data) < payload_size:
                data += client_socket.recv(4096)
                
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Deserialize frame
            frame = pickle.loads(frame_data)
            
            # Display the frame
            cv2.imshow('Client Feed', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        def quit_camera(self):
            # Release resources
            cv2.destroyAllWindows()
            
class OpenNewWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.title("Here is the Title of the Window")
        self.geometry("500x500")
        self.resizable(0, 0)

        frame1 = ttk.LabelFrame(main_frame, text="This is a ttk LabelFrame")
        frame1.pack(expand=True, fill="both")

        label1 = tk.Label(frame1, font=("Verdana", 20), text="OpenNewWindow Page")
        label1.pack(side="top")


top = LoginPage()
top.title("Starlite Network - Login")
root = MyApp()
root.withdraw()
root.title("Starlite Network")

root.mainloop()
