import cv2
import facerecogApi
import takeref


def detectStudent():
    """ Prend une photo de référence de l'élève et le traque.
        Soulève des alertes lorsqu'il disparait de l'écran ou que ce n'est
        pas la bonne personne
    """
    takeref.takepicture()
    video_capture = cv2.VideoCapture(0)
    # TODO , FETCH une image du serveur au lieux de celles en local
    # TODO remplacer le nom étudiant par celui de l'élève
    # TODO envoyer des alerte aux serveur
    test_image = facerecogApi.load_image_file(
        "./faces/etudiant.png")
    test_face_encoding = facerecogApi.face_encodings(test_image)[0]
    known_face_encodings = [test_face_encoding]
    known_face_names = ["etudiant"]
    face_locations = []
    face_encodings = []
    face_landmarks = []
    face_names = []
    warning_disapear = 0
    warning_unknown = 0
    # font = cv2.FONT_HERSHEY_DUPLEX
    while True:
        _, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        visage = frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = facerecogApi.face_locations(small_frame)
        face_names = []
        if face_locations:
            face_encodings = facerecogApi.face_encodings(small_frame,
                                                         face_locations)
            face_landmarks = facerecogApi.face_landmarks(small_frame,
                                                         face_locations)
            for list_pos in face_landmarks[0].values():
                for x, y in list_pos:
                    cv2.circle(small_frame, (x, y), 1, (0, 0, 255), -1)

            cv2.imshow('Visage', small_frame)
            for face_encoding in face_encodings:
                name = "Unknown"
                matches = facerecogApi.compare_faces(known_face_encodings,
                                                     face_encoding)
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                visage = frame[top:bottom, left:right]

                # cv2.rectangle(frame, (left, bottom - 35),
                #               (right, bottom), (0, 0, 255), cv2.FILLED)
                # cv2.putText(frame, name, (left + 6, bottom - 6),
                #             font, 1.0, (255, 255, 255), 1)
            # print(face_landmarks[0].values())

        #cv2.imshow('Video', frame)
        # cv2.waitKey(200)
        print("Face name :", face_names)
        if "etudiant" not in face_names:
            warning_disapear += 1
        else:
            warning_disapear = 0

        if "Unknown" in face_names:
            warning_unknown += 1

        if face_names == ["etudiant"]:
            warning_unknown = 0

        if warning_disapear > 50:
            print("L'élève à disparu !")
        if warning_unknown > 50:
            print("Visage inconnu !")
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == 27:
            break
    video_capture.release()
    cv2.destroyAllWindows()


detectStudent()
