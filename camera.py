from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np
import serial
import time
import cv2

try:
    ser = serial.Serial('COM9', 9600) 
    time.sleep(2) 
    print("מחובר לארדואינו על COM89.")
except Exception as e:
    print(f"שגיאה בחיבור לארדואינו: {e}")
    
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("לא ניתן לפתוח את המצלמה. בדוק כי היא מחוברת ונסה שוב.")
    

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

while True:
    ret, frame = cap.read()

    if not ret:
        print("cant read from camera.")
    
    cv2.imwrite('image.jpg', frame)
    
    image = Image.open("image.jpg").convert("RGB")
    
    
    
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    # turn the image into a numpy array
    image_array = np.asarray(image)
    
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Load the image into the array
    data[0] = normalized_image_array
    
    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]   
    #some mumbo jumbo i did for my one model, fix it for your model
    print(class_name[8], "  ", confidence_score)

    if class_name[8]=='2' and confidence_score>0.75:
        ser.write(b'2')
        time.sleep(1)
    else:
        ser.write(b'1')
        time.sleep(1)
    
    

