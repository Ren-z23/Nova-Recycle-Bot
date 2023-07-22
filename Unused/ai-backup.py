import tensorflow as tf
from keras import layers, models
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np

import cv2
import time

# Enable GPU memory growth for all available GPUs
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)
else:
    print("No GPU devices found. Using CPU.")

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class AI():
    def __init__(self) -> None:
        try:
            self.model = tf.keras.models.load_model('image_classification_model.h5')
        except:
            print('No model detected... \n Training...')
            self.train()
            
    def take_pictures(self,label, camera_label=0, num_of_images=1000, reshape=None):
        # Create a directory for the specified label if it doesn't exist
        save_directory = os.path.join('Assets/ImageClassification', label)
        os.makedirs(save_directory, exist_ok=True)

        cap = cv2.VideoCapture(camera_label)
        num_images = 0

        # Function to create a transparent overlay with text
        def create_overlay_text(text, frame):
            overlay = frame.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            font_thickness = 2
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
            text_x = 10
            text_y = text_size[1] + 10
            cv2.putText(overlay, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)
            return cv2.addWeighted(frame, 1, overlay, 0.6, 0)

        # Show camera feed with text overlay for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5:
            ret, frame = cap.read()
            text = f'Taking images in {int(5 - (time.time() - start_time))} seconds...'
            frame_with_overlay = create_overlay_text(text, frame)
            cv2.imshow('Camera', frame_with_overlay)
            cv2.waitKey(1)

        # Release the camera and close the OpenCV window to reset the camera capture
        cap.release()
        cv2.destroyAllWindows()

        # Reopen the camera to capture images again
        cap = cv2.VideoCapture(camera_label)

        # Start capturing images
        while True:
            ret, frame = cap.read()
            num_images += 1

            # If a reshape tuple is provided, apply reshaping to the image
            if reshape is not None and isinstance(reshape, tuple):
                frame = cv2.resize(frame, reshape)

            # Display the number of images in the top right corner
            text = f'Images taken: {num_images}'
            frame_with_overlay = create_overlay_text(text, frame)
            cv2.imshow('Camera', frame_with_overlay)

            # Save the image in the new folder
            image_filename = os.path.join(save_directory, f'{label}_image_{num_images}.png')
            cv2.imwrite(image_filename, frame)

            # Exit the loop when the desired number of images is taken
            if num_images >= num_of_images:
                break

            # Exit the loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the OpenCV window
        cap.release()
        cv2.destroyAllWindows()
    def train(self):

        tf.random.set_seed(42)

        # Limit GPU memory growth
        physical_devices = tf.config.list_physical_devices('GPU')
        if physical_devices:
            for device in physical_devices:
                tf.config.experimental.set_memory_growth(device, True)

        # Define the main data folder
        main_folder = "Assets/ImageClassification"

        # Define the ImageDataGenerator for data augmentation and preprocessing
        datagen = ImageDataGenerator(
            rescale=1.0/255.0,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            preprocessing_function=lambda img: tf.image.resize(img, [224, 224]),
            validation_split=0.1
        )

        # Load and augment images from the subfolders using ImageDataGenerator
        train_generator = datagen.flow_from_directory(
            main_folder,
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            subset='training'
        )

        validation_generator = datagen.flow_from_directory(
            main_folder,
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            subset='validation'
        )

        # Create the model
        num_classes = train_generator.num_classes

        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])

        model.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

        history = model.fit(train_generator, epochs=10, validation_data=validation_generator)

        # Optional: Save the model for future use
        model.save("image_classification_model.h5")
        print('Training Done!')
        
        # Optional: Visualize the training process
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label='val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend(loc='lower right')
        plt.show()
    def predict(self,image_path):
    

        # Get class names from the folder names
        main_folder = "Assets/ImageClassification"
        class_names = sorted(os.listdir(main_folder))

        # Load and preprocess the image
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        img_array = img_array / 255.0  # Normalize the pixel values to [0, 1]

        # Make the prediction
        predictions = self.model.predict(img_array)
        class_index = tf.argmax(predictions[0])

        # Print the predicted class and its probability
        predicted_class = class_names[class_index]
        probability = np.max(predictions[0])

        print(f"Image: {image_path}")
        print(f"Predicted Class: {predicted_class}")
        print(f"Probability: {probability:.2f}")
        print("")
        return predicted_class, probability

    def loop_predict(self, image_path):
        try:
            while True:
                predicted_class, probability = self.predict(image_path)
                
                
                time.sleep(1)  # Add a pause of 1 second between predictions

        except KeyboardInterrupt:
            print("Loop interrupted. Stopping predictions.")