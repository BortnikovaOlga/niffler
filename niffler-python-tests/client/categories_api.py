from urllib.parse import urljoin
from .http_client import HttpClient


class CategoriesApi:
    url: str

    def __init__(self, base_url: str, token: str):
        # self.url = urljoin(base_url, "/api/categories")
        self.url = f"{base_url}/api/categories"
        self.client = HttpClient(token)

    def get_categories(self):
        response = self.client.get(f"{self.url}/all")
        response.raise_for_status()
        return response.json()

    def add_category(self, name: str):
        response = self.client.post(f"{self.url}/add", json={"name": name})
        response.raise_for_status()
        return response.json()
