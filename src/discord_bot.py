import requests

class DiscordWebhookClient:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, message):
        payload = {
            "content": message
        }

        response = requests.post(
            url=self.webhook_url,
            json=payload,
            timeout=10
        )

        response.raise_for_status()