db.patient.insertOne(
    {
        "first_name": "Ashish",
        "last_name": "Singh",
        "birth_date": "2003-11-17",
        "address":"Ghatkopar Mumbai 75",
        "last_visit_date": "2023-09-12",
        "mobile_number":"1234567890",
        "email_id":"email1@gmail.com",
        "medical_history":{
            "allergies":[
                "allergy1","allergy2","allergy3"
            ],
            "surgeries":[
                {
                    "surgery_name":"endoscopy",
                    "surgery_date":"2013-09-12"
                },
                {
                    "surgery_name":"Cataract",
                    "surgery_date":"2016-04-19"
                },
                {
                    "surgery_name":"Heart bypass",
                    "surgery_date":"2019-07-13"
                }
            ],
            "medication":[
                {
                    "medicine_name":"Crocin",
                    "medicine_reason":"Frequent headache",
                    "is_lifetime":"No",
                    "medicine_frequency":"Once Every night"
                },
                {
                    "medicine_name":"Calciferol",
                    "medicine_reason":"Vitamin D deficiency",
                    "is_lifetime":"Yes",
                    "medicine_frequency":"Twice Every day"
                },
                {
                    "medicine_name":"Bonfeit K2-7",
                    "medicine_reason":"Calcium deficiency",
                    "is_lifetime":"Yes",
                    "medicine_frequency":"Thrice Every day"
                }
            ]
            
        },
        "images": [
            {
                "image_link": "image_link1",
                "doctor_comment": "No problem, everything fine",
                "response_from_model": "None"
            },
            {
                "image_link": "image_link2",
                "doctor_comment": "Left part of image depicts XYZ issue",
                "response_from_model": "None"
            },
            {
                "image_link": "image_link3",
                "doctor_comment": "No problem, everything fine",
                "response_from_model": "None"
            }
        ],
        "blood_group": "A+",
        "gender":"male"
    }
)


// old examples for old schema:

db.patient.insertOne(
    {
        "id": 1000,
        "name": "Ashish Singh",
        "age": 34,
        "images": [
            {
                "image_link": "link1",
                "doctor_view": "No problem, everything fine",
                "response_from_model": "None"
            }
        ],
        "blood_group": "A+"
    }
)

db.patient.insertOne(
    {
        "id": 1001,
        "name": "Arnab Shah",
        "age": 39,
        "images": [
            {
                "image_link": "link2",
                "doctor_view": "No problem, everything fine",
                "response_from_model": "None"
            }
        ],
        "blood_group": "A-"
    }
)


db.patient.insertOne(
    {
        "id": 1002,
        "name": "Rajweer Shah",
        "age": 49,
        "images": [
            {
                "image_link": "link3",
                "doctor_view": "No problem, everything fine",
                "response_from_model": "None"
            }
        ],
        "blood_group": "O+"
    }
)
db.patient.deleteOne( { "age": 39 } )

db.patient.find({_id : ObjectId('65e788fb85a25cbaa653e2fb')});

