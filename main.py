import os
import pickle
from deepface import DeepFace
import cv2
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

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

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgRGB = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    try:
        # Extract faces without enforce_detection
        faces = DeepFace.extract_faces(imgRGB, enforce_detection=False)
    except ValueError as e:
        print(f"Error extracting faces: {e}")
        faces = []

    if faces:
        faceCurFrame = [face["facial_area"] for face in faces]
        encodeCurFrame = [DeepFace.represent(face["face"], model_name='VGG-Face') for face in faces]

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            # Compare faces
            faceDis = [np.linalg.norm(np.array(encodeFace) - np.array(enc)) for enc in encodeListKnown]
            matchIndex = np.argmin(faceDis)
            print("Match Index", matchIndex)

            if faceDis[matchIndex] < 0.6:  # Threshold for a match
                # Known face detected
                y1, x2, y2, x1 = faceLoc['top'], faceLoc['right'], faceLoc['bottom'], faceLoc['left']
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

    # Display the result
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
