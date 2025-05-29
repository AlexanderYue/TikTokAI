from TikTokApi import TikTokApi
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from proxyproviders import Webshare
from openai import OpenAI
import time
import random
import yt_dlp
import io
import asyncio
import os
import re
import json
import whisper
import requests

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"
ms_token = os.environ.get("MS_TOKEN")  # Get your ms_token from environment variables
model = whisper.load_model("tiny")

pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

#gen_url = "https://api.aivideoapi.com/runway/generate/text"


client = OpenAI(
    api_key = os.getenv('OpenAIKey')
)

def videoSynth(message):
    # Define the payload for the API request
    payload = {
        "text_prompt": "news presentation, argumentative, " + message,  # Fixed spelling error and spacing
        "model": "gen3",
        "width": 1344,
        "height": 768,
        "motion": 5,
        "seed": 0,
        "callback_url": "",
        "time": 5
    }

    # Define the headers
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "174ced9bf7c12470088e23fcac9dcb911"  # Added 'Bearer' for token-based authorization
    }
    response = requests.post(gen_url, json=payload, headers=headers)

    return response.text


def askLLM(message, comments):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Provide a counter-arguement script to the following video transcription, that I can easly synthesize into video using another AI software such as deepbrain. This transcript should have last roughly 30 seconds long when read at a normal pace. Do not use '/n' or anything like that, just give words. Involve the sentiment of the comments in your creation, do not quote. Use online resources with your web tool to research deeply on the topic covered in the transcript: {message},additionally, utilize the following sentiments from the comments to build a better script: {comments}"
            }
        ],
        model="o1-preview",
    )
    return chat_completion.choices[0].message.content


async def get_comments(video_id, filename):
    async with TikTokApi() as api:
        # Initialize TikTokApi session
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

        # Get the video object
        video = api.video(id=video_id)
        count = 0
        # Iterate through comments
        with open(filename, 'w', encoding='utf-8') as f:
            async for comment in video.comments(count=15):  # Adjust `count` as needed
                print(comment.text)  # Print comment text to console
                sentimentAnalysis(filename, comment.text)
                append_to_file(filename, comment.text)


def transcribe_audio(file_path):
    print(file_path)
    result = model.transcribe(file_path)
    return result['text']


def download_audio_from_tiktok(url):
    try:
        print(f"Downloading audio from: {url}")
        
        # Options to download and convert audio to mp3
        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best available audio
            'postprocessors': [{  # Ensure conversion to mp3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Set desired MP3 quality
            }],
            'outtmpl': 'audio.%(ext)s',  # Save with a fixed name 'audio' and proper extension
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_file = 'audio.mp3'  # The file will always be saved as audio.mp3 after conversion
            print(f"Downloaded and converted audio file: {audio_file}")
        
        return audio_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def save_to_file(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def append_to_file(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a', encoding='utf-8') as f:
        if f.tell() == 0:
            f.write('[')
        else:
            f.write(',\n')
        json.dump(data, f, ensure_ascii=False, indent=4)
    # No need to close the file manually, as 'with' handles that

# Sentiment analysis function
def sentimentAnalysis(filename, text):
    """Analyze the sentiment of a text."""
    result = pipe(text)
    # Return the classification label (positive, negative, neutral) and score
    sentiment = result[0]["label"]
    score = result[0]["score"]
    sentimentScore = "Sentiment:", sentiment, "| Score:", score
    print(sentimentScore)
    append_to_file(filename, sentimentScore)
    #return {"sentiment": sentiment, "score": score}




async def user_example():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser = 'chromium', headless = False)
        username = "cnn" #change this per user
        user = api.user(username)
        user_data = await user.info()
        save_to_file("info/user_info.json", user_data)
        #print(user_data)
        vidCnt = 0
        async for video in user.videos(count=30):
            vidCnt += 1
            # Extract the video ID
            match = re.search(r"id='(\d+)'", str(video))
            if match:
                vidID = match.group(1)  # Extract the matched number (video ID)
                print(f"Video ID: {vidID}")
                print(f"https://tiktok.com/@{username}/video/{vidID}") #this is the link to the video
            
            vidLink = f"https://tiktok.com/@{username}/video/{vidID}"
            append_to_file("info/user_video_info.json", video.as_dict)
            
            # Download and process audio
            audioFile = download_audio_from_tiktok(vidLink)
            if audioFile==False:
                print("")
                print("-------------------Video is not correct data type, skipping transcription-------------------")
                print("")
            audioPass = transcribe_audio("audio.mp3")
            folder = f"vid{vidCnt}"
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, "transcript.json")
            commentFilename = os.path.join(folder, "comments.json")
            arguementFilename = os.path.join(folder, "counter.json")
            await get_comments(vidID, commentFilename)
            with open (commentFilename, 'r') as f:
                comments = f.read()
            script = askLLM(audioPass, comments)
            print("This is script: ", script)
            save_to_file(arguementFilename, script)
            print(videoSynth(script))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(audioPass)

            print("-------------Complete-------------------")
            
            # Sleep for 30 seconds between downloads
            print(f"Sleeping for 30 seconds before the next download...")
            await asyncio.sleep(30)  # Pause for 30 seconds



        # Uncomment if you want to process playlists
        # async for playlist in user.playlists():
        #     print(playlist)


if __name__ == "__main__":
    asyncio.run(user_example())