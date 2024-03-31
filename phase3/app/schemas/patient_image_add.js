db.patient.updateOne(
    { "id": "Ashish-Singh-114417841941" },
    {
        $push: {
            images: {
                "image_link": "new_image_link4",
                "doctor_comment": "Your doctor's comment here 4",
                "response_from_model": "None"
            }
        }
    }
)