from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
import threading
import pyttsx3
import socket
import os
import ai
import cv2
import kivy


raspberry_address = "192.168.0.162"

camera_mode = True
camera_index = 0
custom_image = '' #ImagePath

def get_own_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

Computer_IP = get_own_ip()
Window.fullscreen = 'auto'

shown_text = 'Hello World!'

IMAGE_DIRECTORY = "Assets\GUI\Images"

class ImageBackground(FloatLayout):
    def __init__(self, **kwargs):
        super(ImageBackground, self).__init__(**kwargs)
        
        if camera_mode is True:
            threading.Thread(target=self.video_capture_thread).start()
        
        
        
        
        self.background = Image(source=os.path.join(IMAGE_DIRECTORY, 'heretorecycle.png'), allow_stretch=True)
        self.add_widget(self.background)

        self.relative_layout = FloatLayout()
        self.add_widget(self.relative_layout)

        with self.relative_layout.canvas.before:
            Color(0x25 / 255.0, 0x22 / 255.0, 0x3c / 255.0, 1)
            self.rect = Rectangle(pos=(0, 775), size=(1920, 200))

        self.label = Label(
            text=f'{shown_text}',
            color=(1, 1, 1, 1),
            font_size=80,
            size_hint=(None, None),
            size=(Window.width, 100),
            pos_hint={'center_x': 0.5, 'top': 0.88},
        )
        self.relative_layout.add_widget(self.label)

        self.yes_button = Button(
            text='Yes',
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.6, 'center_y': 0.1},
        )
        self.yes_button.bind(on_release=self.yes_button_clicked)
        self.add_widget(self.yes_button)

        self.no_button = Button(
            text='No',
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.4, 'center_y': 0.1},
        )
        self.no_button.bind(on_release=self.no_button_clicked)
        self.add_widget(self.no_button)

        self.image_widget = None
        self.predicter = ai.AI()
        if camera_mode is True:
            threading.Thread(target=self.predict_and_show, args=(self.frame)).start()
        else:
            threading.Thread(target=self.predict_and_show, args=(os.path.join(custom_image),)).start()

    def video_capture_thread(self):
        global camera_mode, camera_index

        if camera_mode:
            cap = cv2.VideoCapture(camera_index)
            while True:
                self.ret, self.frame = cap.read()
                # Do any processing or manipulation of the frame as needed
                # For example, you could display the frame using OpenCV's imshow() function
                # or send it to the Kivy app for display
                cv2.imwrite("temp_frame.jpg", self.frame)
                # Pass the temporary image path to predict_and_show
                threading.Thread(target=self.predict_and_show, args=("temp_frame.jpg",)).start()



    def predict_and_show(self, image_path):
        predicted_class, probability = self.predicter.loop_predict(image_path)
        #if os.path.exists(image_path):
        #    os.remove(image_path)

        # Show the prediction result on the label
        #prediction_text = f"Predicted Class: {predicted_class}\nProbability: {probability:.2f}"
        #self.label.text = prediction_text

    def yes_button_clicked(self, instance):
        print('Yes button clicked')
        if not self.yes_button.disabled:
            self.hide_buttons()
            # Load the temporary image and pass its path for prediction
            temp_image_path = os.path.join(os.getcwd(), "temp_frame.jpg")
            self.show_image_on_screen(temp_image_path)
            threading.Thread(target=self.predict_and_show, args=(temp_image_path,)).start()

    

    def no_button_clicked(self, instance):
        print('No button clicked')

    def hide_buttons(self):
        Clock.schedule_once(lambda dt: self.set_button_visibility(False), 0)

    def show_cover_buttons(self):
        self.remove_widget(self.yes_button)
        self.remove_widget(self.no_button)
        button_width = Window.width / 2
        button_height = Window.height

        self.close_button = Button(
            text='Close',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'x': 0, 'top': 1},
        )
        self.close_button.bind(on_release=self.close_button_callback)
        self.add_widget(self.close_button)

        self.show_buttons()

    def set_button_visibility(self, visible):
        self.yes_button.disabled = not visible
        self.no_button.disabled = not visible
        self.yes_button.opacity = 1 if visible else 0
        self.no_button.opacity = 1 if visible else 0

    def show_buttons(self):
        Clock.schedule_once(lambda dt: self.set_button_visibility(True), 0)

    def show_image_on_screen(self, image_path):
        if self.image_widget:
            self.remove_widget(self.image_widget)
        self.image_widget = Image(source=image_path, allow_stretch=True)
        self.add_widget(self.image_widget)

    def destroy_image(self):
        if self.image_widget:
            self.remove_widget(self.image_widget)
            self.image_widget = None

    def close_button_callback(self, instance):
        print('Close button clicked')
        self.remove_widget(instance)
        self.show_buttons()
        self.add_widget(self.yes_button)
        self.add_widget(self.no_button)

class MyApp(App):
    def build(self):
        image_background = ImageBackground()
        return image_background


def start_speech_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1235))
    server_socket.listen(1)
    print('Socket server started, listening for commands...')
    
    def speak(text):
        engine = pyttsx3.init()
    
        # Set the voice
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)
        # Set the rate
        # engine.setProperty('rate', rate)
        engine.say(text)
        engine.runAndWait()
    
    while True:
        # Accept client connection
        client_socket, address = server_socket.accept()
        print('Client connected:', address)
        # Receive command from client
        command = client_socket.recv(1024).decode()
        # Process the command
        client_socket.close()
        print('Saying:', command)
        speak(command) 
def listen_socket():
    global command
    # Create a socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (raspberry_address, 1234)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print('Socket server started, listening for commands...')

    while True:
        # Accept client connection
        client_socket, address = server_socket.accept()
        print('Client connected:', address)
        
        # Receive command from client
        command = client_socket.recv(1024).decode()
        
        # Process the command (e.g., perform actions based on the received command)
        print('Received command:', command)
        
        # Close the client socket
        client_socket.close()
        if command =='FinishedDetection':
            ImageBackground.finished_detection_image()

if __name__ == '__main__':
    Window.size = (1920, 1080)


    app = MyApp()
    app.run()
