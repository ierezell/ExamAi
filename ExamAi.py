import os
import sys
sys.path.append(os.path.abspath(__file__))
sys.path.append(os.path.abspath(__file__) + '/detectFaces/')
sys.path.append(os.path.abspath(__file__) + '/detectSound/')
sys.path.append(os.path.abspath(__file__) + '/Api/')

from detectFaces import detectWebcam, takeref
from Api import facerecog, models
import cv2
import pyaudio

if __name__ == "__main__":
    detectWebcam.detectStudent()
