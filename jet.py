import subprocess
import adafruit_servokit
import socket
import threading
import time
import cv2
import ai
Servos = adafruit_servokit.ServoKit(channels=16)
Servos.servo[0].angle = 0
print('moving to 0')
time.sleep(2)
print('moving to 180')
Servos.servo[0].angle = 180
time.sleep(2)
print('moving to 90')
Servos.servo[0].angle = 90

hostname = socket.gethostname()
my_ip = socket.gethostbyname(hostname)
camera_mode = True
camera_index = 0
custom_image = ""  # ImagePath
ip = '10.42.0.48'
#ip = '10.42.0.44'

class jetson:
    def __init__(self, **kwargs):
        threading.Thread(target=self.listen_socket).start()
        self.predictor = ai.AI()
        self.Servos = adafruit_servokit.ServoKit(channels=16)
        if camera_mode is True:
            threading.Thread(target=self.video_capture_thread).start()
    #def move_servo(degree):
    #    Servos.servo[0] = degree
    def video_capture_thread(self):
        global camera_mode, camera_index

        if camera_mode:
            cap = cv2.VideoCapture(camera_index)
            while True:
                ret, frame = cap.read()
                if ret:
                    # Do any processing or manipulation of the frame as needed
                    # For example, you could display the frame using OpenCV's imshow() function
                    # or send it to the Kivy app for display
                    self.frame = (
                        frame.copy()
                    )  # Update the self.frame with the captured frame
                    cv2.imwrite("temp_frame.jpg", self.frame)
                    # Pass the temporary image path to predict_and_show
                    threading.Thread(
                        target=self.predict_and_show, args=("temp_frame.jpg",)
                    ).start()
                time.sleep(1)

    def predict_and_show(self, image_path):
        print('predicting')
        def move_servo(degree):
                Servos.servo[0].angle = degree
        predicted_class, probability, image = self.predictor.predict(image_path)
        prediction_text = (
            f"Predicted Class: {predicted_class}\nProbability: {probability:.2f}"
        )
        print(prediction_text)
        self.predicted_class = predicted_class
        print(predicted_class)
        print('/n')
        print('n- ' + self.predicted_class)
        #self.send_socket_info(predicted_class)
        print('currently it is ' + self.predicted_class)
        if str(self.predicted_class) == 'Cans':
                print('it is can')
                Servos.servo[0].angle = 0
                move_servo(0)

                print('moved servo to 0')
        elif str(self.predicted_class) == 'Bottles':
                print('it is Bottle')
                Servos.servo[0].angle = 180
                move_servo(180)
                print('moved servo to 180') 
        elif str(self.predicted_class) == 'Background':
                print('it is background')
                Servos.servo[0].angle = 90
                move_servo(90)
        self.send_socket_info(predicted_class)
        time.sleep(1)
        move_servo(90)
        #time.sleep(1)

    def send_socket_info(self, text):
        try:
                print('sending info')
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                # Connect to the server
                server_address = (ip, 1236)
                client_socket.connect(server_address) 
                text_bytes = text.encode('utf-8')
                # Send commands
                client_socket.sendall(text_bytes)
                # Close the client socket
                client_socket.close()
        except:
                try:
                        command = f'sudo nmcli device wifi connect Robot_Hotspot_SG_ITE password robotics'
                        result = subprocess.run(command, shell=True, text=True, capture_output=False)
                except:
                        pass
                client_socket.connect(server_address)
                print('issue')
                pass


    def listen_socket(self):
        global command
        # Create a socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        server_address = (socket.gethostbyname(hostname), 1234)
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
            print(f"GUI: {command}")
            if command == "Command: Yes_Button":
                print(command)
            elif command == "Command: Close_Button":
                print(command)


jet = jetson()
jet.predict_and_show("temp_frame.jpg")
