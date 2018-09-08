
import sys
import dlib
import cv2

detector = dlib.get_frontal_face_detector()
cam = cv2.VideoCapture(0)
color_green = (0, 255, 0)
line_width = 3
while True:
    ret_val, img = cam.read()
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = detector(rgb_image)
    for det in dets:
        cv2.rectangle(img, (det.left(), det.top()),
                      (det.right(), det.bottom()), color_green, line_width)
    cv2.imshow('my webcam', img)
    if cv2.waitKey(1) == 27:
        break  # esc to quit
cv2.destroyAllWindows()
