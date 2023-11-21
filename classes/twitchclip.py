from dotenv import load_dotenv
import os
from classes.twitch_api import TwitchAPI
from bs4 import BeautifulSoup
from selenium import webdriver
from classes.clip import Clip

TODO = """
    - Set up logger for TwitchClips"""


class TwitchClips:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.url = os.getenv("URL")

        self.api = TwitchAPI()
        self.api.auth(self.client_id, self.client_secret)

        # Initialize the WebDriver (example using Chrome)
        self.driver = webdriver.Chrome()

        self.clips_id_list = []
        self.clips = []

    def get_clip_ids(self):
        # Go to the URL
        self.driver.get(self.url)

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
                clip = self.api.get_clip(clip_id)
                clip = Clip(
                    clip["id"],
                    clip["url"],
                    clip["broadcaster_id"],
                    clip["broadcaster_name"],
                    clip["game_id"],
                    clip["title"],
                    clip["view_count"],
                    clip["created_at"],
                    clip["thumbnail_url"],
                    clip["duration"],
                    f"clips/{clip_id}.mp4",
                )

                self.clips.append(clip)
            except Exception as e:
                print(e)

    def download_clips(self):
        for clip in self.clips:
            pass
