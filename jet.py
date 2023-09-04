import socket
import threading
import time
import cv2
import ai

hostname = socket.gethostname()
my_ip = socket.gethostbyname(hostname)
camera_mode = True
camera_index = 0
custom_image = ""  # ImagePath
gui_ip = '10.42.0.48'

class jetson:
    def __init__(self, **kwargs):
        self.predict_thread = None
        self.thread_lock = threading.Lock()
        threading.Thread(target=self.listen_socket).start()
        self.predictor = ai.AI()

        if camera_mode:
            threading.Thread(target=self.video_capture_thread).start()

    def video_capture_thread(self):
        global camera_mode, camera_index

        if camera_mode:
            cap = cv2.VideoCapture(camera_index)
            while True:
                with self.thread_lock:
                    if self.predict_thread and self.predict_thread.is_alive():
                        self.predict_thread.join()
                    
                    self.predict_thread = threading.Thread(
                        target=self.predict_and_show_thread, args=("temp_frame.jpg",)
                    )
                    self.predict_thread.start()
                    
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite("temp_frame.jpg", frame)
                    threading.Thread(
                        target=self.predict_and_show, args=("temp_frame.jpg",)
                    ).start()
                time.sleep(3)

    def predict_and_show(self, image_path):
        predicted_class, probability, image = self.predictor.predict(image_path)
        prediction_text = (
            f"Predicted Class: {predicted_class}\nProbability: {probability:.2f}"
        )
        print(prediction_text)
        print(predicted_class)
        self.send_socket_info(predicted_class)
        if predicted_class == 'Cans':
            print('it is Cans')
            #Servos.servo[0].angle = 0
        elif predicted_class == 'Bottles':
            print('it is Bottles')
            #Servos.servo[0].angle = 180
        elif predicted_class == 'Background':
            print('it is background')
            #Servos.servo[0].angle = 90
        self.send_socket_info(predicted_class)
        time.sleep(1)
        #Servos.servo[0].angle = 90
        time.sleep(1)

    def send_socket_info(self, text):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (gui_ip, 1236)
        client_socket.connect(server_address)
        text_bytes = text.encode('utf-8')
        client_socket.sendall(text_bytes)
        client_socket.close()

    def listen_socket(self):
        global command
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        server_address = (socket.gethostbyname(hostname), 1234)
        server_socket.bind(server_address)
        server_socket.listen(1)
        print("Socket server started, listening for commands...")

        while True:
            client_socket, address = server_socket.accept()
            print("Client connected:", address)
            command = client_socket.recv(1024).decode()
            print("Received command:", command)
            client_socket.close()
            print(f"GUI: {command}")
            if command == "Command: Yes_Button":
                print(command)
            elif command == "Command: Close_Button":
                print(command)

while __name__ == '__main__':
    jet = jetson()
    jet.predict_and_show("temp_frame.jpg")
