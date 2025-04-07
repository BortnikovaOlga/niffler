from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    gateway_url: str
    db_engine: str
    auth_url: str
    auth_secret: str
    test_username: str
    test_password: str

    # spend_db_url: str
