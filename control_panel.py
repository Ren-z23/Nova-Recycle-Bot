from flask import Flask, request, jsonify, render_template
import os
import socket

hostname = socket.gethostname()
my_ip = socket.gethostbyname(hostname)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'ControlPanel'))



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/press_yes_butn', methods=['POST'])
def press_yes_button():
    # Your Python function logic here
    result = "Python function activated successfully!"
    print('Hello WOrld!')


    # Create a socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = (my_ip, 1234)
    client_socket.connect(server_address)

    # Send commands
    #client_socket.sendall(b'show')  # Send 'show' command
    client_socket.sendall(b'Command: Yes_Button')

    # Close the client socket
    client_socket.close()
    return jsonify({'result': result})

@app.route('/test_function_python', methods=['POST'])
def test_function_python():
    print('Command: Close_Button')
    # Create a socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = (my_ip, 1234)
    client_socket.connect(server_address)
    client_socket.sendall(b'Command: Close_Button')
    client_socket.close()
    return jsonify({'result': 'test_function_python'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444)
