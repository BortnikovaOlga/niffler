from urllib.parse import urljoin
from .http_client import HttpClient


class SpendsApi:
    url: str

    def __init__(self, base_url: str, token: str):
        # self.url = urljoin(base_url, "/api/spends")
        self.url = f"{base_url}/api/spends"
        self.client = HttpClient(token)

    def add_spends(self, body):
        url = f"{self.url}/add"
        response = self.client.post(url, json=body)
        response.raise_for_status()
        return response.json()

    def remove_spends(self, ids: list[int]):
        url = urljoin(self.url, "/remove")
        response = self.client.delete(url, params={"ids": ids})
        response.raise_for_status()
