import os

import requests
from dotenv import load_dotenv
from src.system_prompt import build_match_prompt
from src.discord_bot import DiscordWebhookClient


class RiotAccountClient:
    def __init__(self, game_name, game_tag, headers):
        self.game_name = game_name
        self.game_tag = game_tag
        self.headers = headers

    def get_puuid(self):
        url = (
            "https://asia.api.riotgames.com/"
            "riot/account/v1/accounts/by-riot-id/"
            f"{self.game_name}/{self.game_tag}"
        )

        response = requests.get(
            url=url,
            headers=self.headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()["puuid"]

    def get_match_id(self, puuid):
        url = (
            "https://sea.api.riotgames.com/"
            "lol/match/v5/matches/by-puuid/"
            f"{puuid}/ids?start=0&count=1"
        )

        response = requests.get(
            url=url,
            headers=self.headers,
            timeout=10
        )

        response.raise_for_status()

        match_ids = response.json()

        if not match_ids:
            return None

        return match_ids[0]

    def get_match_info(self, match_id):
        url = (
            "https://sea.api.riotgames.com/"
            "lol/match/v5/matches/"
            f"{match_id}"
        )

        response = requests.get(
            url=url,
            headers=self.headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()


class MatchFormatter:
    POSITION_MAP = {
        "TOP": "上路",
        "JUNGLE": "打野",
        "MIDDLE": "中路",
        "BOTTOM": "下路",
        "UTILITY": "輔助",
    }

    POSITION_ORDER = {
        "TOP": 0,
        "JUNGLE": 1,
        "MIDDLE": 2,
        "BOTTOM": 3,
        "UTILITY": 4,
    }

    def __init__(self, match_info, target_puuid):
        self.match_info = match_info
        self.target_puuid = target_puuid

    def get_game_time(self):
        game_duration = self.match_info["info"]["gameDuration"]

        minutes = game_duration // 60
        seconds = game_duration % 60

        return f"{minutes}:{seconds:02d}"

    def get_target_player(self):
        participants = self.match_info["info"]["participants"]

        for participant in participants:
            if participant["puuid"] == self.target_puuid:
                return participant

        return None

    def format_player(self, participant):
        position = self.POSITION_MAP.get(
            participant["teamPosition"],
            participant["teamPosition"]
        )

        champion = participant["championName"]
        kills = participant["kills"]
        deaths = participant["deaths"]
        assists = participant["assists"]
        damage = participant["totalDamageDealtToChampions"]

        return (
            f"{position}: {champion}, "
            f"KDA: {kills}/{deaths}/{assists}, "
            f"英雄傷害: {damage:,}"
        )

    def get_team_players(self, team_id):
        participants = self.match_info["info"]["participants"]

        players = [
            participant
            for participant in participants
            if participant["teamId"] == team_id
        ]

        return sorted(
            players,
            key=lambda player: self.POSITION_ORDER.get(
                player["teamPosition"],
                99
            )
        )

    def build_result(self):
        target_player = self.get_target_player()

        if target_player is None:
            raise ValueError("找不到目標玩家")

        result = "WIN" if target_player["win"] else "LOSE"
        game_time = self.get_game_time()

        blue_players = self.get_team_players(100)
        red_players = self.get_team_players(200)

        lines = [
            result,
            f"遊戲時間: {game_time}",
            "",
            "玩家:",
            self.format_player(target_player),
            "",
            "藍方:",
        ]

        for player in blue_players:
            lines.append(self.format_player(player))

        lines.append("")
        lines.append("紅方:")

        for player in red_players:
            lines.append(self.format_player(player))

        return "\n".join(lines)


load_dotenv()


def main():
    roit_api_key = os.getenv("RGAPI_KEY")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not roit_api_key:
        raise RuntimeError("找不到 RGAPI_KEY")

    if not discord_webhook_url:
        raise RuntimeError("找不到 DISCORD_WEBHOOK_URL")


    discord = DiscordWebhookClient(
        webhook_url=discord_webhook_url
    )

    api_headers = {
        "X-Riot-Token": roit_api_key,
        "Accept": "application/json"
    }

    riot_client = RiotAccountClient(
        game_name="Airhi",
        game_tag="0203",
        headers=api_headers
    )

    puuid = riot_client.get_puuid()

    match_id = riot_client.get_match_id(
        puuid=puuid
    )

    if match_id is None:
        print("找不到歷史對戰")
        return

    match_info = riot_client.get_match_info(
        match_id=match_id
    )

    formatter = MatchFormatter(
        match_info=match_info,
        target_puuid=puuid
    )

    result = formatter.build_result()

    print(result)

    discord.send_message(result)
    


if __name__ == "__main__":
    main()