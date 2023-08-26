import socket


my_ip = '192.168.1.100'

def send_socket_info(text):
    # Create a socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    server_address = (my_ip, 1236)
    client_socket.connect(server_address)
    text_bytes = text.encode('utf-8')
    
    # Send commands
    client_socket.sendall(text_bytes)
    # Close the client socket
    client_socket.close()

send_socket_info('Bottles')