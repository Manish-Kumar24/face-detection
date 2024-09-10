import os
import pickle
import cv2
import cvzone  # type:ignore
import numpy as np
from deepface import DeepFace  # type:ignore

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load background image
imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Load the encoding file
print("Loading Encode File ...")
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded ...")

# Load the Haarcascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    gray = cv2.cvtColor(imgS, cv2.COLOR_BGR2GRAY)

    # Detect faces using Haarcascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    for (x, y, w, h) in faces:
        face = imgS[y:y + h, x:x + w]
        faceRGB = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        # Represent the detected face
        try:
            encodeCurFrame = DeepFace.represent(faceRGB, model_name='VGG-Face', enforce_detection=False)
            current_vector = np.array(encodeCurFrame[0]["embedding"])
        except ValueError as e:
            print(f"Error representing face: {e}")
            continue

        # Compare faces
        faceDis = [np.linalg.norm(current_vector - np.array(enc[0]["embedding"])) for enc in encodeListKnown]
        matchIndex = np.argmin(faceDis)
        # print("Match Index", matchIndex)
        # Print the corresponding student name or ID
        print("Recognized:", studentIds[matchIndex])

        if faceDis[matchIndex] < 0.6:  # Threshold for a match
            # Known face detected
            x1, y1, x2, y2 = x * 4, y * 4, (x + w) * 4, (y + h) * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

    # Display the result
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
