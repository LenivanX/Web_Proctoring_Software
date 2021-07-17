from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition

clicked = False
encode_face = None


def take_snap(frame):
    global encode_face
    cv2.imshow('snap', frame)
    encode = face_recognition.face_encodings(frame)
    encode_face = encode


def click():
    global clicked
    clicked = not clicked


def match_face(frame):
    global encode_face
    warn_timer = 0

    img = cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA)
    encode = face_recognition.face_encodings(img)[0]
    match = face_recognition.compare_faces([encode_face], encode)
    print(match)
    if not match:
        warn_timer += 1
        if warn_timer > 30:
            messagebox.showinfo('Error!', 'FaceError!')
            root.destroy()
            return False
    return True


def vid_cap():
    global clicked
    global encode_face
    warn_timer = 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        faces = face_recognition.face_locations(frame)

        if len(faces) != 1:
            warn_timer += 1
            if warn_timer > 30:
                messagebox.showinfo('Error!', 'Face Not Found!')
                return False
        else:
            warn_timer = 0

        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (450, 350), interpolation=cv2.INTER_AREA)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            label_webcam['image'] = img
            root.update()

        if clicked:
            if warn_timer == 0:
                take_snap(frame)
                click()
            else:
                messagebox.showinfo('Error!', 'FaceError!')
                click()

        if encode_face is not None:
            if not match_face(frame):
                return False


root = Tk()
root.geometry('600x600')
root.title('Snap')

label_webcam = Label(root, text='webcam', width=450, height=350)
label_webcam.place(x=10, y=10)

button_snap = Button(root, text='Snap', width=10, height=2, command=click)
button_snap.place(x=10, y=400)

if not vid_cap():
    root.destroy()
root.mainloop()
