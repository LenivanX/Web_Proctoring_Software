from tkinter import *
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import face_recognition

# main root
root1 = Tk()
root1.title('Exam Login')
root1.geometry('500x500')
root1.resizable(False, False)


# functions
def face_recog(img):
    img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_AREA)
    faces = face_recognition.face_locations(img)
    return len(faces)


def exam(root2):
    warnings = 0
    warn_timer = 0
    msg = ''

    # labels
    label_exam_started = Label(root2, text='Exam started')
    label_exam_started.place(x=20, y=20)

    label_total_warnings = Label(root2, text='Warnings left: 3', anchor='w')
    label_total_warnings.place(x=20, y=40)

    label_warn = Label(root2, text='', width=100, fg='red', anchor='w')
    label_warn.place(x=20, y=60)

    label_webcam = Label(root2, text='Webcam')
    label_webcam.place(x=20, y=80)

    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            faces = face_recog(frame)

            if faces != 1:
                warn_timer += 1
                if faces < 1:
                    msg = 'No Face Visible!'
                elif faces > 1:
                    msg = 'More than 1 face Visible!'
            else:
                label_warn['text'] = ''
                warn_timer = 0

            if warn_timer > 60:
                warnings += 1
                warn_timer = 0

                if warnings <= 3:
                    label_warn['text'] = 'Warning! ' + msg
                    label_total_warnings['text'] = 'Warnings left:' + str(3 - warnings)
                else:
                    messagebox.showinfo('Too Many Warnings!', 'exam cancelled!!')
                    root2.destroy()

            img = cv2.resize(img, (160, 100), interpolation=cv2.INTER_AREA)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            label_webcam['image'] = img
            root2.update()
        else:
            messagebox.showinfo('Webcam Error!', 'webcam not working!')
            root2.destroy()


def exam_portal():
    # branched root
    root2 = Tk()
    root2.geometry('500x500')
    root2.title('Exam')
    root2.resizable(False, False)

    # functions
    def button_click():
        button_start.destroy()
        exam(root2)

    # buttons
    button_start = Button(root2, text='Start Exam', width=20, command=button_click)
    button_start.place(x=20, y=20)

    root2.mainloop()


def login():
    wrong_detail = True
    wrong_pass = True
    name = entry_name.get()
    roll = entry_roll.get()
    pasw = entry_pass.get()
    with open('login_data/login_data.csv', 'r') as f:
        data = f.readlines()
        for line in data:
            g_name, g_roll, g_pass = line.split(',')
            if name.upper() == g_name.upper() and roll == g_roll:
                wrong_detail = False
                if g_pass[-1] == '\n':
                    g_pass = g_pass[:-1]
                if pasw == g_pass:
                    wrong_pass = False
                    break
    if wrong_detail:
        messagebox.showinfo('Error!', 'Invalid Name/Roll')
    elif wrong_pass:
        messagebox.showinfo('Error!', 'Wrong Password')
        return
    else:
        root1.destroy()
        exam_portal()


# labels
label_title = Label(root1, text='Enter LOGIN Details')
label_title.place(x=20, y=20)
label_name = Label(root1, text='Name')
label_name.place(x=20, y=50)
label_roll = Label(root1, text='Roll')
label_roll.place(x=20, y=80)
label_pass = Label(root1, text='Password')
label_pass.place(x=20, y=110)

# entries
entry_name = Entry(root1, text='', width=50)
entry_name.place(x=100, y=50)
entry_roll = Entry(root1, text='', width=50)
entry_roll.place(x=100, y=80)
entry_pass = Entry(root1, text='', width=50)
entry_pass.place(x=100, y=110)

# buttons
button_login = Button(root1, text='Login', width=20, command=login)
button_login.place(x=20, y=140)

root1.mainloop()
