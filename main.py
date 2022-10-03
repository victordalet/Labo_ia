########################################
#Victor Dalet
#labo ia project
########################################

import cv2

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
WHITE = (255, 255, 255)
KNOWN_DISTANCE = 20  # centimeter
KNOWN_WIDTH = 18  # centimeter
fonts = cv2.FONT_HERSHEY_COMPLEX

def focal_length(measured_distance, real_width, width_in_rf_image):
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value

def distance_finder(focal_length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance

def face_data(image):
    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
        face_width = w

    return face_width

def main():

    ref_image = cv2.imread("Ref_image.png")
    ref_image_face_width = face_data(ref_image)
    focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, ref_image_face_width)


    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        face_width_in_frame = face_data(frame)
        if face_width_in_frame != 0:
            print(focal_length_found)
            Distance = distance_finder(focal_length_found, KNOWN_WIDTH, face_width_in_frame)
            print(Distance)
            cv2.putText(
                frame, f"Distance = {round(Distance, 2)} CM", (50, 50), fonts, 1, (WHITE), 2
            )

        cv2.imshow("frame", frame)
        if cv2.waitKey(1)==ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

main()