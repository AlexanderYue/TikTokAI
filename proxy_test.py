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

# Use a manually defined list of proxies (IP:PORT:USER:PASS format)
static_proxies = [
    "198.23.239.134:6540:iiwjybdk:au8jnyo1pagk",
    "38.153.152.244:9594:iiwjybdk:au8jnyo1pagk",
    "207.244.217.165:6712:iiwjybdk:au8jnyo1pagk",
    "107.172.163.27:6543:iiwjybdk:au8jnyo1pagk",
    "86.38.234.176:6630:iiwjybdk:au8jnyo1pagk",
    "173.211.0.148:6641:iiwjybdk:au8jnyo1pagk",
    "216.10.27.159:6837:iiwjybdk:au8jnyo1pagk",
    "154.36.110.199:6853:iiwjybdk:au8jnyo1pagk",
    "45.151.162.198:6600:iiwjybdk:au8jnyo1pagk",
    "188.74.210.21:6100:iiwjybdk:au8jnyo1pagk"
]

# Randomly select a proxy from the list
ip, port, user, pwd = random.choice([p.split(':') for p in static_proxies])
proxy_dict = {
    "server": f"http://{user}:{pwd}@{ip}:{port}"
}

ms_token = os.environ.get("MS_TOKEN")
pc = Pinecone(api_key="pcsk_3guZaS_KkcAGTGK3T4YWAFBnC1tmfQWgcbbc9hHzHAQVF64framswjgZhXieBpnR5isBfm")
model = whisper.load_model("tiny")
pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
gen_url = "https://api.aivideoapi.com/runway/generate/text"

client = OpenAI(api_key=os.getenv('OpenAIKey'))

def videoSynth(message):
    payload = {
        "text_prompt": "news presentation, argumentative, " + message,
        "model": "gen3",
        "width": 1344,
        "height": 768,
        "motion": 5,
        "seed": 0,
        "callback_url": "",
        "time": 5
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "174ced9bf7c12470088e23fcac9dcb911"
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

def save_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def append_to_file(filename, data):
    with open(filename, 'a', encoding='utf-8') as f:
        if f.tell() == 0:
            f.write('[')
        else:
            f.write(',\n')
        json.dump(data, f, ensure_ascii=False, indent=4)

def sentimentAnalysis(filename, text):
    result = pipe(text)
    sentiment = result[0]["label"]
    score = result[0]["score"]
    sentimentScore = "Sentiment:", sentiment, "| Score:", score
    print(sentimentScore)
    append_to_file(filename, sentimentScore)

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result['text']

def download_audio_from_tiktok(url):
    try:
        print(f"Downloading audio from: {url}")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio.%(ext)s',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_file = 'audio.mp3'
        return audio_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

async def get_comments(video_id, filename):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, proxy=proxy_dict)
        video = api.video(id=video_id)
        with open(filename, 'w', encoding='utf-8') as f:
            async for comment in video.comments(count=15):
                print(comment.text)
                sentimentAnalysis(filename, comment.text)
                append_to_file(filename, comment.text)

async def user_example():
    async with TikTokApi(proxy=proxy_dict) as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)        
        username = "foxnews"
        user = api.user(username)
        user_data = await user.info()
        save_to_file("user_info.json", user_data)

        vidCnt = 0
        async for video in user.videos(count=30):
            vidCnt += 1
            match = re.search(r"id='(\d+)'", str(video))
            if match:
                vidID = match.group(1)
                print(f"Video ID: {vidID}")
                print(f"https://tiktok.com/@{username}/video/{vidID}")
            vidLink = f"https://tiktok.com/@{username}/video/{vidID}"
            append_to_file("user_video_info.json", video.as_dict)

            audioFile = download_audio_from_tiktok(vidLink)
            if not audioFile:
                print("\n-------------------Video is not correct data type, skipping transcription-------------------\n")
                continue
            audioPass = transcribe_audio("audio.mp3")
            filename = f"vid{vidCnt}Transcript.json"
            commentFilename = f"vid{vidCnt}Comments.json"
            arguementFilename = f"vid{vidCnt}Counter.json"

            await get_comments(vidID, commentFilename)
            with open(commentFilename, 'r') as f:
                comments = f.read()
            script = askLLM(audioPass, comments)
            print("This is script: ", script)
            save_to_file(arguementFilename, script)
            print(videoSynth(script))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(audioPass)

            print("-------------Complete-------------------")
            print("Sleeping for 30 seconds before the next download...")
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(user_example())
