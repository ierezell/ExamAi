import cv2


def takepicture():
    """
    Ask for the user to put his head straight in a square with eyes visible
    Returns :
    -------
    Nothing, write the reference image in a folder.

    Arguments :
    -------
    None

    Raises :
    -------
    Exeptions related to OpenCV. Only basic functions

    Examples :
    -------
    >>> takepicture()

    """
    frame = cv2.VideoCapture(0)
    frame.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    frame.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    face_cascade = cv2.CascadeClassifier(
        './models/haarcascade_frontalface_default.xml')
    print("face cascade : ", face_cascade.empty())
    eye_cascade = cv2.CascadeClassifier(
        './models/haarcascade_eye.xml')

    target = [200, 130, 450, 400]
    phototaken = False
    while not phototaken:
        _, img = frame.read()
        img = cv2.flip(img, 1)
        pic = img.copy()
        cv2.rectangle(img, (target[0], target[1]),
                      (target[2], target[3]), (0, 0, 255), 6)

        cv2.putText(img, 'Alignez votre tete au carre rouge', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

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
                # If the head is in the target and we can see both eyes
            if (pos[0] > target[0] and pos[1] > target[1] and
                    pos[2] < target[2] and pos[3] < target[3] and
                    len(eyes) == 2):
                cv2.imwrite("./faces/etudiant.png", pic)
                phototaken = True

        cv2.imshow('Photo reference', img)
        cv2.waitKey(100)

    cv2.destroyAllWindows()
    return
