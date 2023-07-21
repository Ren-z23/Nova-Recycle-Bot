import socket

def send_text(text, ip_address, port):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the receiver
    sock.connect((ip_address, port))
    
    # Send the text
    sock.send(text.encode())
    
    # Close the socket
    sock.close()

# Example usage
ip_address = "192.168.0.158"
port = 1234
text_to_send = "Hello, receiver!"
send_text(text_to_send, ip_address, port)
