from dotenv import load_dotenv
import os
from classes.twitch_api import TwitchAPI
from bs4 import BeautifulSoup
from selenium import webdriver
from classes.clip import Clip
import requests
import time

TODO = """
    - Set up logger for TwitchClips"""


class TwitchClips:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.clips_url = os.getenv("URL")

        self.api = TwitchAPI()
        self.api.auth(self.client_id, self.client_secret)

        self.clips_id_list = []
        self.clips = []

    def get_clip_ids(self):
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()

        # Get url content
        self.driver.get(self.clips_url)

        # Wait for Cloudflare's anti-bot page (adjust the time as needed)
        time.sleep(5)

        # Now you can scrape the page or interact with it as needed
        content = self.driver.page_source

        # Close the WebDriver
        self.driver.quit()

        soup = BeautifulSoup(content, "html.parser")

        clips = soup.find("div", id="clips-day").find_all("div", class_="clip-entity")

        for clip in clips:
            clip_id = clip.find("div", class_="clip-tp")["data-litebox"].split("clip=")[
                -1
            ]

            if clip is None:
                continue

            self.clips_id_list.append(clip_id)

    def prepare_clips(self):
        for clip_id in self.clips_id_list:
            try:
                # Get clip information from the Twitch API
                clip = self.api.get_clip(clip_id)

                # Create a Clip instance
                clip_instance = Clip(
                    id=clip["id"],
                    url=clip["url"],
                    broadcaster_id=clip["broadcaster_id"],
                    broadcaster_name=clip["broadcaster_name"],
                    game_id=clip["game_id"],
                    game_name=self.api.get_game(clip["game_id"]),
                    title=clip["title"],
                    view_count=clip["view_count"],
                    created_at=clip["created_at"],
                    thumbnail_url=clip["thumbnail_url"],
                    thumbnail_path=f"data/thumbnails/{clip_id}.jpg",
                    duration=clip["duration"],
                    clip_path=f"data/clips/{clip_id}.mp4",
                )

                self.clips.append(clip_instance)
            except Exception as e:
                print(e)

    def download_clips(self):
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()

        for clip in self.clips:
            # Go to the URL of the twitch clip
            self.driver.get(clip.url)

            # Scrape clip URL
            content = self.driver.page_source
            soup = BeautifulSoup(content, "html.parser")

            # parse video URL of the clip
            try:
                clip_url = soup.find("video")["src"]
                clip_id = clip.id
                file_name = "data/clips/" + clip_id + ".mp4"
            except Exception as e:
                raise e

            if clip_url is None:
                raise Exception("Clip URL is None")

            # Download the clip
            response = requests.get(clip_url, stream=True)

            # Ensure the request is successful
            if response.status_code == 200:
                with open(file_name, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            file.write(chunk)
            else:
                raise Exception("Clip download failed")

        # Close the WebDriver
        self.driver.quit()
