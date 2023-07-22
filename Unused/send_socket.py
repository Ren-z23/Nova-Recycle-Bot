import socket

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 1234)
client_socket.connect(server_address)

# Send commands
#client_socket.sendall(b'show')  # Send 'show' command
client_socket.sendall(b'hide')  # Send 'hide' command

# Close the client socket
client_socket.close()
