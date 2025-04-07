import base64
import pkce
from client.session import AuthSession
from model.envs import Envs


class OAuthClient:
    """Авториизует по Oauth2.0"""

    session: AuthSession
    base_url: str

    def __init__(self, env: Envs):
        """Генерируем code_verifier и code_challenge. И генерируем basic auth token из секрета сервиса авторизации."""
        self.session = AuthSession(base_url=env.auth_url)
        self.redirect_uri = env.frontend_url + "/authorized"
        # Этот код мы написали самостоялтельно и заменили на целевую схему с использованием бибилотеки
        # self.code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        # self.code_verifier = re.sub('[^a-zA-Z0-9]+', '', self.code_verifier)
        #
        # self.code_challenge = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        # self.code_challenge = base64.urlsafe_b64encode(self.code_challenge).decode('utf-8')
        # self.code_challenge = self.code_challenge.replace('=', '')
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()

        # self._basic_token = base64.b64encode(env.auth_secret.encode('utf-8')).decode('utf-8')
        # self.authorization_basic = {"Authorization": f"Basic {self._basic_token}"}
        self.token = None

    def get_token(self, username, password):
        """Возвраащает token oauth для авторизации пользователя с username и password

        1. Получаем jsessionid и xsrf-token куку в сесссию.
        2. Получаем code из redirec по xsrf-token'у.
        3. Получаем access_token.
        """
        res = self.session.get(
            url="/oauth2/authorize",
            params={
                "response_type": "code",
                "client_id": "client",
                "redirect_uri": self.redirect_uri,
                "code": self.session.code,
                "scope": "openid",
                "code_challenge": self.code_challenge,
                "code_challenge_method": "S256",
                "continue": "",
            },
            allow_redirects=True
        )

        res = self.session.post(
            url=f"/login",
            data={  # padantic
                "username": username,
                "password": password,
                "_csrf": self.session.cookies.get("XSRF-TOKEN")
            },
            allow_redirects=True
        )
        code = self.session.code[0]
        data = {
                   "code": code,
                   "redirect_uri": self.redirect_uri,
                   "code_verifier": self.code_verifier,
                   "grant_type": "authorization_code",
                   "client_id": "client",

               }
        token_response = self.session.post(
            url=f"/oauth2/token",
            data=data
            # headers=self.authorization_basic,
        )

        self.token = token_response.json().get("access_token", None)
        return self.token
