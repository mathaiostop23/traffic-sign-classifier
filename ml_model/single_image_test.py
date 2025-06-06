import numpy as np
import tensorflow as tf
import cv2
import os 

model = tf.keras.models.load_model('./traffic_sign.keras')

class_names = np.array(['Speed limit (20km/h)', 'Speed limit (30km/h)', 'Speed limit (50km/h)', 'Speed limit (60km/h)', 'Speed limit (70km/h)', 'Speed limit (80km/h)', 'End of speed limit (80km/h)', 'Speed limit (100km/h)', 'Speed limit (120km/h)', 'No passing', 'No passing for vehicles over 3.5 metric tons', 'Right-of-way at the next intersection', 'Priority road', 'Yield', 'Stop', 'No vehicles', 'Vehicles over 3.5 metric tons prohibited', 'No entry', 'General caution', 'Dangerous curve to the left', 'Dangerous curve to the right', 'Double curve', 'Bumpy road', 'Slippery road', 'Road narrows on the right', 'Road work', 'Traffic signals', 'Pedestrians', 'Children crossing', 'Bicycles crossing', 'Beware of ice/snow', 'Wild animals crossing', 'End of all speed and passing limits', 'Turn right ahead', 'Turn left ahead', 'Ahead only', 'Go straight or right', 'Go straight or left', 'Keep right', 'Keep left', 'Roundabout mandatory', 'End of no passing', 'End of no passing by vehicles over 3.5 metric tons'])


img_path = './50km.jpeg'
image = cv2.imread(os.path.join(img_path))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (32, 32))
img_array = np.array(image)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array.astype('float32') / 255.0

predictions = model.predict(img_array)
class_idx = np.argmax(predictions[0])
class_confidence = predictions[0][class_idx]
if class_confidence > 0.9:
            class_label = int(class_idx)
            class_label = class_names[class_label]
            class_confidence = class_confidence *100
else:
            class_label = "Not Sure"
            class_confidence = class_confidence *100
            
print ("The Predicted Class Is :",class_label,"",class_confidence,"%")