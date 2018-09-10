import dlib
import cv2


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# cap.set(cv2.CAP_PROP_FPS, 10)

face_cascade = cv2.CascadeClassifier(
    '/home/pedrok/Programmes/anaconda3/envs/Master/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    '/home/pedrok/Programmes/anaconda3/envs/Master/share/OpenCV/haarcascades/haarcascade_eye.xml')

color_green = (0, 255, 0)
color_red = (0, 0, 255)
color_white = (255, 255, 255)
line_width = 3
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftText = (10, 50)
fontScale = 1
mire = [200, 130, 450, 400]
photo = True
while photo:
    _, img = cap.read()
    pic = img
    cv2.rectangle(img, (mire[0], mire[1]),
                  (mire[2], mire[3]), color_red, line_width * 2)

    cv2.putText(img, 'Alignez votre tete au carre rouge', bottomLeftText,
                font, fontScale, color_white, line_width)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        pos = [x, y, x + w, y + h]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for nb_eyes, (ex, ey, ew, eh) in enumerate(eyes):
            cv2.rectangle(roi_color, (ex, ey),
                          (ex + ew, ey + eh), (0, 255, 0), 2)

            if (pos[0] > mire[0] and pos[1] > mire[1] and pos[2] < mire[2]
                    and pos[3] < mire[3] and nb_eyes == 1):

                cv2.imwrite("test.png", pic)
                photo = False
    cv2.imshow('my webcam', img)
    key = cv2.waitKey(100)

cv2.destroyAllWindows()
