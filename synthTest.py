import requests
import time


# Step 1: Generate video via HeyGen API
url = "https://api.heygen.com/v2/video/generate"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "Y2Q2M2VkYjY2NmFlNGRiMWEyMmEzODcyYWZlM2RlODItMTczNTkyMjIzOQ=="
}

payload = {
    "caption": True,
    "dimension": {"width": 720, "height": 1280},
    "title": "test2",
    "callback_id": "test2",
    "video_inputs": [
        {
            "character": {
                "type": "avatar",
                "avatar_id": "Bryan_IT_Sitting_public",
                "scale": 1,
                "avatar_style": "normal",
                "offset": {"x": 0, "y": 0}
            },
            "voice": {
                "type": "text",
                "voice_id": "cc29d03937d14240acf109c827a9a51a",
                "input_text": " The family of an Ohio man who died in sheriff's custody is demanding action against the jail employees involved in his restraint. The family of an Ohio man who died in sheriff's custody is a criminal. 25-year-old Christian Black was arrested and taken to the Montgomery County jail on March 24th for an alleged incident involving a car jacking. Black appears agitated in the video and has seen repeatedly striking his head and body against a cell window. At least 10 correctional officers were prayer outside before entering and attempting to restrain him. While it appears Black is having some kind of crisis, his family told CNN that he did not have any mental health issues and was not on any prescribed medication. The officers deployed a stun gun and eventually overpower Black, putting him in a safety restraint chair. Black is eventually forced forward by corrections officers while restrained in the chair with his hands behind his back. About two minutes later Black appears unconscious, leaning back in the chair according to the sheriff's office. One officer continues to firmly hold his face back which is now restrained in a mask. You're getting out of the chair because I don't feel a heartbeat. I don't feel heartbeat. minutes later some of the same officers involved in restraining Black are seen performing CPR on him. Black was eventually transported to the hospital by the date and fire department where he died two days later. Black's cause of death was ruled a homicide likely caused by mechanical and positional asphyxia according to the coroner's officers preliminary findings. The Ohio Patrolman's Benevolent Association defended the deputies involved in a statement to CNN and said several officers were used to contain Black because of his size and strength. It says their actions were consistent with their training and practice and were used in an effort to prevent Black from injuring or killing himself. Black's family is calling on the sheriff to resign and is now considering civil litigation. The sheriff expressed condolences to the family and pledged to cooperate with all independent investigations. The sheriff's office said the ten employees involved in the incident have been placed on paid administrative leave. The date in police department homicide unit is investigating the incident. A sheriff's spokesperson told CNN."
            },
            "background": {
                "type": "color",
                "value": "#008000"
            }
        }
    ],
    "folder_id": "string",
    "callback_url": "test2"
}

# Make POST request to generate the video
response = requests.post(url, json=payload, headers=headers)

# Step 2: Extract video_id from response
if response.status_code == 200:
    data = response.json()
    video_id = data.get("data", {}).get("video_id")
    if not video_id:
        print("❌ Video ID not found in response.")
        print(data)
        exit(1)
    print(f"✅ Video ID: {video_id}")
    print(data)
else:
    print(f"❌ Failed to generate video. Status code: {response.status_code}")
    exit(1)

# Step 3: Poll until video is ready (optional but recommended)
# Replace with actual HeyGen status check API if available

print("⏳ Waiting 30 seconds before attempting to download...")
#time.sleep(30)

# Step 4: Download the video
download_url = f"https://app.heygen.com/share/{video_id}"
output_filename = "AviVideo.mp4"


# Replace with your actual API key and video ID
api_key = "Y2Q2M2VkYjY2NmFlNGRiMWEyMmEzODcyYWZlM2RlODItMTczNTkyMjIzOQ=="

headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}

# URL to check video status
video_status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"

while True:
    response = requests.get(video_status_url, headers=headers)
    status = response.json()["data"]["status"]

    if status == "completed":
        video_url = response.json()["data"]["video_url"]
        thumbnail_url = response.json()["data"]["thumbnail_url"]
        print(f"Video generation completed! \nVideo URL: {video_url} \nThumbnail URL: {thumbnail_url}")

        # Save the video to a file
        video_filename = "generated_video.mp4"
        video_content = requests.get(video_url).content
        with open(video_filename, "wb") as video_file:
            video_file.write(video_content)
        break
        
    elif status in ["processing", "pending"]:
        print("Video is still processing. Checking status...")
        time.sleep(5)  # Sleep for 5 seconds before checking again
        
    elif status == "failed":
        error = response.json()["data"]["error"]
        print(f"Video generation failed. '{error}'")
        break