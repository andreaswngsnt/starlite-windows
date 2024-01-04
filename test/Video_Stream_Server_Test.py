import cv2
import socket
import pickle
import struct

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(5)

# Accept a client connection
client_socket, addr = server_socket.accept()
print(f"Connection from {addr} established!")

# Initialize OpenCV video capture
cameraIndex = 0 #Type of camera to use (i.e., "0" means laptop webcam)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Serialize frame
    data = pickle.dumps(frame)
    
    # Get the size of the data and send it
    message_size = struct.pack("L", len(data))
    client_socket.sendall(message_size + data)

    # Display the resulting frame
    cv2.imshow('Server Feed', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
server_socket.close()
