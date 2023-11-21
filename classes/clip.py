from dataclasses import dataclass
import datetime


@dataclass
class Clip:
    def __init__(
        self,
        id: int,
        url: str,
        broadcaster_id: int,
        broadcaster_name: str,
        game_id: int,
        title: str,
        view_count: int,
        created_at: datetime.datetime,
        thumbnail_url: str,
        duration: int,
        path: str,
    ):
        self.id = (id,)
        self.url = (url,)
        self.broadcaster_id = (broadcaster_id,)
        self.broadcaster_name = (broadcaster_name,)
        self.game_id = (game_id,)
        self.title = (title,)
        self.view_count = (view_count,)
        self.created_at = (created_at,)
        self.thumbnail_url = (thumbnail_url,)
        self.duration = duration
        self.path = path

    def to_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "broadcaster_id": self.broadcaster_id,
            "broadcaster_name": self.broadcaster_name,
            "game_id": self.game_id,
            "title": self.title,
            "view_count": self.view_count,
            "created_at": self.created_at,
            "thumbnail_url": self.thumbnail_url,
            "duration": self.duration,
            "path": self.path,
        }
