import numpy as np
import os
import cv2
import pandas as pd 
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.utils import shuffle
import matplotlib.pyplot as plt 

print("TensorFlow version:", tf.__version__)
print("Metal device available:", 
      len(tf.config.list_physical_devices('GPU')) > 0)

np.random.seed(42)

class_names = np.array(['Speed limit (20km/h)', 'Speed limit (30km/h)', 'Speed limit (50km/h)', 'Speed limit (60km/h)', 'Speed limit (70km/h)', 'Speed limit (80km/h)', 'End of speed limit (80km/h)', 'Speed limit (100km/h)', 'Speed limit (120km/h)', 'No passing', 'No passing for vehicles over 3.5 metric tons', 'Right-of-way at the next intersection', 'Priority road', 'Yield', 'Stop', 'No vehicles', 'Vehicles over 3.5 metric tons prohibited', 'No entry', 'General caution', 'Dangerous curve to the left', 'Dangerous curve to the right', 'Double curve', 'Bumpy road', 'Slippery road', 'Road narrows on the right', 'Road work', 'Traffic signals', 'Pedestrians', 'Children crossing', 'Bicycles crossing', 'Beware of ice/snow', 'Wild animals crossing', 'End of all speed and passing limits', 'Turn right ahead', 'Turn left ahead', 'Ahead only', 'Go straight or right', 'Go straight or left', 'Keep right', 'Keep left', 'Roundabout mandatory', 'End of no passing', 'End of no passing by vehicles over 3.5 metric tons'])

data_dir = './'
train_path = './Train'
test_path = './Test'


input_shape = (32, 32, 3)
num_classes = len(os.listdir(train_path))
batch_size = 32
epochs = 15

image_data = []
image_labels = []

for i in range(num_classes):
    path = os.path.join(train_path, str(i))
    images = os.listdir(path)
    for img in images:
        image = cv2.imread(os.path.join(path, img))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        resize_image = cv2.resize(image, (32, 32))
        image_data.append(resize_image)
        image_labels.append(i)
    
    
    
image_data = np.array(image_data)
image_labels = np.array(image_labels)

print(image_data.shape, image_labels.shape)

image_data, image_labels = shuffle(image_data, image_labels, random_state=42)

X_train, X_val, y_train, y_val = train_test_split(image_data, image_labels, test_size=0.2, random_state=42)

X_train = X_train / 255  # Normalize pixel values to [0, 1]
X_val = X_val / 255

y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_val = tf.keras.utils.to_categorical(y_val, num_classes)

print(y_train.shape)
print(y_val.shape)



model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape))
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(num_classes, activation='softmax'))

model.summary()

aug = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.15,
    horizontal_flip=False,
    vertical_flip=False,
    fill_mode="nearest")


opt = Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])



history = model.fit(aug.flow(X_train, y_train, batch_size=batch_size), epochs=epochs, validation_data=(X_val, y_val))



test = pd.read_csv('./Test.csv')
labels = test["ClassId"].values
imgs = test["Path"].values

X_test = []
for img in imgs:
    image = cv2.imread(os.path.join(data_dir, img))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resize_image = cv2.resize(image, (32, 32))
    X_test.append(resize_image)

X_test = np.array(X_test) / 255

pred_prob = model.predict(X_test)
pred_classes = np.argmax(pred_prob, axis=1)

#Accuracy with the test data
test_accuracy = accuracy_score(labels, pred_classes) * 100
print('Test Data accuracy: {:.2f}%'.format(test_accuracy))

plt.figure(figsize = (7, 7))

start_index = 0
for i in range(40):
    plt.subplot(8, 6, i + 1)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    prediction = pred_classes[start_index + i]
    actual = labels[start_index + i]
    col = 'g'
    if (prediction != actual).all():
        col = 'r'
    plt.xlabel('Actual={} || Pred={}'.format(class_names[actual], class_names[prediction]), color = col)
    plt.imshow(X_test[start_index + i])
plt.show()


model.save('TrafficSign.keras')