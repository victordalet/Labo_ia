import face_recognition
import cv2
import numpy as np
import json
import data


class Face:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.color = (0, 0, 0)
        self.known_face_encodings = Data("img.json").get_data()
        self.known_face_names = Data("name.json").get_data()
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.run()
        self.video_capture.release()
        cv2.destroyAllWindows()

    def load(self,url):
        image = face_recognition.load_image_file(url)
        name = ""
        url = url.replace('student/','')
        for i in url:
            if i == ".":
                break
            name += i
        return face_recognition.face_encodings(image)[0] , name


    def test(self): 
        face_names = []
        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            self.face_names.append(name) 


    def draw(self):
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(self.frame, (left, top), (right, bottom), self.color, 2)
            cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame, name, (left + 6, bottom - 6), font, 1.0, self.color, 1) 

    def run(self):
        while 42:
            ret, self.frame = self.video_capture.read()
            if self.process_this_frame:
                small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.test()

            self.process_this_frame = not self.process_this_frame
            self.draw()
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




def main():
    data_img = Data("img.json")
    data_name = Data("name.json")
    data_img.give_data(Face().load("student/macron.jpg")[0])
    data_name.give_data(Face().load("student/macron.jpg")[1])
    Face().run()

main()