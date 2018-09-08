import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('LiveWebcam', frame)
    if (cv2.waitKey(1) == ord('y')):
        nom = input("Nom de la photo ? :")
        nom = nom + ".png"
        cv2.imwrite(nom, frame)
    if (cv2.waitKey(1) == ord('q')) or (cv2.waitKey(1) == 27):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
