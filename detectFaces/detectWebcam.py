import facerecogApi
import cv2
from takeref import takepicture


def detectStudent():
    # Take the reference picture to compare all along the exam.
    takepicture()

    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.

    # #################################################################
    # TO DO , FETCH une image du serveur au lieux de celles en local###
    # #################################################################
    test_image = facerecogApi.load_image_file("faces/etudiant.png")

    test_face_encoding = facerecogApi.face_encodings(test_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        test_face_encoding
    ]

    known_face_names = [
        "etudiant"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    warning_disapear = 0
    warning_unknown = 0
    while True:
        # Grab a single frame of video
        _, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        # Resize frame of video to 1/4 size for faster recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color
        # (which facerecog uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = facerecogApi.face_locations(rgb_small_frame)
        face_encodings = facerecogApi.face_encodings(
            rgb_small_frame, face_locations)

        # if not face_locations:
        #     warning_disapear += 1

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = facerecogApi.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"
            # If a match was found in known_face_encodings,
            # just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

        print(face_names)
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
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations,
                                                    face_names):
            # Scale back up face locations since the frame we detected in was
            # scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        cv2.waitKey(200)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == 27:
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return
