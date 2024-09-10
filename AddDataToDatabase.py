import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-f37fe-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "22cs3038":
        {
            "name": "Manish Kumar",
            "major": "Robotics",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "22cs2018":
        {
            "name": "Amit Anand",
            "major": "Data Science",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "22cs3019":
        {
            "name": "Aviram Yadav",
            "major": "Developer",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "22cs3054":
        {
            "name": "Sanvi Shukla",
            "major": "NLP",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "22cs3057":
        {
            "name": "Shubhro Dev",
            "major": "DSA",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "22cs3074":
        {
            "name": "Harshit Negi",
            "major": "Developer",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "cs0001":
        {
            "name": "Dr. Akash Yadav",
            "major": "DSA",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "cs0002":
        {
            "name": "Dr. Gargi Srivastava",
            "major": "Developer",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "cs0003":
        {
            "name": "Dr. Kalka Dubey",
            "major": "Cloud Computing",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "cs0004":
        {
            "name": "Dr. Nirbhay Tagore",
            "major": "Facial Recognition",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "cs0005":
        {
            "name": "Dr. Pallabi Saikia",
            "major": "Computer Vision",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "cs0006":
        {
            "name": "Dr. Santosh Mishra",
            "major": "Deep Learning",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        },
    "cs0007":
        {
            "name": "Dr. Susham Biswas",
            "major": "Artificial Intelligence",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-08-19 18:40:00"
        }
}

for key, value in data.items():
    ref.child(key).set(value)