#Import the libraries needed
import cv2
import numpy as np
from tensorflow.keras.models import load_model
#Load the pretrained model
model=load_model("adam_model2.h5")
#Open the webcam
cap=cv2.VideoCapture(0)
#Load the haar cascade model to detect faces
faces_to_detect=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#Label for the emotions
emotions={0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}
#Start video processing; infinite loop
while True:
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Grayscale is needed for Haar Cascade
    faces=faces_to_detect.detectMultiScale(gray, 1.1, 5) #Detects multiple faces
    #Iterate over detected faces, extract, preprocess, predict, display emotion
    for x, y, w, h in faces:
        sub_face_img=gray[y:y + h, x:x + w]
        resized=cv2.resize(sub_face_img, (48, 48))
        normalize=resized/255.0
        reshaped=np.reshape(normalize, (1, 48, 48,1))
        result=model.predict(reshaped)
        label=np.argmax(result, axis=1)[0]
        print(label)
        #Add a bounding box and the emotion detected on the image
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame,emotions[label],(x,y -10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2,cv2.LINE_AA)
        # Display the resulting frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()