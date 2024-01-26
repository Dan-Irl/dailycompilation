from classes.sqlite import init_db, insert_clip
from classes.twitchclip import TwitchClips
import os

if __name__ == "__main__":
    db_name = "clips.db"
    if not os.path.exists(db_name):
        init_db(db_name)

    twitch_clips = TwitchClips()
    twitch_clips.get_clip_ids()
    twitch_clips.prepare_clips()
    twitch_clips.download_clips()

    # for clip in twitch_clips.clips:
    #     insert_clip(db_name, clip)
