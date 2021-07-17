import cv2
import face_recognition

img = face_recognition.load_image_file('images/1001.jpg')
face = face_recognition.face_locations(img)[0]
enc = face_recognition.face_encodings(img)[0]

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        img1 = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        face1 = face_recognition.face_locations(img1)[0]
        enc1 = face_recognition.face_encodings(img1)[0]
        cv2.rectangle(frame, (face1[3] * 2, face1[0] * 2), (face1[1] * 2, face1[2] * 2), (0, 0, 255), 2)
        cv2.imshow('', frame)
        cv2.waitKey(1)
        print(face_recognition.compare_faces([enc], enc))
