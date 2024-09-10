import os
import pickle

import datetime
from deepface import DeepFace #type:ignore
import cv2
import cvzone      #type:ignore
import numpy as np

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-f37fe-default-rtdb.firebaseio.com/",
    'storageBucket':'faceattendancesystem-f37fe.appspot.com'
})

bucket = storage.bucket()

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

modeType = 0
counter = 0
id = -1
imgStudent = []

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
        # encodeCurFrame = [DeepFace.represent(face["face"], model_name='VGG-Face') for face in faces]
        encodeCurFrame = []

        for face in faces:
            if face["face"].size != 0:  # Ensure face data is valid
                try:
                    representation = DeepFace.represent(face["face"], model_name='VGG-Face', enforce_detection=False)
                    if representation:  # Check if the representation is not empty        #
                        encodeCurFrame.append(representation[0]["embedding"])
                except ValueError as e:
                    print(f"Error representing face: {e}")
                    continue  # Skip this face if there's an error

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                print("Type of encodeListKnown:", type(encodeListKnown))
                print("Sample item in encodeListKnown:", encodeListKnown[0])
                # Compare faces
                # faceDis = [np.linalg.norm(np.array(encodeFace) - np.array(enc)) for enc in encodeListKnown]
                # print(encodeListKnown[:2])
                # faceDis = [np.linalg.norm(np.array(encodeFace) - np.array(enc)) for enc in encodeListKnown]
                # Compute face distances
                faceDis = [np.linalg.norm(np.array(encodeFace) - np.array(enc['embedding'])) for enc in encodeListKnown]
                matchIndex = np.argmin(faceDis)
                print("Match Index", matchIndex)

                if faceDis[matchIndex] < 0.6:  # Threshold for a match
                    # Known face detected
                    y1, x2, y2, x1 = faceLoc['top'], faceLoc['right'], faceLoc['bottom'], faceLoc['left']
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]
                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275,400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(2)
                        counter = 1
                        modeType = 1
            if counter != 0:
                if counter == 1:
                    # Get the data
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)
                    # Get the image from the storage
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    # Update data of attendance
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                      "%Y-%m-%d %H:%M:%S")
                    secondElapsed = (datetime.now()-datetimeObject).total_seconds
                    print(secondElapsed)
                    if secondElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:

                    if 10<counter<20:
                        modeType = 2
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                    (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                    (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                    (100, 100, 100), 1)
                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414-w)//2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50))
                        imgBackground[175:175+216, 909:909+216] = imgStudent
                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0

    # Display the result
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
