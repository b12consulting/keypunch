# See keycloak api doc: https://www.keycloak.org/docs-api/21.0.1/rest-api/index.html
# See kecloak-orgs api doc: https://github.com/p2-inc/phasetwo-docs/blob/master/openapi.yaml

import requests

from keypunch.utils import logger

DEFAULT_REALM = "master"


class Endpoint:
    def __init__(self, session, url):
        self.session = session
        self.url = url
        self._data = None
        self._json = None
        self._params = None

    @staticmethod
    def extract(raw_response):
        try:
            raw_response.raise_for_status()
        except Exception as e :
            msg = "Received unexpected status (%s) \n %s \n Server response: %s"
            logger.exception(msg, raw_response.status_code, str(e), raw_response.content)
            raise # Bubble-up

        response = raw_response.json() if raw_response.content else {}  # ?
        return response

    def form(self, **data):
        logger.debug("POST (url-encoded): %s", self.url)
        data = data or self._data
        raw_response = self.session.post(self.url, data=data)
        return self.extract(raw_response)

    def post(self, **json):
        logger.debug("POST: %s", self.url)
        json = json or self._json
        raw_response = self.session.post(self.url, json=json)
        return self.extract(raw_response)

    def put(self, **json):
        logger.debug("PUT: %s (payload: %s)", self.url, json)
        json = json or self._json
        raw_response = self.session.put(self.url, json=json)
        return self.extract(raw_response)

    def delete(self, **params):
        logger.debug("DELETE: %s", self.url)
        params = params or self._params
        raw_response = self.session.delete(self.url, params=params, json=self._json)
        return self.extract(raw_response)

    def delete_with_payload(self, json_payload=None, /, **json):
        json = json_payload or json
        logger.debug("DELETE: %s (payload: %s)", self.url, json)
        raw_response = self.session.request("DELETE", self.url, json=json)
        return self.extract(raw_response)

    def get(self, **params):
        logger.debug("GET: %s", self.url)
        params = params or self._params
        raw_response = self.session.get(self.url, params=params)
        return self.extract(raw_response)

    def json(self, values):
        self._json = values
        return self

    def data(self, values):
        self._data = values
        return self

    def params(self, values):
        self._params = values
        return self


class KClient:
    _paths = {
        # Base keycloak
        "token": "/realms/{realm}/protocol/openid-connect/token",
        "realms": "/admin/realms",
        "realm": "/admin/realms/{realm}",
        "users": "/admin/realms/{realm}/users",
        "user": "/admin/realms/{realm}/users/{user_id}",
        "clients": "/admin/realms/{realm}/clients",
        "reset-password": "/admin/realms/{realm}/users/{user_id}/reset-password",
        "roles": "/admin/realms/{realm}/clients/{client_id}/roles",
        "role-mappings": "/admin/realms/{realm}/users/{user_id}/role-mappings",
        "role-mappings-user-realm": "/admin/realms/{realm}/users/{user_id}/role-mappings/realm",
        "role-mappings-user-client": "/admin/realms/{realm}/users/{user_id}/role-mappings/clients/{client_id}",
        "execute-actions-email": "/admin/realms/{realm}/users/{user_id}/execute-actions-email?lifespan={lifespan}",
        # Org extension
        "orgs": "/realms/{realm}/orgs",
        "org": "/realms/{realm}/orgs/{org_id}",
        "members": "/realms/{realm}/orgs/{org_id}/members",
        "member": "/realms/{realm}/orgs/{org_id}/members/{user_id}",
        "invitations": "/realms/{realm}/orgs/{org_id}/invitations",
        "invitation": "/realms/{realm}/orgs/{org_id}/invitations/{invitation_id}",
        "role-users": "/realms/{realm}/orgs/{org_id}/roles/{role}/users",
        "user-orgs": "/realms/{realm}/users/{user_id}/orgs",
    }

    def __init__(self, base_url, realm=DEFAULT_REALM):
        self.base_url = base_url.rstrip("/")
        self.realm = realm
        self.session = requests.Session()
        self.access_token = None

    def login(self, username, password, realm=None):
        realm = realm or self.realm
        data = {
            "client_id": "admin-cli",
            "username": username,
            "password": password,
            "grant_type": "password",
        }
        resp = self.endpoint("token", realm=realm).form(**data)
        self.access_token = resp["access_token"]
        self.session.headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

    def endpoint(self, name, /, **attr):
        path = self._paths[name]
        url = self.base_url + path.format(**attr)
        return Endpoint(self.session, url)
