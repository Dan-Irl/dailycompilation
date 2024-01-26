from dataclasses import dataclass
import datetime


@dataclass
class Clip:
    id: int = None
    url: str = None
    video_url: str = None
    broadcaster_id: int = None
    broadcaster_name: str = None
    game_id: int = None
    game_name: str = None
    title: str = None
    view_count: int = None
    created_at: datetime.datetime = None
    thumbnail_url: str = None
    thumbnail_path: str = None
    duration: int = None
    clip_path: str = None
    deleted: int = None
    posted: int = None

    def to_json(self):
        """_summary_

        Returns:
            dict: returns the data object as a dictionary
        """
        return {
            "id": self.id,
            "url": self.url,
            "video_url": self.video_url,
            "broadcaster_id": self.broadcaster_id,
            "broadcaster_name": self.broadcaster_name,
            "game_id": self.game_id,
            "game_name": self.game_name,
            "title": self.title,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat(),
            "thumbnail_url": self.thumbnail_url,
            "duration": self.duration,
            "clip_path": self.clip_path,
            "thumbnail_path": self.thumbnail_path,
            "deleted": self.deleted,
            "posted": self.posted,
        }
