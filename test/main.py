########################################
#Victor Dalet
#labo ia project
########################################

import cv2
import tello

class Facedetector:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.WHITE = (255, 255, 255)
        self.KNOWN_DISTANCE = 20  # centimeter
        self.KNOWN_WIDTH = 18  # centimeter
        self.fonts = cv2.FONT_HERSHEY_COMPLEX
        self.drone = Drone()
        self.run()

    def focal_length(self):
        self.focal_length_found = (self.ref_image_face_width * self.KNOWN_DISTANCE) / self.KNOWN_WIDTH

    def distance_finder(self):
        self.distance = (self.KNOWN_WIDTH * self.focal_length_found) / self.face_width_in_frame

    def face_data(self,image):
        face_width = 0
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray_image, 1.3, 5)
        for (x, y, h, w) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), self.WHITE, 1)
            face_width = w
        return face_width

    def initialization(self):
        self.ref_image = cv2.imread("Ref_image.png")
        self.ref_image_face_width = self.face_data(self.ref_image)
        self.focal_length()

    def run(self):

        self.initialization()

        self.cap = cv2.VideoCapture(0)
        while 42:
            _, self.frame = self.cap.read()
            self.face_width_in_frame = self.face_data(self.frame)
            if self.face_width_in_frame != 0:
                self.distance_finder()
                self.drone.follow()
                cv2.putText(
                    self.frame, f"Distance = {round(self.distance, 2)} CM", (50, 50), self.fonts, 1, (self.WHITE), 2
                )
            else:
                print("")
                self.drone.rotate()

            cv2.imshow("frame", self.frame)
            if cv2.waitKey(1)==ord("q"):
                break
        self.cap.release()
        cv2.destroyAllWindows()


class Drone:
    def __init__(self):
        self.distance_max = 60
        self.speed = 1
        self.drone = tello.Tello()
        self.drone.takeoff() #décolage
        #self.drone.land() #attérissage

    def follow(self):
        if self.distance > self.distance_max:
            self.drone.forward(self.speed)
        elif self.distance < self.distance_max:
            self.drone.backward(self.speed)
    
    def rotate(self):
            self.drone.rotate("r",self.speed)

Facedetector()