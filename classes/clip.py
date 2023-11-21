from dataclasses import dataclass
import datetime


@dataclass
class Clip:
    id: int
    url: str
    broadcaster_id: int
    broadcaster_name: str
    game_id: int
    title: str
    view_count: int
    created_at: datetime.datetime
    thumbnail_url: str
    duration: int
    path: str

    def to_json(self):
        """_summary_

        Returns:
            dict: returns the data object as a dictionary
        """
        return {
            "id": self.id,
            "url": self.url,
            "broadcaster_id": self.broadcaster_id,
            "broadcaster_name": self.broadcaster_name,
            "game_id": self.game_id,
            "title": self.title,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat(),
            "thumbnail_url": self.thumbnail_url,
            "duration": self.duration,
            "path": self.path,
        }
