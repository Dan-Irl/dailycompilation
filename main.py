from classes.sqlite import init_db, insert_clip
from classes.twitchclip import TwitchClips
from classes.editing import Edit
import os

if __name__ == "__main__":
    db_name = "clips.db"
    if not os.path.exists(db_name):
        init_db(db_name)

    # TODO fix scaper fopr WSL
    twitch_clips = TwitchClips()
    # twitch_clips.get_clip_ids()
    twitch_clips.clips_id_list = [
        "CarefulBlitheCheetahDendiFace-ecWD2KF-SFxyzHI2",
        "CarefulBlitheCheetahDendiFace-ecWD2KF-SFxyzHI2",
    ]
    twitch_clips.prepare_clips()

    # list of twitch clips
    clips = twitch_clips.clips

    # Download all clips
    # twitch_clips.download_clips()

    # Edit clips
    editor = Edit()

    # Edit, saves compilation and returns compilation object
    compilation = editor.edit(twitch_clips.clips)
