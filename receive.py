import socket
import csv

# Function to handle data recording in a CSV file
def record_data(data):
    with open('data.csv', mode='a') as file:
        fieldnames = ['Date', 'Time', 'Temperature (Celsius)', 'Humidity (%)']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty; write header only if it's the first entry
        if file.tell() == 0:
            writer.writeheader()

        # Extract data from the received message
        lines = data.strip().split('\n')
        date, time = lines[0].split(' ', 1)
        temperature = lines[1].split()[-1][:-2]
        humidity = lines[2].split()[-1][:-1]

        # Write the data to the CSV file
        writer.writerow({
            'Date': date,
            'Time': time,
            'Temperature (Celsius)': temperature,
            'Humidity (%)': humidity
        })

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
server_address = ('192.168.1.100', 1234)
server_socket.bind(server_address)
server_socket.listen(1)
print("Socket server started, listening for connections...")

while True:
    # Accept client connection
    client_socket, address = server_socket.accept()
    print("Client connected:", address)

    # Receive and record data from client
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print("Received data:", data)
        record_data(data)

    # Close the client socket
    client_socket.close()
