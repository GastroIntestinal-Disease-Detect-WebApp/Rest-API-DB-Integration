# chats is a list of chat
chat_collection = [
    { # let's call this Chat
    "chat_thread_id":"date_time_in-Milli_sec_6digitRandNumber",
    "chat_title":"title1",
    "participants":[
        "partid1",
        "partid2"
    ],
    "chats":[ # let's call this IndividualChat
        {
            "message":"Hey there, how are you doing",
            "from":"partid1",
            "to":"partid2",
            "date-time":"2024-1-25 13:26:01"
        },
        {
            "message":"Hi, I am doing good",
            "from":"partid2",
            "to":"partid1",
            "date-time":"2024-1-25 13:28:01"
        }

    ]
    },

    {
        "chat_thread_id":"2_date_time_in-Milli_sec_6digitRandNumber",
        "chat_title":"title2",
        "participants":[
            "partid3",
            "partid2"
        ],
        "chats":[
            {
                "message":"Yo !!",
                "from":"partid3",
                "to":"partid2",
                "date-time":"2024-1-25 13:26:01"
            },
            {
                "message":"Bye !!!",
                "from":"partid2",
                "to":"partid3",
                "date-time":"2024-1-25 13:28:01"
            }
    
        ]
    }

]

