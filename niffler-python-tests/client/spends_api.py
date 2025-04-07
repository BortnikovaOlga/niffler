from model.web_spend import Spend
from .http_client import HttpClient
from allure import step


class SpendsApi:

    def __init__(self, base_url: str, token: str):
        self.client = HttpClient(base_url=f"{base_url}/api/spends", token=token)

    @step("http добавить расход")
    def add_spend(self, body: Spend) -> Spend:
        response = self.client.post("/add", data=body.model_dump_json())
        response.raise_for_status()
        return Spend.model_validate(response.json())

    @step("http удалить расход")
    def remove_spends(self, ids: list):
        response = self.client.delete("/remove", params={"ids": ids})
        response.raise_for_status()

    @step("http получить все расходы")
    def get_all_spends(self, **kwargs) -> list[Spend]:
        response = self.client.get("/all", **kwargs)
        response.raise_for_status()
        return [Spend.model_validate(value) for value in response.json()]
        # return TypeAdapter(list[Spend]).validate_python(response.json())

    @step("http получить расход по ид")
    def get_by_id(self, id: str) -> Spend:
        response = self.client.get(f"/{id}")
        response.raise_for_status()
        return Spend.model_validate(response.json())

    @step("http редактировать расход")
    def update(self, update: Spend) -> Spend:
        response = self.client.patch("/edit", data=update.model_dump_json())
        response.raise_for_status()
        return Spend.model_validate(response.json())
