#Import the libraries needed
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings("ignore")
#Load the pretrained model
model=load_model("adam_model2.h5")
#Load the haar cascade model to detect faces
faces_to_detect=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#Label for the emotions
emotions={0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}
#Read the input images
cap=cv2.imread(r" ")
#Convert to grayscale; model was trained on grayscale images
gray=cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
faces=faces_to_detect.detectMultiScale(gray, 1.1, 5)
#Loop for the faces
for x,y,w,h in faces:
        sub_face_img=gray[y:y + h, x:x + w] #Extract and crop the face using its bounding box
        resized=cv2.resize(sub_face_img, (48, 48)) #Match the input size expected by the CNN model
        normalize=resized/255.0 #Stabilize gradients
        reshaped=np.reshape(normalize, (1, 48, 48,1)) #Reshape the images to match the input shape of CNN
        result=model.predict(reshaped) #Pass face to model for emotion prediction
        label=np.argmax(result, axis=1)[0] #Find the emotion with the highest probability
        print(emotions[label])
        #Add a bounding box and the emotion detected on the image
        cv2.rectangle(cap,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(cap,emotions[label],(x,y -10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2,cv2.LINE_AA)
#Display the image on a new window       
cv2.imshow('Emotion Recognition', cap)
#print("Detected faces:", faces)
cv2.waitKey(0)
cv2.destroyAllWindows()