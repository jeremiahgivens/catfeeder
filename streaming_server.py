import cv2
import numpy as np
import socket
import struct
import pickle

# initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# create socket and bind to host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 5000
socket_address = (host_ip, port)
server_socket.bind(socket_address)

# listen for incoming connections
server_socket.listen(5)
print("Listening at:", socket_address)

# accept connection from client
client_socket, client_address = server_socket.accept()
print('Connected to:', client_address)

# encode and send video frames to client
while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    client_socket.sendall(message_size + data)

# release OpenCV video capture and close socket
cap.release()
client_socket.close()
server_socket.close()