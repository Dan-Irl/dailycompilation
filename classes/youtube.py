import os
import random
import time
import json
import httplib2
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from classes.compilation import Compilation

scopes = ["https://www.googleapis.com/auth/youtube.upload"]
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error,)
MAX_RETRIES = 10


class YoutubeUploader:
    def __init__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "dailycompilation/client_secret.json"
        self.refresh_token_file = "dailycompilation/refresh_token.json"
        self.client_id = str(os.getenv("YT_CLIENT_ID"))
        self.client_secret = str(os.getenv("YT_CLIENT_SECRET"))

    def get_authenticated_service(self):
        credentials = None
        # Check if refresh token exists
        if os.path.exists(self.refresh_token_file):
            with open(self.refresh_token_file, "r") as token_file:
                refresh_token = json.load(token_file).get("refresh_token")
                if refresh_token:
                    credentials = Credentials(
                        None,
                        refresh_token=refresh_token,
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=self.client_id,
                        client_secret=self.client_secret,
                        scopes=scopes,
                    )
                    # Refresh the token
                    credentials.refresh(Request())
                    print("Refreshed token")

        if not credentials or not credentials.valid:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, scopes
            )
            credentials = flow.run_local_server()
            # Save refresh token for next time

            auth_url, _ = flow.authorization_url(prompt="consent")

            print(f"Please go to this URL: {auth_url}")
            print(
                "After granting access, copy the code you're given and paste it here."
            )

            code = input("Enter the authorization code: ")
            credentials = flow.fetch_token(code=code)

            with open(self.refresh_token_file, "w") as token_file:
                json.dump({"refresh_token": credentials.refresh_token}, token_file)

        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials
        )

    def upload_thumbnail(self, video_id, file_path):
        print("Uploading thumbnail...")
        request = self.youtube.thumbnails().set(videoId=video_id, media_body=file_path)
        response = request.execute()
        print(response)

    def upload_video(self, video_content: Compilation):
        body = dict(
            snippet=dict(
                title=video_content.title,
                description=video_content.description,
                tags=video_content.tags,
                categoryId=video_content.category_id,
            ),
            status=dict(privacyStatus=video_content.privacy_status),
        )

        insert_request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(
                video_content.path, chunksize=-1, resumable=True
            ),
        )

        video_id = self.resumable_upload(insert_request)
        self.upload_thumbnail(
            video_id, "dailycompilation/data/thumbnails/thumbnail.png"
        )

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if "id" in response:
                        print(
                            "Video id '%s' was successfully uploaded." % response["id"]
                        )
                        return response["id"]
                    else:
                        exit(
                            "The upload failed with an unexpected response: %s"
                            % response
                        )
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = (
                        f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                    )
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = f"A retriable error occurred: {e}"

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2**retry
                sleep_seconds = random.random() * max_sleep
                print(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)
