from dotenv import load_dotenv
import os
from classes.twitch_api import TwitchAPI
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from classes.clip import Clip
import requests
import time
import logging

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

        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--enable-javascript")

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_clip_ids(self):
        # Get url content
        self.driver.get(self.clips_url)

        try:
            # Wait for a specific element to be loaded for up to 30 seconds
            # Replace 'someElementId' with the actual ID or element you expect to be present
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "clips-day"))
            )

            # Now you can scrape the page or interact with it as needed
            content = self.driver.page_source

            # Log HTML to a file
            try:
                with open(
                    "dailycompilation/logs/page_source.html", "w", encoding="utf-8"
                ) as file:
                    file.write(content)
            except Exception as e:
                logging.warning(f"Could not write html file: {e}")

        except Exception as e:
            logging.warning(f"Error during webpage loading: {e}")

        finally:
            # Close the WebDriver
            self.driver.quit()

        logging.info("Finished scrape and closed driver")

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
                    thumbnail_path=f"dailycompilation/data/thumbnails/{clip_id}.jpg",
                    duration=clip["duration"],
                    clip_path=f"dailycompilation/data/clips/{clip_id}.mp4",
                )

                self.clips.append(clip_instance)
            except Exception as e:
                print(e)

    def download_clips(self):
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--enable-javascript")

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)

        for clip in self.clips:
            # Go to the URL of the twitch clip
            self.driver.get(clip.url)

            try:
                # Wait for the mature content button to be clickable (with increased timeout)
                wait = WebDriverWait(self.driver, 2)  # Increased timeout
                mature_content_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="channel-player-gate"]/div/div/div[4]/div/button',
                        )
                    )
                )

                # Click the mature content button if found
                mature_content_button.click()
            except TimeoutException:
                pass

            # Scrape clip URL
            content = self.driver.page_source
            soup = BeautifulSoup(content, "html.parser")

            # parse video URL of the clip
            try:
                clip_url = soup.find("video")["src"]
                clip_id = clip.id
                file_name = "dailycompilation/data/clips/" + clip_id + ".mp4"
            except Exception as e:
                raise Exception(f"Could not parse clip URL: {e}")

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
