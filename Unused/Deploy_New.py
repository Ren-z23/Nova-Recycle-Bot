import time
import cv2
import tensorflow as tf
import numpy as np
import RPi.GPIO as GPIO
import socket

model = tf.keras.models.load_model('Model_1.h5')

confidence = 0.5

# Motor driver pins
A_ENA_PIN = 4
A_IN1_PIN = 5
A_IN2_PIN = 6
A_IN3_PIN = 7
A_IN4_PIN = 8
A_ENB_PIN = 9

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up motor driver pins
GPIO.setup(A_ENA_PIN, GPIO.OUT)
GPIO.setup(A_IN1_PIN, GPIO.OUT)
GPIO.setup(A_IN2_PIN, GPIO.OUT)
GPIO.setup(A_IN3_PIN, GPIO.OUT)
GPIO.setup(A_IN4_PIN, GPIO.OUT)
GPIO.setup(A_ENB_PIN, GPIO.OUT)

ENA = GPIO.PWM(A_ENA_PIN, 100)  # Frequency of 100 Hz
ENB = GPIO.PWM(A_ENB_PIN, 100)  # Frequency of 100 Hz

speed = 100  # Speed of this robot

def A_up():
    ENA.start(speed)
    GPIO.output(A_IN1_PIN, GPIO.LOW)
    GPIO.output(A_IN2_PIN, GPIO.HIGH)

def A_down():
    ENA.start(speed)
    GPIO.output(A_IN1_PIN, GPIO.LOW)
    GPIO.output(A_IN2_PIN, GPIO.HIGH)

def A_stop():
    ENA.stop()
    GPIO.output(A_IN1_PIN, GPIO.LOW)
    GPIO.output(A_IN2_PIN, GPIO.LOW)

def B_up():
    ENB.start(speed)
    GPIO.output(A_IN3_PIN, GPIO.HIGH)
    GPIO.output(A_IN4_PIN, GPIO.LOW)

def B_down():
    ENB.start(speed)
    GPIO.output(A_IN3_PIN, GPIO.LOW)
    GPIO.output(A_IN4_PIN, GPIO.HIGH)

def B_stop():
    ENB.stop()
    GPIO.output(A_IN3_PIN, GPIO.LOW)
    GPIO.output(A_IN4_PIN, GPIO.LOW) 

host = socket.gethostname()  # localhost
port = 1234

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

server_socket.listen(1)

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection established from {client_address[0]}:{client_address[1]}")

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received data: {data}")

    # Process the received data or perform any desired actions
    if data == 'Classify':
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                image = np.copy(frame)
                image_resized = cv2.resize(image, (224, 224))
                image = np.array(image_resized) / 255.0  # Normalize the image
                image = tf.convert_to_tensor(image)
                image = tf.expand_dims(image, axis=0)  # Add a batch dimension
                results = model.predict(image)
                if results[0][0] > confidence:
                    predicted_class = 'Can'
                else:
                    predicted_class = 'Bottle'
                print(results)
                print("Predicted class:", predicted_class)
                # Motor control based on the predicted class
                if predicted_class == "Can":
                    print('Can')
                    A_stop()
                    # A_up()
                else:
                    print('Bottle')
                    A_down()
                    # B_down()
                time.sleep(0.2)
                A_stop()
        finally:
            pass
