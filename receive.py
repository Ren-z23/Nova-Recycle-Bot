import socket


def listen_socket():
            global command
            # Create a socket server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hostname = socket.gethostname()
            server_address = (socket.gethostbyname(hostname), 1236)
            server_socket.bind(server_address)
            server_socket.listen(1)
            print("Socket server started, listening for commands...")

            while True:
                # Accept client connection
                client_socket, address = server_socket.accept()
                print("Client connected:", address)

                # Receive command from client
                command = client_socket.recv(1024).decode()

                # Process the command (e.g., perform actions based on the received command)
                print("Received command:", command)

                # Close the client socket
                client_socket.close()
                print(f'GUI: {command}')
                if command == "Command: Yes_Button":
                    print(command)
                elif command == "Command: Close_Button":
                    print(command)
                    

while True:
    listen_socket()