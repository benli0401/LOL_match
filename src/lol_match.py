import requests
import json
import os
from dotenv import load_dotenv


class RiotAccountClient:
    def __init__(self, game_name, game_tag, headers):
        self.game_name = game_name
        self.game_tag = game_tag
        self.headers = headers

    def get_puuid(self):
        url = (
            f"https://asia.api.riotgames.com/"
            f"riot/account/v1/accounts/by-riot-id/"
            f"{self.game_name}/{self.game_tag}"
        )

        response = requests.get(
            url=url,
            headers=self.headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()["puuid"]

load_dotenv()
def main():
    api_key = os.getenv("RGAPI_KEY")
    api_headers = {
            "X-Riot-Token": api_key,
            "Accept": "application/json"
        }
    
    puuid = RiotAccountClient(game_name="Airhi", game_tag="0203", headers=api_headers).get_puuid()
    print(puuid)

main()