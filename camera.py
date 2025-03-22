import cv2
# load the haar classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # create a bounding box around detected face
    def get_frame(self):
        ret,frame=self.video.read()
        faces=face_cascade.detectMultiScale(frame,1.3, 5)
        for x,y, w, h in faces:
            x1,y1 = x + w, y + h
            cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        ret,jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()