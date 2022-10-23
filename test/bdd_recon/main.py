import face_recognition
import cv2
import numpy as np
import json
import data


class Face:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.color = (0, 0, 0)
        self.color_txt = (255,255,255)
        self.known_face_names = data.Data("data/name.json").get_data()
        self.abscent_face_names = data.Data("data/name.json").get_data()
        self.known_face_encodings = []
        print("Training...")
        for i in self.known_face_names:
            self.known_face_encodings.append(self.load('student/'+i+'.jpg'))
        print("Successful completion of training.")
        print("Launch...")
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.run()
        self.video_capture.release()
        cv2.destroyAllWindows()
        print("Bye")


    def load(self,url):
        image = face_recognition.load_image_file(url)
        return face_recognition.face_encodings(image)[0]


    def test(self): 
        face_names = []
        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            self.name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                self.name = self.known_face_names[best_match_index]
                print(self.known_face_names[best_match_index])
                try : 
                    self.abscent_face_names.remove(self.name) 
                except : pass
            else : print("Unknown")
            self.face_names.append(self.name)
            


    def draw(self):
        for (top, right, bottom, left), self.name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(self.frame, (left, top), (right, bottom), self.color, 2)
            cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), self.color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame, self.name, (left + 6, bottom - 6), font, 1.0, self.color_txt, 1) 

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
            cv2.imshow('Video', self.frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break






def main():
    """data_img = data.Data("data/img.json")
    data_name = data.Data("data/name.json")
    data_name.give_data(Face().load("student/macron.jpg")[1])
    np.savetxt('student/'+Face().load("student/macron.jpg")[1] + '.txt',Face().load("student/macron.jpg")[0])"""
    
    Face()

main()