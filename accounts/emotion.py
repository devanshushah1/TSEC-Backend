import numpy as np
import argparse
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from tensorflow.keras.models import load_model


def emotion():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", help="train/display")
    mode = ap.parse_args().mode

    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu', input_shape=(48, 48, 1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))
    model.load_weights('emotion.h5')

    cv2.ocl.setUseOpenCL(False)

    emotion = {0: "Angry", 1: "Disgusted", 2: "Fearful",
               3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    def FrameCapture(path):
        counter = {
            "Angry": 0,
            "Disgusted": 0,
            "Fearful": 0,
            "Happy": 0,
            "Neutral": 0,
            "Sad": 0,
            "Surprised": 0
        }
        # Path to video file
        vidObj = cv2.VideoCapture(path)

        # Used as counter variable
        count = 0

        # checks whether frames were extracted
        success = 1

        while success:
            # vidObj object calls read
            # function extract frames
            success, frame = vidObj.read()
            # Saves the frames with frame-count
            if not success:
                break
            face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            finalface = face.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5)
            print('abc', finalface)
            print(456)

            for (x, y, w, h) in finalface:
                finalgray = gray[y:y + h, x:x + w]
                cropimg = np.expand_dims(np.expand_dims(
                    cv2.resize(finalgray, (48, 48)), -1), 0)
                predict = model.predict(cropimg)
                maxi = int(np.argmax(predict))
                counter[emotion[maxi]] += 1
                print(123)

        return counter

    print(FrameCapture('WIN_20210327_15_45_31_Pro.mp4'))


emotion()
