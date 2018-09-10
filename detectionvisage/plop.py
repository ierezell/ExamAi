import dlib
import cv2

detector = dlib.get_frontal_face_detector()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# cap.set(cv2.CAP_PROP_FPS, 10)

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

    dets = detector(img)
    for det in dets:
        pos = [det.left(), det.top(), det.right(), det.bottom()]
        cv2.rectangle(img, (det.left(), det.top()),
                      (det.right(), det.bottom()), color_green, line_width)

        print(pos[0], mire[0], pos[1], mire[1],
              pos[2], mire[2], pos[3], mire[3])
        if (pos[0] > mire[0] & pos[1] > mire[1]
                & pos[2] < mire[2] & pos[3] < mire[3]):
            cv2.imwrite("test.png", pic)
            photo = False

    cv2.imshow('my webcam', img)
    key = cv2.waitKey(100)

cv2.destroyAllWindows()
