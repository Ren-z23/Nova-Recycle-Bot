import socket

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('192.168.0.158', 1235)
client_socket.connect(server_address)

# Send commands

client_socket.sendall(b'Publishers SummaryWho needs a Class when youre already the strongest anyways?Ten years ago, Amelia woke up alone and lost in a broken world where she ha')  

# Close the client socket
client_socket.close()
