import cv2
import numpy as np
import socket
import struct
import pickle

# create socket and connect to host and port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.149'  # replace with server IP address
port = 5000
client_socket.connect((host_ip, port))
print('Connected to:', (host_ip, port))

# receive and decode video frames from server
data = b""
payload_size = struct.calcsize("L")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    # display video frames
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# close OpenCV window and socket
cv2.destroyAllWindows()
client_socket.close()