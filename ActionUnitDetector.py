import torch
from feat import Detector
import numpy as np

# class to detect action units of a face in an image 
class ActionUnitDetector():
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.detector = Detector(device=self.device)
        self.aus = ["AU01", "AU02", "AU04", "AU05", "AU06", "AU07", "AU09", "AU10", "AU11", "AU12", "AU14", "AU15", "AU17",
               "AU20", "AU23", "AU24", "AU25", "AU26", "AU28", "AU43"]
    def detectAUImage(self, image):
        detected_faces = self.detector.detect_faces(image)
        detected_landmarks = self.detector.detect_landmarks(image, detected_faces)
        prediction = np.asarray(self.detector.detect_aus(image, detected_landmarks))
        return prediction[0], detected_faces

    def detectAUImagesPath(self, imagePaths):
        prediction = self.detector.detect_image(imagePaths, batch_size=1)
        return prediction[self.aus].to_numpy(dtype=np.float32)
