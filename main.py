from classes.sqlite import init_db, insert_clip
from classes.twitchclip import TwitchClips
from classes.editing import Edit
from classes.youtube import YoutubeUploader
import os

twitch_clips = TwitchClips()
twitch_clips.get_clip_ids()
twitch_clips.prepare_clips()

# list of twitch clips
clips = twitch_clips.clips

# # Download all clips
twitch_clips.download_clips()

# # Edit clips
editor = Edit()

# Edit, saves compilation and returns compilation object
editor.edit(clips)

# # Generate title and description
compilation = editor.video_info(clips)
print(compilation.title)
print(compilation.description)

# # Init youtube uploader
# uploader = YoutubeUploader()

# # Authenticate
# uploader.get_authenticated_service()
# # uploader.upload_video(compilation)
