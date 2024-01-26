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
        self.fontsize_main = os.getenv("FONTSIZE_MAIN")
        self.fontsize_sub = os.getenv("FONTSIZE_SUB")
        self.text_color = os.getenv("TEXT_COLOR")
        self.font = os.getenv("FONT")
        self.background_color = os.getenv("BACKGROUND_COLOR")
        self.opacity = os.getenv("OPACITY")

        self.edited_clips = []

        # Init compilation object

        self.compilation = Compilation()

    def edit(self, clips: list[Clip]) -> Compilation:
        for clip in clips:
            # Create text clips
            main_title = TextClip(
                f"{clip.title}",
                fontsize=self.fontsize_main,
                color=self.text_color,
                font=self.font,
            )
            sub_title = TextClip(
                f"{clip.title} - {clip.game_name}",
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
            main_title = main_title.set_position(("left", 10))
            subtitle = subtitle.set_position(("left", main_title.size[1] + 10))
            background = background.set_position(("left", "bottom"))

            # Composite the text and the background
            txt_clip = CompositeVideoClip(
                [background, main_title, subtitle],
                size=(text_width + 20, text_height + 20),
            )
            txt_clip = txt_clip.set_position(("center", "bottom")).set_duration(5)

            video = CompositeVideoClip(
                [clip, txt_clip.set_start(0)]
            )  # Adjust set_start for overlay timing
            self.edited_clips.append(video)

            self.video = concatenate_videoclips(self.edited_clips)
            
            # save path
            path = f"dailycompilation/data/compilations/{datetime.now().strftime("%y/%m/%d")}.mp4"
            self.video.write_videofile(path)
            
            # Create compilation object
            self.compilation.path = path

            return self.compilation
            
            
