from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip,
    ColorClip,
)
from classes.clip import Clip
from classes.compilation import Compilation
from dotenv import load_dotenv
import os
from datetime import datetime


class Edit:
    def __init__(self) -> None:
        load_dotenv()
        self.fontsize_main = int(os.getenv("FONTSIZE_MAIN"))
        self.fontsize_sub = int(os.getenv("FONTSIZE_SUB"))
        self.text_color = str(os.getenv("TEXT_COLOR"))
        self.font = str(os.getenv("FONT"))
        self.background_color = tuple(map(int,os.getenv("BACKGROUND_COLOR").split(',')))
        self.opacity = float(os.getenv("OPACITY"))
        
        # Video info
        self.video_title = os.getenv("VIDEO_TITLE")
        self.video_gategory_id = int(os.getenv("VIDEO_CATEGORY"))
        self.video_tags = os.getenv("VIDEO_TAGS").split(",")


        self.edited_clips = []

        # Init video
        self.video = None

        # Init compilation object
        self.compilation = Compilation()

    def edit(self, clips: list[Clip]) -> Compilation:
        for clip in clips:
            # Get the clip video file from clip path
            clip_file = VideoFileClip(clip.clip_path).resize(newsize=(1920, 1080))

            # Create text clips
            main_title = TextClip(
                f"{clip.title}",
                fontsize=self.fontsize_main,
                color=self.text_color,
                font=self.font,
            )
            sub_title = TextClip(
                f"{clip.broadcaster_name} - {clip.game_name}",
                fontsize=self.fontsize_sub,
                color=self.text_color,
                font=self.font,
            )

            text_width = max(main_title.size[0], sub_title.size[0])
            text_height = main_title.size[1] + sub_title.size[1]

            # Create a background box for the text
            background = ColorClip(
                size=(text_width + 20, text_height + 20), color=self.background_color
            ).set_opacity(self.opacity)

            # Set the position of the text and the background
            main_title = main_title.set_position(("center", 10))
            sub_title = sub_title.set_position(("center", main_title.size[1] + 10))
            background = background.set_position(("center", "bottom"))

            # Composite the text and the background
            txt_clip = CompositeVideoClip(
                [background, main_title, sub_title],
                size=(text_width + 20, text_height + 20),
            )
            txt_clip = txt_clip.set_position(("left", "top")).set_duration(7)

            video = CompositeVideoClip(
                [clip_file, txt_clip.set_start(0)]
            )  # Adjust set_start for overlay timing
            self.edited_clips.append(video)

        self.video = concatenate_videoclips(self.edited_clips)

        # save path
        path = f"dailycompilation/data/compilations/{datetime.now().strftime("%Y_%m_%d")}.mp4"
        self.video.write_videofile(path, fps=24)

        # Create compilation object
        self.compilation.path = path

        return self.compilation
    
    def video_info(self, clips: list[Clip]) -> Compilation:
        # Takes the clips and check the duration of each clip to create a timestamp description of the compilation
        video_info = {}
        
        video_title = self.video_title
        video_info["title"] = video_title
        
        description_prefix = f"Most viewed Twitch clips of the day ({datetime.now().strftime("%Y-%m-%d")}).\n\n"
        
        # Initialize the starting time
        current_time = 0

        # Building the video description
        timestamp_list = []
        
        for clip in clips:
            # Get the clip duration
            clip_duration = clip.duration

            # Add the clip duration to the current time
            endtime = current_time + clip_duration

            # Convert the current time to a timestamp
            timestamp = f"{datetime.utcfromtimestamp(current_time).strftime('%M:%S')} - {datetime.utcfromtimestamp(endtime).strftime('%M:%S')} : www.twitch.tv/{clip.broadcaster_name}"

            # Update the current time
            current_time = endtime
            
            # Add the timestamp to the timestamp list
            timestamp_list.append(timestamp)
            
        # Add the timestamp list to the description
        video_info["description"] = description_prefix + "\n".join(timestamp_list)
        
        video_info["tags"] = self.video_tags
        video_info["category_id"] = self.video_gategory_id 
        
        self.compilation.title = video_title
        self.compilation.description = video_info["description"]
        self.compilation.tags = video_info["tags"]
        self.compilation.category_id = video_info["category_id"]
            
        return self.compilation
        
        
