import requests
import json

# HeyGen API endpoint to list avatars
url = "https://api.heygen.com/v2/avatars"

# Headers including your API key
headers = {
    "accept": "application/json",
    "x-api-key": "Y2Q2M2VkYjY2NmFlNGRiMWEyMmEzODcyYWZlM2RlODItMTczNTkyMjIzOQ=="
}

# Send GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    avatars = response.json()
    
    # Pretty print to console
    print("Available Avatars:\n")
    print(json.dumps(avatars, indent=4))
    
    # Write to file
    with open("heygen_avatars.json", "w") as f:
        json.dump(avatars, f, indent=4)
    
    print("\nAvatar data saved to 'heygen_avatars.json'")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)


# HeyGen API endpoint to list voices
url = "https://api.heygen.com/v2/voices"

# Headers with your API key
headers = {
    "accept": "application/json",
    "x-api-key": "Y2Q2M2VkYjY2NmFlNGRiMWEyMmEzODcyYWZlM2RlODItMTczNTkyMjIzOQ=="
}

# Send GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    voices = response.json()
    
    # Print to console (optional)
    print("Available Voices:\n")
    print(json.dumps(voices, indent=4))
    
    # Write to file
    with open("heygen_voices.json", "w") as f:
        json.dump(voices, f, indent=4)
    
    print("\nVoice data saved to 'heygen_voices.json'")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)


#            {
#                "avatar_id": "Bryan_IT_Sitting_public",
#                "avatar_name": "Bryan Tech Expert",
#                "gender": "male",
#                "preview_image_url": "https://files2.heygen.ai/avatar/v3/33c9ac4aead44dfc8bc0082a35062a70_45580/preview_talk_3.webp",
#                "preview_video_url": "https://files2.heygen.ai/avatar/v3/33c9ac4aead44dfc8bc0082a35062a70_45580/preview_video_talk_3.mp4",
#                "premium": false,
#                "type": null,
#                "tags": null,
#                "default_voice_id": null
#            },