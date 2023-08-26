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
import kivy
import time
import asyncio
import websockets
import control_panel
from kivy.animation import Animation
from kivy.graphics.texture import Texture
from functools import partial
import qrcode
import pygame



monitor_ip = '192.168.1.100'   #Change to the ip of the computer that is acting as the GUI
website_node_ip = '192.168.1.100'    #Change to the ip of the computer that is hosting the website

Window.fullscreen = "auto"
test = True   #If its true, it will use the current computer's camera instead of waiting for a prediction from another computer
Tokens = ['token1', 'token2', 'token3', 'token4', 'token5']  #Tokens that will be used
qr_code_link = f'{website_node_ip}/Server/index.php?token='
IMAGE_DIRECTORY = "Assets/GUI/Images"
Used_Tokens = []


class ImageBackground(FloatLayout):
    def __init__(self, **kwargs):
        self.minister = False
        #threading.Thread(target=self.move).start()               #Uncomment this to move the robot

        super(ImageBackground, self).__init__(**kwargs)
        self.predicted_label = 'Background'
        self.previous_predicted_label = None
        self.audio_lock = False
        self.frame = None
        self.prediction_thread = None
        self.additional_image_widget = None
        self.current_predicted_label = None
        self.accept_lock = False
        self.base_lock = False
        self.move_queued = True

        
        threading.Thread(target=self.listen_socket2).start()
        threading.Thread(target=self.listen_socket3).start()


        self.background = Image(                  
            source=os.path.join(IMAGE_DIRECTORY, "background.png"),
            allow_stretch=True,
        )
        self.add_widget(self.background)

        self.relative_layout = FloatLayout()
        self.add_widget(self.relative_layout)

        with self.relative_layout.canvas.before:
            Color(0x25 / 255.0, 0x22 / 255.0, 0x3C / 255.0, 1)
            self.rect = Rectangle(pos=(0, 800), size=(2500, 200))

        
        
        self.predicted_label = Label(
            text="", 
            color=(1, 1, 1, 1),
            font_size=120,
            size_hint=(None, None),
            size=(Window.width, 100),
            pos_hint={"center_x": 0.2, "top": 0.86},
        )
        

        self.yes_button = Button(
            text="Yes",
            font_size = 16,
            size_hint=(None, None),
            size=(300, 150),
            pos_hint={"center_x": 0.7, "center_y": 0.3},
        )
        self.yes_button.bind(on_release=self.yes_button_clicked)
        self.add_widget(self.yes_button)

        self.no_button = Button(
            text="No",
            font_size=16,
            size_hint=(None, None),
            size=(300, 150),
            pos_hint={"center_x": 0.3, "center_y": 0.3},
        )
        self.no_button.bind(on_release=self.no_button_clicked)
        self.add_widget(self.no_button)
        
        self.close_button = Button(
            text="Close",
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"x": 0.1, "top": 0.9},
        )

        self.Accept_button = Button(
            text="Acccepted",
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={"center_x": 0.2, "center_y": 0.5},
        )
        self.Accept_button.bind(on_release=self.accept_button_clicked)
        
        

        self.image_widget = None
    def move(self):          #This will only work if the robot base is the same one as shown in the readme.
        self.play_audio(os.path.join('Assets', 'Audio', 'Intro.mp3'))
        os.system('rosservice call /gobot_command/play_path')
        time.sleep(20)
        self.play_audio(os.path.join('Assets', 'Audio', 'Leave30Seconds.mp3'))
        time.sleep(10)
        self.play_audio(os.path.join('Assets', 'Audio', 'Question.mp3'))
        os.system('rosservice call /gobot_command/pause_path')
        time.sleep(10)

        
        while True:
            if self.base_lock == False:
                os.system('rosservice call /gobot_command/play_path')
                break
            else:
                time.sleep(1)
        os.system('rosservice call /gobot_command/play_path')
        time.sleep(20)
        self.play_audio(os.path.join('Assets', 'Audio', 'Leave30Seconds.mp3'))
        time.sleep(8)
        self.play_audio(os.path.join('Assets', 'Audio', 'Question.mp3'))
        os.system('rosservice call /gobot_command/pause_path')
        time.sleep(10)
        
        while True:
            if self.base_lock == False:
                os.system('rosservice call /gobot_command/play_path')
                break
            else:
                time.sleep(1)
        os.system('rosservice call /gobot_command/play_path')
        time.sleep(20)
        self.play_audio(os.path.join('Assets', 'Audio', 'Leave30Seconds.mp3'))
        time.sleep(8)
        self.play_audio(os.path.join('Assets', 'Audio', 'Question.mp3'))
        os.system('rosservice call /gobot_command/pause_path')
        time.sleep(10)
        while True:
            if self.base_lock == False:
                os.system('rosservice call /gobot_command/play_path')
                break
            else:
                time.sleep(1)

    def accept_button_clicked(self, instance):       #The button that shows if a whitelisted item is scanned
        print("Accept Button Clicked")

        # Remove the QR code image widget if it exists
        if hasattr(self, "QR_code") and self.QR_code:
            self.remove_widget(self.QR_code)
        
        current_generated_token = Tokens[0]             
        Used_Tokens.append(current_generated_token) 
        Tokens.remove(current_generated_token)

        self.create_qr_code(current_generated_token)

        # Create a new QR code image widget with the updated QR code image
        self.QR_code = Image(
            source=os.path.join(IMAGE_DIRECTORY, "Token_QR_Code.png"),
            allow_stretch=True,
            size=(750, 750),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        
        #Reloading a new qr code after removing the old one
        self.QR_code.reload()
        # Remove the predicted label from its current parent
        if self.predicted_label.parent:
            self.predicted_label.parent.remove_widget(self.predicted_label)

        # Remove the 'Accept' button from the layout
        if self.Accept_button in self.children:
            self.remove_widget(self.Accept_button)

        # Add the new QR code image widget when "Accepted" button is clicked
        self.add_widget(self.QR_code)
        
        self.accept_lock = True

        # Schedule the function to check the predicted label
        Clock.schedule_once(self.check_predicted_label, 0.5)

    #Create audio thread in order to not stop the GUI
    def play_audio_thread(self,audio_file):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        self.audio_lock = True

    def play_audio(self,audio_file):
        
        audio_thread = threading.Thread(target=self.play_audio_thread, args=(audio_file,))
        audio_thread.start()
    
    
    #Check the predicted label and act accordingly
    def check_predicted_label(self, dt):
        # Get the current predicted label

        predicted_label = self.predicted_label.text
        
        #Locking the audio
        if self.previous_predicted_label != self.predicted_label and self.audio_lock == True:
            self.audio_lock = False
            self.previous_predicted_label = self.predicted_label
        if predicted_label == "Bottles":
            
            if self.audio_lock == False:
                self.play_audio(os.path.join('Assets', 'Audio', 'Accepted.mp3'))
            # Add the Accept_button to the layout if not already added
            if self.Accept_button not in self.children:
                if self.accept_lock == False:
                    try:
                        self.add_widget(self.Accept_button)
                    except:
                        pass
        elif predicted_label == 'Cans':
            if self.audio_lock == False:
                self.play_audio(os.path.join('Assets', 'Audio', 'Accepted.mp3'))
            # Add the Accept_button to the layout if not already added
            if self.Accept_button not in self.children:
                if self.accept_lock == False:
                    try:
                        self.add_widget(self.Accept_button)
                    except:
                        pass
        

        # Schedule the function to run again after a certain interval (e.g., 1 second)
        Clock.schedule_once(self.check_predicted_label, 1.0)


    def initiate_image_change(self, dt):
        self.show_additional_image_with_animation()


    def yes_button_clicked(self, instance):
        self.audio_lock = False
        self.base_lock = True
        print("Yes button clicked")
        self.play_audio(os.path.join('Assets', 'Audio', 'Normal.mp3'))
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


            # Start the function to check the predicted label
            Clock.schedule_once(self.check_predicted_label, 0.5)
            # Show the additional image with animation
            Clock.schedule_once(self.initiate_image_change, 0.5)  # Delay the function call
            self.accept_lock = False





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

        new_width = 500
        aspect_ratio = original_image.width / original_image.height
        new_height = new_width/aspect_ratio
        self.additional_image_widget.size=(200,200)

        # Set the initial position of the additional image (center of the screen)
        self.additional_image_widget.center = (600, 0)

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
        self.base_lock = False
        if self.image_widget:
            self.remove_widget(self.image_widget)
            self.image_widget = None

    def close_button_callback(self, instance):
        self.predicted_label.text = 'Background'
        print("Close button clicked")
        self.play_audio(os.path.join('Assets', 'Audio', 'Intro.mp3'))
        if self.move_queued == True and self.base_lock == False:
            self.move_queued = False
        if self.Accept_button  in self.children:
            self.remove_widget(self.Accept_button)
        self.remove_widget(instance)
        self.show_buttons()
        self.relative_layout.remove_widget(self.predicted_label)
        self.add_widget(self.yes_button)
        self.add_widget(self.no_button)
        if self.Accept_button not in self.children:
            try:
                self.remove_widget(self.QR_code)
            except:
                pass

        # Remove the additional image when 'Close' is clicked
        if self.additional_image_widget:
            self.remove_widget(self.additional_image_widget)
            self.additional_image_widget = None

    def on_yes_button_clicked(self, instance):
        self.yes_button_clicked(instance)
        
    
    def on_close_button_clicked(self, instance):
        self.close_button_callback(instance)

    
    #Socket 2 listens for the jetson nano's prediction and forward to rest of the code
    def listen_socket2(self):
        global command
        # Create a socket server
        server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address2 = (monitor_ip, 1236)
        server_socket2.bind(server_address2)
        server_socket2.listen(1)
        print("Socket server started, listening for commands...")

        while True:
            # Accept client connection
            client_socket2, address2 = server_socket2.accept()
            print("Client connected:", address2)

            # Receive command from client
            predicted_label = client_socket2.recv(1024).decode()
            if predicted_label == 'Background':
                self.predicted_label.text = ''
            else:
                self.predicted_label.text = predicted_label
            # Process the command (e.g., perform actions based on the received command)
            print("Received command:", self.predicted_label.text)
            

            # Close the client socket
            client_socket2.close()
            print(f'Class: {self.predicted_label.text}')
            
    #Socket 3 listens to command from computer and instructs the robot base to move
    def listen_socket3(self):
        # Create a socket server
        server_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address3 = (monitor_ip, 1237)
        server_socket3.bind(server_address3)
        server_socket3.listen(1)
        print("Socket server started, listening for commands...")

        while True:
            # Accept client connection
            client_socket3, address3 = server_socket3.accept()
            print("Client connected:", address3)

            # Receive command from client
            move_cmd = client_socket3.recv(1024).decode()
            # Process the command (e.g., perform actions based on  received command)
            print("Received command:", move_cmd)
            # Close the client socket
            client_socket3.close()
            if move_cmd == 'move':
                os.system('rosservice call /gobot_command/play_path')
            elif move_cmd == 'pause':
                os.system('rosservice call /gobot_command/pause_path')
            elif move_cmd == 'stop':
                os.system('rosservice call /gobot_command/stop_path')
            move_cmd = None

    def create_qr_code(self,text):


        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_link + text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(os.path.join(IMAGE_DIRECTORY, 'Token_QR_Code.png'))

class MyApp(App):
    def build(self):
        image_background = ImageBackground()
        return image_background


if __name__ == "__main__":
    Window.size = (1920, 1080)

    app = MyApp()
    app.run()

