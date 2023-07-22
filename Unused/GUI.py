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

raspberry_address = "192.168.0.162"

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

        # Set the background image
        self.background = Image(source=os.path.join(IMAGE_DIRECTORY, 'heretorecycle.png'), allow_stretch=True)
        self.add_widget(self.background)

        # Create a RelativeLayout to hold the colored bar and text label
        self.relative_layout = FloatLayout()
        self.add_widget(self.relative_layout)

        # Create the colored bar on top
        with self.relative_layout.canvas.before:
            Color(0x25 / 255.0, 0x22 / 255.0, 0x3c / 255.0, 1)
            self.rect = Rectangle(pos=(0, 775), size=(1920, 200))

        # Create the text label
        self.label = Label(
            text=f'{shown_text}',
            color=(1, 1, 1, 1),
            font_size=80,
            size_hint=(None, None),
            size=(Window.width, 100),
            pos_hint={'center_x': 0.5, 'top': 0.88},
        )
        self.relative_layout.add_widget(self.label)

        # Create the "Yes" button
        self.yes_button = Button(
            text='Yes',
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.6, 'center_y': 0.1},
        )
        self.yes_button.bind(on_release=self.yes_button_clicked)  # Bind the button event
        self.add_widget(self.yes_button)

        # Create the "No" button
        self.no_button = Button(
            text='No',
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.4, 'center_y': 0.1},
        )
        self.no_button.bind(on_release=self.no_button_clicked)  # Bind the button event
        self.add_widget(self.no_button)


        
        # Initialize button_image1 and button_image2 as instance variables
        self.button_image1 = None
        self.button_image2 = None
        self.image_widget = None
    def show_image(self, image_path):
        # Remove any existing image widget
        if self.image_widget is not None:
            self.remove_widget(self.image_widget)
        
        # Create a new image widget with the specified image path
        self.image_widget = Image(source=image_path, allow_stretch=True)
        self.add_widget(self.image_widget)

    def show_buttons(self):
        Clock.schedule_once(lambda dt: self.set_button_visibility(True), 0)

    def hide_buttons(self):
        Clock.schedule_once(lambda dt: self.set_button_visibility(False), 0)

    def set_button_visibility(self, visible):
        self.yes_button.disabled = not visible
        self.no_button.disabled = not visible
        self.yes_button.opacity = 1 if visible else 0
        self.no_button.opacity = 1 if visible else 0

    def timeout_callback(self, dt):
        self.remove_widget(self.image_widget)  # Remove the current image widget
        self.show_image(os.path.join(IMAGE_DIRECTORY, 'QRCode.png'))  # Display the new image
        Clock.schedule_once(self.close_image_callback, 10)  # Schedule the next timeout after 10 seconds
        self.show_buttons()
        
    def close_image_callback(self, dt):     
        
        self.remove_widget(self.image_widget)  # Remove the current image widget
        self.show_buttons()  # Show the buttons again

    def yes_button_clicked(self, instance):
        print('Yes button clicked')
        if not self.yes_button.disabled:
            self.hide_buttons()
            self.show_cover_buttons()

    def no_button_clicked(self, instance):
        print('No button clicked')

    def show_cover_buttons(self):
        self.remove_widget(self.yes_button)
        self.remove_widget(self.no_button)

        # Calculate the button size and position
        button_width = Window.width / 2
        button_height = Window.height

        # Create the first image button
        self.button_image1 = Button(
            background_normal=os.path.join(IMAGE_DIRECTORY, 'Cans.png'),
            size_hint=(None, None),
            size=(button_width, button_height),
            pos_hint={'x': 0, 'y': 0},
        )
        self.button_image1.bind(on_release=self.button_image1_clicked)
        self.add_widget(self.button_image1)

        # Create the second image button
        self.button_image2 = Button(
            background_normal=os.path.join(IMAGE_DIRECTORY, 'Bottles.png'),
            size_hint=(None, None),
            size=(button_width, button_height),
            pos_hint={'x': 0.5, 'y': 0},
        )
        self.button_image2.bind(on_release=self.button_image2_clicked)
        self.add_widget(self.button_image2)

        # Create the close button
        self.close_button = Button(
            text='Close',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'x': 0, 'top': 1},
        )
        self.close_button.bind(on_release=self.close_button_callback)  # Bind the button event
        self.add_widget(self.close_button)

        # Call show_buttons method to make "Yes" and "No" buttons visible again
        self.show_buttons()

    def button_image1_clicked(self, instance):
        print('Button image 1 clicked')
        self.remove_widget(self.button_image1)
        self.remove_widget(self.button_image2)
        self.remove_widget(self.close_button)
        self.image_widget = Image(source=os.path.join(IMAGE_DIRECTORY, 'WIP-Instructions.png'), allow_stretch=True)
        self.add_widget(self.image_widget)
        Clock.schedule_once(self.timeout_callback, 10)  # Schedule the timeout after 10 seconds

    def button_image2_clicked(self, instance):
        print('Button image 2 clicked')
        self.remove_widget(self.button_image1)
        self.remove_widget(self.button_image2)
        self.remove_widget(self.close_button)
        self.image_widget = Image(source=os.path.join(IMAGE_DIRECTORY, 'WIP-Instructions.png'), allow_stretch=True)
        self.add_widget(self.image_widget)
        Clock.schedule_once(self.timeout_callback, 10)  # Schedule the timeout after 10 seconds
    def close_button_callback(self, instance):
        print('Close button clicked')
        self.remove_widget(instance)
        self.remove_widget(self.button_image1)
        self.remove_widget(self.button_image2)
        self.remove_widget(self.image_widget)
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
    Window.size = (1920, 1080)  # Set the window size
    
    speech_thread = threading.Thread(target=start_speech_thread)
    speech_thread.daemon = True
    speech_thread.start()
    
    socket_thread = threading.Thread(target=listen_socket)
    socket_thread.daemon = True
    socket_thread.start()

    app = MyApp()
    app.run()
