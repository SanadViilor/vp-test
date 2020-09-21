from tensorflow import keras
import cv2
import numpy
import concurrent.futures
import threading
from simple_pyspin import Camera
from keras.applications import imagenet_utils

## PREDICTION ###############

def predict(param, model):
    # crop param to 960*960
    cropped = param[:, 160:160+960]
    input = cv2.resize(cropped, (300, 300))
    input = numpy.expand_dims(input, axis=0)
    input = imagenet_utils.preprocess_input(input, mode='tf')
    output = model.predict(input)
    # rescale prediction

    return (int(output[0, 0]*960+160), int(output[0, 1]*960))




## PROCESSING VIDEO STREAM ########
if __name__ == '__main__':
    
    model = keras.models.load_model('best.hdf5')
    
    camera = Camera()
    camera.init()
    if 'Bayer' in camera.PixelFormat:
        camera.PixelFormat = "RGB8"
    camera.start()

    while(True):
        frame = camera.get_array()
        frame = cv2.cvtColor(cv2.flip(frame, -1), cv2.COLOR_BGR2RGB)
        predicted = predict(frame, model)
        cv2.circle(frame, predicted, 5, (0, 0, 255), -1)
        cv2.imshow('prediction', frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    camera.stop()
    camera.release()
