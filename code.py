import os
import glob
base_dir = os.path.join('./cell_images')
infected_dir = os.path.join(base_dir,'Parasitized')
uninfected_dir = os.path.join(base_dir,'Uninfected')
infected_files = glob.glob(infected_dir+'/*.png')
uninfected_files = glob.glob(uninfected_dir+'/*.png')
len(infected_files)
len(uninfected_files)
import numpy as np
import pandas as pd

np.random.seed(42)

files_df = pd.DataFrame({
    'filename': infected_files + uninfected_files,
    'label': ['malaria'] * len(infected_files) + ['healthy'] * len(uninfected_files)
}).sample(frac=1, random_state=42).reset_index(drop=True)
from sklearn.model_selection import train_test_split
from collections import Counter

train_files, test_files, train_labels, test_labels = train_test_split(files_df['filename'].values,
                                                                      files_df['label'].values,
                                                                      test_size=0.4, random_state=42)
train_files, val_files, train_labels, val_labels = train_test_split(train_files,
                                                                    train_labels,
                                                                    test_size=0.1, random_state=42)

print(train_files.shape, val_files.shape, test_files.shape)
print('Train:', Counter(train_labels), '\nVal:', Counter(val_labels), '\nTest:', Counter(test_labels))
from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen=ImageDataGenerator(rescale=1./255,shear_range=0.2,zoom_range=0.2,horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)
x_train = train_datagen.flow_from_directory(r'C:\Users\Dell\Desktop\cell_images\cell_images',target_size=(64,64),batch_size=16,class_mode='binary')
x_test = test_datagen.flow_from_directory(r'C:\Users\Dell\Desktop\cell_images\cell_images',target_size=(64,64),batch_size=16,class_mode='binary')
print(x_train.class_indices)
img_width=64
img_height=64
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
"""model=Sequential()
model.add(Conv2D(32,(3,3),input_shape=(64,64,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(128,kernel_initializer='uniform',activation='relu'))
model.add(Dense(1,kernel_initializer='uniform',activation='sigmoid'))
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
"""
model=Sequential()
model.add(Conv2D(16,(3,3),input_shape=(img_width,img_height, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))

model.add(Conv2D(32,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(1,activation='sigmoid'))
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history=model.fit_generator(x_train,steps_per_epoch = 1000,epochs=5,validation_data=x_test,validation_steps=len(x_test))
model.save('mymodel.h5')
from tensorflow.keras.models import load_model
import cv2
model=load_model('mymodel.h5')
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
from skimage.transform import resize
def detect(frame):
    try:
        img=resize(frame,(64,64))
        img=np.expand_dims(img,axis=0)
        if(np.max(img)>1):
            img=img/255.0
        prediction=model.predict(img)
        print(prediction)
        prediction_class=model.predict_classes(img)
        print(prediction_class)
    except AttributeError:
        print('uninfected')
frame=cv2.imread('C1_thinF_IMG_20150604_104722_cell_15.png')
data=detect(frame)
import matplotlib.pyplot as plt
def plot_learningCurve(history,epoch):
    epoch_range=range(1,epoch+1)
    plt.plot(epoch_range,history.history['accuracy'])
    plt.plot(epoch_range,history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train','Val'],loc='upper left')
    plt.show()

    plt.plot(epoch_range,history.history['loss'])
    plt.plot(epoch_range,history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train','Val'],loc='upper left')
    plt.show()
plot_learningCurve(history,5)
