from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
import threading
import pyttsx3
import socket
import os
import ai
import cv2
import kivy
import time
import asyncio
import websockets
import control_panel
from kivy.animation import Animation
from kivy.graphics.texture import Texture
from functools import partial

my_ip = "192.168.0.100"
camera_mode = True
camera_index = 1
custom_image = ""  # ImagePath


def get_own_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


Computer_IP = get_own_ip()
Window.fullscreen = "auto"

shown_text = "Hello World!"

IMAGE_DIRECTORY = "Assets\GUI\Images"


class ImageBackground(FloatLayout):
    def __init__(self, **kwargs):
        super(ImageBackground, self).__init__(**kwargs)

        self.predicter = ai.AI()  # Create an instance of the AI class
        self.frame = None
        self.prediction_thread = None
        self.additional_image_widget = None
        self.current_predicted_label = None

        threading.Thread(target=self.start_control_panel).start()
        threading.Thread(target=self.listen_socket).start()
        threading.Thread(target=self.start_speech_thread).start()

        if camera_mode is True:
            threading.Thread(target=self.video_capture_thread).start()

        self.background = Image(
            source=os.path.join(IMAGE_DIRECTORY, "heretorecycle.png"),
            allow_stretch=True,
        )
        self.add_widget(self.background)

        self.relative_layout = FloatLayout()
        self.add_widget(self.relative_layout)

        with self.relative_layout.canvas.before:
            Color(0x25 / 255.0, 0x22 / 255.0, 0x3C / 255.0, 1)
            self.rect = Rectangle(pos=(0, 775), size=(1920, 200))

        self.label = Label(
            text=f"{shown_text}",
            color=(1, 1, 1, 1),
            font_size=80,
            size_hint=(None, None),
            size=(Window.width, 100),
            pos_hint={"center_x": 0.5, "top": 0.88},
        )
        self.relative_layout.add_widget(self.label)
        
        
        self.predicted_label = Label(
            text="",  # Initialize the text as empty
            color=(1, 1, 1, 1),
            font_size=120,
            size_hint=(None, None),
            size=(Window.width, 100),
            pos_hint={"center_x": 0.2, "top": 0.86},
        )
        #self.relative_layout.add_widget(self.predicted_label)
        

        self.yes_button = Button(
            text="Yes",
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.6, "center_y": 0.1},
        )
        self.yes_button.bind(on_release=self.yes_button_clicked)
        self.add_widget(self.yes_button)

        self.no_button = Button(
            text="No",
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.4, "center_y": 0.1},
        )
        self.no_button.bind(on_release=self.no_button_clicked)
        self.add_widget(self.no_button)

        self.image_widget = None
        self.predicter = ai.AI()
        if camera_mode is True:
            threading.Thread(target=self.predict_and_show, args=(self.frame)).start()
        else:
            threading.Thread(
                target=self.predict_and_show, args=(os.path.join(custom_image),)
            ).start()

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

    def initiate_image_change(self, dt):
        self.show_additional_image_with_animation()

    def predict_and_show(self, image_path):
        predicted_class, probability, image = self.predicter.predict(image_path)
        prediction_text = f"Predicted Class: {predicted_class}\nProbability: {probability:.2f}"
        print(prediction_text)

        # Check if the predicted label has changed
        if predicted_class != self.current_predicted_label:
            self.current_predicted_label = predicted_class
            # Fade out the current image and fade in the new image
            self.show_additional_image_with_animation()

        # Update the predicted_label with the new predicted class
        self.predicted_label.text = predicted_class

    def yes_button_clicked(self, instance):
        print("Yes button clicked")
        if not self.yes_button.disabled:
            self.hide_buttons()
            self.show_cover_buttons()

            # Remove the predicted_label from its current parent before adding it again
            if self.predicted_label.parent:
                self.predicted_label.parent.remove_widget(self.predicted_label)

            # Add the predicted_label to the relative_layout
            self.relative_layout.add_widget(self.predicted_label)

            # Load the temporary image and add it as a widget
            temp_image_name = f"{self.predicted_label.text}.png"
            temp_image_path = os.path.join("Assets", "GUI", "ImageClasses", temp_image_name)

            # Show the additional image with animation
            Clock.schedule_once(self.initiate_image_change, 0.5)  # Delay the function call





    def show_additional_image_with_animation(self):
        if self.additional_image_widget:
            # If there's an existing additional image widget, remove it with a fade-out animation
            Animation(opacity=0, duration=0.5).start(self.additional_image_widget)
            # Schedule the update_image_texture method after the fade-out animation completes
            Clock.schedule_once(self.update_image_texture, 0.5)
        else:
            # If there's no existing additional image widget, directly update the image texture
            self.update_image_texture()
    def update_image_texture(self, dt=None):
        # Get the predicted label
        predicted_class = self.predicted_label.text

        # Construct the image path based on the predicted label
        temp_image_name = f"{predicted_class}.png"
        temp_image_path = os.path.join("Assets", "GUI", "ImageClasses", temp_image_name)

        # Check if the image file exists before creating the CoreImage object
        try:
            with open(temp_image_path, "rb") as f:
                pass
        except FileNotFoundError:
            print(f"Image file not found: {temp_image_path}")
            return

        

        # Load the image
        original_image = CoreImage(temp_image_path, ext="png").texture

        # Create a new Image widget with the texture and add it to the layout
        self.additional_image_widget = Image(texture=original_image, allow_stretch=True)
        self.add_widget(self.additional_image_widget)

        # Set the initial position of the additional image (center of the screen)
        self.additional_image_widget.center = (Window.width / 2, Window.height / 2)

        # Animate the image (fade-in) with a duration of 0.5 seconds
        self.additional_image_widget.opacity = 0
        Animation(opacity=1, duration=0.5).start(self.additional_image_widget)

        # Schedule the removal of the old image widget after the fade-in animation completes
        Clock.schedule_once(self.remove_old_image_widget, 0.5)
        
    def remove_old_image_widget(self, dt=None):
        # Remove the old additional image widget after the fade-in animation completes
        if self.image_widget:
            self.remove_widget(self.image_widget)
            self.image_widget = None
            
    def start_animation(self):
        if self.additional_image_widget is None:         
            # No additional image widget, so animation cannot start
            return

        # Create an animation to move the additional image to the right within 1 second
        anim = Animation(x=300, duration=0.75)

        # Start the animation
        anim.start(self.additional_image_widget)


    def no_button_clicked(self, instance):
        print("No button clicked")

    def hide_buttons(self):
        Clock.schedule_once(lambda dt: self.set_button_visibility(False), 0)

    def show_cover_buttons(self):
        self.remove_widget(self.yes_button)
        self.remove_widget(self.no_button)
        button_width = Window.width / 2
        button_height = Window.height

        self.close_button = Button(
            text="Close",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"x": 0, "top": 1},
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
        print("Close button clicked")
        self.remove_widget(instance)
        self.show_buttons()
        self.relative_layout.remove_widget(self.predicted_label)
        self.add_widget(self.yes_button)
        self.add_widget(self.no_button)

        # Remove the additional image when 'Close' is clicked
        if self.additional_image_widget:
            self.remove_widget(self.additional_image_widget)
            self.additional_image_widget = None

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
            if command == "as":
                # ImageBackground.finished_detection_image()
                for i in range(100):
                    print("finished detection")

    def start_control_panel(self):
        control_panel.app.run(host="0.0.0.0", port=5001)

    def start_speech_thread(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        server_address = (socket.gethostbyname(hostname), 1235)
        server_socket.bind(server_address)
        server_socket.listen(1)
        print("Socket server started, listening for commands...")

        def speak(text):
            engine = pyttsx3.init()

            # Set the voice
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[1].id)
            # Set the rate
            # engine.setProperty('rate', rate)
            engine.say(text)
            engine.runAndWait()

        while True:
            # Accept client connection
            client_socket, address = server_socket.accept()
            print("Client connected:", address)
            # Receive command from client
            command = client_socket.recv(1024).decode()
            # Process the command
            print("Saying:", command)
            speak(command)
            client_socket.close()


def run_websocket_server():
    async def handle_message(websocket, path):
        async for message in websocket:
            # Here, 'message' contains the data sent by the client (predicted class and probability)
            # Process the message and respond accordingly
            # For example, you can print the received message
            print(f"Received message: {message}")

            # Do other actions based on the message (e.g., call a function for further processing)
            # For instance, you can extract the predicted class and probability from the JSON message
            # and perform specific actions based on the content of the message.

    # Start the WebSocket server
    start_server = websockets.serve(handle_message, my_ip, 1234)

    # Run the event loop
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


class MyApp(App):
    def build(self):
        image_background = ImageBackground()
        return image_background


if __name__ == "__main__":
    Window.size = (1920, 1080)

    app = MyApp()
    app.run()

""" hostname=socket.gethostname()
print((socket.gethostbyname(hostname), 1234)) """
