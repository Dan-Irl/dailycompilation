from classes.clip import *

if __name__ == "__main__":
    db_name = "clips.db"
    init_db(db_name)

    twitch_clips = TwitchClips()
    twitch_clips.get_clip_ids()
    twitch_clips.prepare_clips()

    for clip in twitch_clips.clips:
        insert_clip(db_name, clip)