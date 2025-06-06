  # Traffic Sign Classification Model


  ## Overview 

  This project is a deep learning-based traffic sign classification system implemented using TensorFlow. 
  The model is trained on the GTSRB (German Traffic Sign Dataset), which consists of various traffic sign images. 
  The goal is to recognize and classify different types of traffic signs accurately.

  ### Dependencies
- Python 3.10
- TensorFlow 2.13
- OpenCV
- NumPy
- Matplotlib
- Pandas
- scikit-learn


## Dataset
The German Traffic Sign Recognition Benchmark (GTSRB) dataset is used for training and testing the model. It includes more than 50000 images which are seperated 39,209 for training and 12,630 for tesing. The images are already resized to (32 x 32), have varying light conditions, rich backgrounds and are seperated in 43 unique classes.


## Data Processing

- Size of Training Set : 31367
- Size of Validation Set : 7841
- Size of Test Set : 12630
- Shape Of Images : (32, 32, 3)
- Number of unique Classes : 43

**Data Augmentation:**

- Data augmentation is crucial for improving model generalization. The `ImageDataGenerator` is used to perform various augmentations, including rotation, zooming, shifting, and shearing.
- Augmented images provide the model with variations of the training data, making it more robust to different real-world scenarios.

**Normalization:**

- Pixel values of images are normalized to the range [0, 1] by dividing by 255.0.
- Normalization helps the model converge faster during training and can improve accuracy.

**Label Encoding:**

- Labels are one-hot encoded using `tf.keras.utils.to_categorical` to match the output format required for categorical crossentropy loss.

## Model Architecture

**Convolutional Neural Network (CNN):**

- Convolutional layers extract spatial hierarchies of features from the input images.
- Batch Normalization is applied after convolutional layers to stabilize and accelerate the training process.

**MaxPooling:**

- Max pooling layers downsample the spatial dimensions, reducing computational complexity and focusing on essential features.

**Dropout:**

- Dropout layers (e.g., `Dropout(0.4)`) help prevent overfitting by randomly setting a fraction of input units to zero during training.

**Dense Layers:**

- Fully connected dense layers interpret the extracted features and make predictions.
- The final layer has softmax activation for multi-class classification.

## Training

**Hyperparameters :**

- Optimizer : Adam
- Learning Rate : 0.001
- Epochs : 15
- Batch Size : 32

**Results :**

- Training Accuracy : 99.26%
- Validation Accuracy : 99.92%
- Test Accuracy : 97.61%

## Summary 

The model features robust data processing, a CNN architecture with augmentation, and various training techniques for higher accuracy. Achieving 97.61% accuracy on the test set, the model is ready for use with provided example scripts. Explore, adapt, and contribute to enhance this traffic sign classification solution.

## Last Details

The Model was trained on a 2021 Macbook Pro with M1 Pro on a conda environment.

## References 

http://benchmark.ini.rub.de/?section=gtsrb&subsection=news
https://ieeexplore.ieee.org/document/6033395
https://www.sciencedirect.com/science/article/abs/pii/S0893608012000457?via%3Dihub







  

  
