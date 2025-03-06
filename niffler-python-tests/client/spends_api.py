from urllib.parse import urljoin

from model.web_spend import Spend
from .http_client import HttpClient


class SpendsApi:
    url: str

    def __init__(self, base_url: str, token: str):
        # self.url = urljoin(base_url, "/api/spends")
        self.url = f"{base_url}/api/spends"
        self.client = HttpClient(token)

    def add_spends(self, body: Spend) -> Spend:
        url = f"{self.url}/add"
        response = self.client.post(url, data=body.model_dump_json())  # response = self.client.post(url, json=body)
        response.raise_for_status()
        return Spend.model_validate(response.json())

    def remove_spends(self, ids: list[int]):
        url = f"{self.url}/remove"
        response = self.client.delete(url, params={"ids": ids})
        response.raise_for_status()
