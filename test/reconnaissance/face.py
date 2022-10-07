import numpy as np
import cv2
import pickle
import subprocess

class Detection:
    def __init__(self):
        self.color = (0,0,0)
        self.importation()
        self.ft_labels()
        self.cap = cv2.VideoCapture(0)
        self.run()
        self.cap.release()
        cv2.destroyAllWindows()


    def importation(self):
        self.face_cascade = cv2.CascadeClassifier('assets/xml/haarcascade_frontalface_alt2.xml')
        self.eye_cascade = cv2.CascadeClassifier('assets/xml/haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier('assets/xml/haarcascade_smile.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("assets/face-trainner.yml")

    def ft_labels(self):
        self.labels = {"person_name": 1}
        with open("assets/other/face-labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            self.labels = {v:k for k,v in og_labels.items()}

    def predict(self):
        id_, conf = self.recognizer.predict(self.roi_gray)
        if conf>=4 and conf <= 85:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = self.labels[id_]
            stroke = 2
            cv2.putText(self.frame, name, (self.x,self.y), font, 1, self.color, stroke, cv2.LINE_AA)

    def drawRect(self):
        stroke = 2
        end_cord_x = self.x + self.w
        end_cord_y = self.y + self.h
        cv2.rectangle(self.frame, (self.x, self.y), (end_cord_x, end_cord_y), self.color, stroke)

    def run(self):

        while 42:
            ret, self.frame = self.cap.read() # capture camera
            gray  = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            for (self.x, self.y, self.w, self.h) in faces:
                self.roi_gray = gray[self.y:self.y+self.h, self.x:self.x+self.w]
                self.roi_color = self.frame[self.y:self.y+self.h, self.x:self.x+self.w]
                img_item = "assets/img/victor/1.png"
                cv2.imwrite(img_item, self.roi_color)

                self.predict()
                self.drawRect()


            cv2.imshow('frame',self.frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

subprocess.run("py face_train.py", shell=True, check=True)
Detection()

