import requests

url = "https://api.heygen.com/v2/video/generate"

payload = {
    "caption": True,
    "dimension": {
        "width": 1280,
        "height": 720
    },
    "title": "test",
    "callback_id": "test",
    "video_inputs": [
        {
            "character": {
                "type": "avatar",
                "avatar_id": "string",
                "talking_photo_id": "ca1fd2232b5247bf85c1f0e4c4929f65",
                "scale": 1,
                "avatar_style": "normal",
                "offset": {
                    "x": 0,
                    "y": 0
                },
                "circle_background_color": "string",
                "talking_photo_style": "string",
                "talking_style": "stable",
                "expression": "default",
                "super_resolution": "string"
            },
            "voice": {
                "type": "string",
                "voice_id": "cc29d03937d14240acf109c827a9a51a",
                "input_text": " The family of an Ohio man who died in sheriff's custody is demanding action against the jail employees involved in his restraint. The family of an Ohio man who died in sheriff's custody is a criminal. 25-year-old Christian Black was arrested and taken to the Montgomery County jail on March 24th for an alleged incident involving a car jacking. Black appears agitated in the video and has seen repeatedly striking his head and body against a cell window. At least 10 correctional officers were prayer outside before entering and attempting to restrain him. While it appears Black is having some kind of crisis, his family told CNN that he did not have any mental health issues and was not on any prescribed medication. The officers deployed a stun gun and eventually overpower Black, putting him in a safety restraint chair. Black is eventually forced forward by corrections officers while restrained in the chair with his hands behind his back. About two minutes later Black appears unconscious, leaning back in the chair according to the sheriff's office. One officer continues to firmly hold his face back which is now restrained in a mask. You're getting out of the chair because I don't feel a heartbeat. I don't feel heartbeat. minutes later some of the same officers involved in restraining Black are seen performing CPR on him. Black was eventually transported to the hospital by the date and fire department where he died two days later. Black's cause of death was ruled a homicide likely caused by mechanical and positional asphyxia according to the coroner's officers preliminary findings. The Ohio Patrolman's Benevolent Association defended the deputies involved in a statement to CNN and said several officers were used to contain Black because of his size and strength. It says their actions were consistent with their training and practice and were used in an effort to prevent Black from injuring or killing himself. Black's family is calling on the sheriff to resign and is now considering civil litigation. The sheriff expressed condolences to the family and pledged to cooperate with all independent investigations. The sheriff's office said the ten employees involved in the incident have been placed on paid administrative leave. The date in police department homicide unit is investigating the incident. A sheriff's spokesperson told CNN.",
                "speed": 0,
                "pitch": 0,
                "emotion": "Excited",
                "locale": "string"
            },
            "background": {
                "type": "color",
                "value": "string",
                "": "string"
            },
            "text": {
                "type": "text",
                "text": "string",
                "font_family": "string",
                "font_size": 0,
                "font_weight": "bold",
                "color": "string",
                "position": {
                    "x": 0,
                    "y": 0
                },
                "text_align": "left",
                "line_height": 0
            }
        }
    ],
    "folder_id": "string",
    "callback_url": "test"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "Y2Q2M2VkYjY2NmFlNGRiMWEyMmEzODcyYWZlM2RlODItMTczNTkyMjIzOQ=="
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)