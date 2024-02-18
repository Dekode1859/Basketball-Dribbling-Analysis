import cv2
import numpy as np

class KalmanFilter:
    kf = cv2.KalmanFilter(4,2)
    kf.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
    kf.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
    
    def predict(self, xcord, ycord):
        measured = np.array([[np.float32(xcord)],[np.float32(ycord)]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        x, y = predicted[0], predicted[1]
        return x, y