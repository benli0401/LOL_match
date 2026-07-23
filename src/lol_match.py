import requests
import json


class LOLApi:
    def __init__(self, RG_api_key):
        self.header = {
            "X-Riot-Token": RG_api_key,
            "Accept": "application/json"
        }

    def get_puuid(self, game_name, game_tag):
        api_url = f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{game_tag}'
        result = requests.get(url=api_url, headers=self.header)
        return result.text

def main():
    api_key = "RGAPI-6cd0599d-c667-4155-9571-86f14d646fbb"
    api_infra = LOLApi(RG_api_key=api_key)
    puuid = api_infra.get_puuid(game_name="Airhi", game_tag="0203")
    print(puuid)

main()