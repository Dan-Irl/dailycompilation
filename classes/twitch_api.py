import requests


class TwitchAPI:
    def __init__(self):
        self.headers = None

    def auth(self, client_id, client_secret):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"

        try:
            response = requests.post(
                "https://id.twitch.tv/oauth2/token", headers=headers, data=data
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        bearer = response.json()["access_token"]

        self.headers = {
            "Authorization": f"Bearer {bearer}",
            "Client-Id": client_id,
        }

    def get_clip(self, clip_id):
        """
        Retrieves information about a specific Twitch clip.

        Args:
            clip_id (str): The ID of the clip to retrieve.

        Returns:
            dict: A dictionary containing information about the clip.
        """
        try:
            response = requests.get(
                f"https://api.twitch.tv/helix/clips?id={clip_id}", headers=self.headers
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        return response.json()["data"][0]

    def get_game(self, game_id):
        """
        Retrieves the name of a game based on its ID from the Twitch API.

        Args:
            game_id (str): The ID of the game.

        Returns:
            str: The name of the game.
        """
        try:
            response = requests.get(
                f"https://api.twitch.tv/helix/games?id={game_id}", headers=self.headers
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        return response.json()["data"][0]["name"]
