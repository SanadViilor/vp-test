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
    # predict
    output = model.predict(input)
    # rescale prediction

    return (int(output[0, 0]*960+160), int(output[0, 1]*960))


class Recorder:
    def __init__(self, resize_width=300, resize_height=300):
        self.cam = Camera()

        with Camera() as cam:  # Azért kell, hogy a színt be lehessen állítani
            if 'Bayer' in cam.PixelFormat:
                cam.PixelFormat = "RGB8"
            cam.start()

        self.cam.init()
        self.cam.start()
        self.frame = cv2.cvtColor(cv2.flip(self.cam.get_array(), 0), cv2.COLOR_BGR2RGB)
        self.frame_resized = []
        self.started = False
        self.read_lock = threading.Lock()
        self.resize_width = resize_width
        self.resize_height = resize_height

    def start(self):
        if self.started:
            print('[!] Asynchronous video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):

        while self.started:
            frame = cv2.cvtColor(cv2.flip(self.cam.get_array(), 0), cv2.COLOR_BGR2RGB)
            frame_cropped = frame[:, 160:160+960]
            with self.read_lock:
                self.frame = frame

                image = cv2.resize(frame_cropped, (self.resize_width, self.resize_height))

                image = image / 127.5
                image = image - 1.

                image = numpy.expand_dims(image, axis=0)

                self.frame_resized = image

    def read(self):
        with self.read_lock:
            #frame = self.frame.copy()
            frame_resized = self.frame_resized.copy()
        return frame_resized

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cam.stop()
        self.cam.close()





## PROCESSING VIDEO STREAM ########
if __name__ == '__main__':
    
    model = keras.models.load_model('best.hdf5')
    record = Recorder()
    record.start()
    

    while(True):
        frame = record.read()
        predicted = predict(frame, model)
        predicted = (int(output[0, 0]*960), int(output[0, 1]*960))
        cv2.circle(frame, predicted, 5, (0, 0, 255), -1)
        cv2.imshow('prediction', frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
    record.stop()
    record.__exit__()