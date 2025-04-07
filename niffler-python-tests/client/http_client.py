from requests import Response
from allure_commons.types import AttachmentType
from requests_toolbelt.utils.dump import dump_response
from allure import attach

from client.session import BaseSession


class HttpClient:

    def __init__(self, base_url, token: str):
        self._session = BaseSession(base_url)  # requests.session()
        self.set_headers({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        # self._session.hooks["response"].append(self.attach_response)

    def set_headers(self, headers):
        self._session.headers.update(headers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    # @staticmethod
    # def attach_response(response: Response, *args, **kwargs):
    #     attachment_name = response.request.method + " " + response.request.url
    #     attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

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
        return self._session.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._session.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self._session.request("PUT", url, **kwargs)

    def patch(self, url, **kwargs):
        return self._session.request("PATCH", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._session.request("DELETE", url, **kwargs)
