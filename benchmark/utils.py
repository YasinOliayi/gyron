import random


def make_message_update(user_id):
    return {
            "update_id": 3606,
            "message": {
                "message_id": 4884,
                "from": {
                    "id": user_id,
                    "is_bot": False,
                    "first_name": "",
                    "last_name": "",
                    "username": ""
                },
                "date": 1789109353,
                "chat": {
                    "id": 1291048737,
                    "type": "private",
                    "username": "",
                    "first_name": ""
                },
                "text": "b"
            }
            }


def make_callback_update(user_id):
    return {
    "update_id": 3609,
    "callback_query": {
        "id": "7317002386271990388",
        "from": {
            "id": user_id,
            "is_bot": False,
            "first_name": "",
            "last_name": "",
            "username": ""
        },
        "message": {
            "message_id": 4888,
            "from": {
                "id": random.randint(0, 1000000000),
                "is_bot": True,
                "first_name": "",
                "last_name": "",
                "username": ""
            },
            "date": 1789110390,
            "chat": {
                "id": 1291048737,
                "type": "",
                "username": "",
                "first_name": ""
            },
            "text": "تست inline keypad",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "دکمه 1",
                            "callback_data": "btn1"
                        }
                    ],
                    [
                        {
                            "text": "دکمه 2",
                            "callback_data": "btn2"
                        }
                    ]
                ]
            }
        },
        "chat_instance": "1291048737",
        "data": "btn2"
    }
}



def make_document_update(user_id):
    return {
    "update_id": 3610,
    "message": {
        "message_id": 4890,
        "from": {
            "id": user_id,
            "is_bot": False,
            "first_name": "",
            "last_name": "",
            "username": ""
        },
        "date": 1789110615,
        "chat": {
            "id": 1291048737,
            "type": "private",
            "username": "",
            "first_name": ""
        },
        "document": {
            "file_id": "12910437:-7067084671:f9e5eb2748c9ec",
            "file_unique_id": "",
            "file_name": "",
            "mime_type": "image/jpeg",
            "file_size": 179757
        },
        "photo": [
            {
                "file_id": "12910487-27041671::1a228f74eca11",
                "file_unique_id": "",
                "width": 1041,
                "height": 1500,
                "file_size": 179757
            }
        ]
    }
}




