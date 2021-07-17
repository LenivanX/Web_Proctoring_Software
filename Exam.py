from tkinter import Tk, Label, Entry, Button, messagebox
import cv2
import face_recognition
from PIL import Image, ImageTk


def login_data():
    d = {}
    with open('login_data/login_data.csv', 'r') as f:
        lines = f.readlines()
        for data in lines:
            name, roll, password = data.split(',')
            if password[-1] == '\n':
                password = password[:-1]
            d[roll] = [name, password]
    return d


# data of login credentials
data_dict = login_data()


class Login:
    def __init__(self):
        # local variables
        label_width = 30
        text_width = 30
        base_pos_x = 20
        base_pos_y = 20

        # main root
        self.root = Tk()
        self.root.geometry('500x500')
        self.root.title('Login')
        self.root.resizable(False, False)
        # self.root.attributes('-fullscreen', True)
        self.root.lift()

        # labels
        self.label_head = Label(self.root, text='LOGIN', width=label_width, anchor='w')
        self.label_name = Label(self.root, text='Name', width=label_width, anchor='w')
        self.label_roll = Label(self.root, text='Roll', width=label_width, anchor='w')
        self.label_password = Label(self.root, text='Password', width=label_width, anchor='w')

        # entries
        self.entry_name = Entry(self.root, text='', width=text_width)
        self.entry_roll = Entry(self.root, text='', width=text_width)
        self.entry_password = Entry(self.root, text='', width=text_width)

        # buttons
        self.button_login = Button(self.root, text='Login', width=10, command=self.validate_login)

        # place widgets
        self.label_head.place(x=base_pos_x, y=base_pos_y)
        self.label_name.place(x=base_pos_x, y=base_pos_y + 40)
        self.label_roll.place(x=base_pos_x, y=base_pos_y + 70)
        self.label_password.place(x=base_pos_x, y=base_pos_y + 100)

        self.entry_name.place(x=base_pos_x + 100, y=base_pos_y + 40)
        self.entry_roll.place(x=base_pos_x + 100, y=base_pos_y + 70)
        self.entry_password.place(x=base_pos_x + 100, y=base_pos_y + 100)

        self.button_login.place(x=base_pos_x, y=base_pos_y + 150)

        # mainloop
        self.root.mainloop()

    def validate_login(self):
        global data_dict
        name = self.entry_name.get()
        roll = self.entry_roll.get()
        password = self.entry_password.get()

        if roll in data_dict:
            if data_dict[roll][0] == name and data_dict[roll][1] == password:
                self.root.destroy()
                waitWindow(roll)
        else:
            messagebox.showinfo('Error!', 'Invalid Credentials')


class WaitWindow:
    def __init__(self, roll):
        self.roll = roll
        self.timer = 0

        # main root
        self.root = Tk()
        self.root.geometry('500x500')
        self.root.title('Wait')
        self.root.resizable(False, False)
        # self.root.attributes('-fullscreen', True)

        # buttons
        self.button_checkcam = Button(self.root, text='Check Webcam', width=30, command=self.check_cam)

        # place widgets
        self.button_checkcam.place(x=50, y=50)

        # mainloop
        self.root.mainloop()

    def check_cam(self):
        # label
        self.label_cam = Label(self.root, text='webcam', width=400, height=350)
        self.label_cam.place(x=50, y=75)

        # load the image
        img = face_recognition.load_image_file(f'images/{self.roll}.jpg')
        face_profile = face_recognition.face_encodings(img)[0]

        # checking face in camera
        capture = cv2.VideoCapture(0)
        while capture.isOpened():
            ret, frame = capture.read()
            self.face_check(frame, face_profile)
            if ret:
                img_label = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_label = cv2.resize(img_label, (400, 350), interpolation=cv2.INTER_AREA)
                img_label = ImageTk.PhotoImage(Image.fromarray(img_label))

                self.label_cam['image'] = img_label
                self.root.update()
        capture.release()

    def face_check(self, frame, face_profile):
        frame = cv2.resize(frame, (200, 200))
        faces = face_recognition.face_locations(frame)
        if len(faces) != 1:
            return
        face_cam = face_recognition.face_encodings(frame)[0]
        result = face_recognition.compare_faces([face_profile], face_cam)

        if result[0]:
            self.timer += 1
            if self.timer > 10:
                messagebox.showinfo('Success!', 'Webcam Check Completed!')
                self.root.destroy()
                exam_window()
        else:
            self.timer = 0


class ExamWindow:
    def __init__(self):
        self.warnings = 0
        self.warn_timer = 0
        self.msg = ''

        # main root
        self.root = Tk()
        self.root.geometry('500x500')
        self.root.title('Exam')
        self.root.resizable(False, False)

        # labels
        self.label_exam_started = Label(self.root, text='Exam started')
        self.label_exam_started.place(x=20, y=20)

        self.label_total_warnings = Label(self.root, text='Warnings left: 3', anchor='w')
        self.label_total_warnings.place(x=20, y=40)

        self.label_warn = Label(self.root, text='', width=100, fg='red', anchor='w')
        self.label_warn.place(x=20, y=60)

        self.label_webcam = Label(self.root, text='Webcam')
        self.label_webcam.place(x=20, y=80)

        self.label_question = Label(self.root, text='Question', width=100, height=50, anchor='w')
        self.label_question.place(x=20, y=200)

        # function call
        self.face_cap()

        # mainloop
        self.root.mainloop()

    def face_recog(self, img):
        img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_AREA)
        faces = face_recognition.face_locations(img)
        return len(faces)

    def face_cap(self):

        capture = cv2.VideoCapture(0)
        while capture.isOpened():
            ret, frame = capture.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                faces = self.face_recog(frame)

                if faces != 1:
                    self.warn_timer += 1
                    if faces < 1:
                        self.msg = 'No Face Visible!'
                    elif faces > 1:
                        self.msg = 'More than 1 face Visible!'
                else:
                    self.label_warn['text'] = ''
                    self.warn_timer = 0

                if self.warn_timer > 60:
                    self.warnings += 1
                    self.warn_timer = 0

                    if self.warnings <= 3:
                        self.label_warn['text'] = 'Warning! ' + self.msg
                        self.label_total_warnings['text'] = 'Warnings left:' + str(3 - self.warnings)
                    else:
                        messagebox.showinfo('Too Many Warnings!', 'exam cancelled!!')
                        self.root.destroy()

                img = cv2.resize(img, (160, 100), interpolation=cv2.INTER_AREA)
                img = ImageTk.PhotoImage(Image.fromarray(img))
                self.label_webcam['image'] = img
                self.root.update()
            else:
                messagebox.showinfo('Webcam Error!', 'webcam not working!')
                self.root.destroy()
        capture.release()


def exam_window():
    ExamWindow()


def waitWindow(roll):
    WaitWindow(roll)


def app():
    Login()


app()
