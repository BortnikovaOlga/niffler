import requests
from requests import Response


class HttpClient:

    def __init__(self, token: str):

        self._session = requests.session()
        self.set_headers({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def set_headers(self, headers):
        self._session.headers.update(headers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def request(self, method: str, url: str, **kwargs) -> Response:
        """
        Request method
        method: method for the new Request object: get, OPTIONS, HEAD, POST, PUT, PATCH, or DELETE. # noqa
        url – URL for the new Request object.
        **kwargs:
            params – (optional) Dictionary, list of tuples or bytes to send in the query string for the Request. # noqa
            json – (optional) A JSON serializable Python object to send in the body of the Request. # noqa
            headers – (optional) Dictionary of HTTP Headers to send with the Request.
        """
        return self._session.request(method, url, **kwargs)

    def get(self, url, **kwargs):
        return self._session.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self._session.post(url, **kwargs)

    def put(self, url, **kwargs):
        return self._session.put(url, **kwargs)

    def patch(self, url, **kwargs):
        return self._session.patch(url, **kwargs)

    def delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)
