import os
import numpy as np
from PIL import Image
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model
import cv2
import time
IMAGESIZE=224 

# Define paths to your cat images and other cat images
my_cat_path = "C:/Users/robin/OneDrive/Documents/homework_2024/electronics_project/my_cat/"
other_cats_path = "C:/Users/robin/OneDrive/Documents/homework_2024/electronics_project/other_cats/"

# Function to load and preprocess images from a directory
def load_images_from_dir(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            img = Image.open(os.path.join(directory, filename))
            img = img.resize((IMAGESIZE, IMAGESIZE))  # Resize images to 224x224
            img = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
            images.append(img)
    return np.array(images)

# Load images from directories
my_cat_images = load_images_from_dir(my_cat_path)
other_cat_images = load_images_from_dir(other_cats_path)

# Create labels (0 for other cats, 1 for your cat)
my_cat_labels = np.ones(len(my_cat_images))
other_cat_labels = np.zeros(len(other_cat_images))

# Combine data and labels
X = np.concatenate((my_cat_images, other_cat_images), axis=0)
y = np.concatenate((my_cat_labels, other_cat_labels), axis=0)

# Shuffle the data
indices = np.arange(X.shape[0])
np.random.shuffle(indices)
X = X[indices]
y = y[indices]

# Split the data into training and validation sets
split = int(0.8 * len(X))
X_train, X_val = X[:split], X[split:]
y_train, y_val = y[:split], y[split:]
# Create MobileNet model with custom output layer
base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(IMAGESIZE, IMAGESIZE, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(1, activation='sigmoid')(x)  # Assuming binary classification
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
# Compute class weights

total_samples = len(y_train)
class_counts = np.bincount(y_train.astype(int))
class_weights = {cls: total_samples / count for cls, count in enumerate(class_counts)}

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    zoom_range=0.2,
    shear_range=0.2,
    fill_mode='nearest')

# Early stopping to prevent overfitting
early_stopping = EarlyStopping(patience=3, restore_best_weights=True)

# Train the model with data augmentation and class weights

model.fit(
    
    datagen.flow(X_train, y_train, batch_size=1),
    steps_per_epoch=len(X_train),
    epochs=10,
    validation_data=(X_val, y_val),
    class_weight=class_weights,
    callbacks=[early_stopping]

)




 # Load and preprocess the image
img = Image.open(<path_to_test_image>)
img = img.resize((IMAGESIZE, IMAGESIZE))
img = np.array(img) / 255.0

# Make prediction
prediction = model.predict(np.expand_dims(img, axis=0))
print(prediction)
# Classify as 'Your Cat' if prediction is closer to 1, otherwise classify as 'Other Cat'
if prediction > 0.5:
    print("Your cat!")
else:
    print("Other cat.")
    
model.save("cat_classifier_model7.keras")




loaded_model = load_model("cat_classifier_model7.keras")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("לא ניתן לפתוח את המצלמה. בדוק כי היא מחוברת ונסה שוב.")
while True:
    ret, frame = cap.read()

    if not ret:
        print("לא ניתן לקרוא מהמצלמה.")
    
    cv2.imwrite('image.jpg', frame)
    
    img = Image.open("image.jpg").convert("RGB")
 # Load and preprocess the image
    img = img.resize((IMAGESIZE, IMAGESIZE))
    img = np.array(img) / 255.0
    
    # Make prediction
    prediction = loaded_model.predict(np.expand_dims(img, axis=0))
    print(prediction)
    print(prediction)
    # Classify as 'Your Cat' if prediction is closer to 1, otherwise classify as 'Other Cat'
    if prediction > 0.5:
        print("Your cat!")
    else:
        print("Other cat.")
    
    time.sleep(1)



            
