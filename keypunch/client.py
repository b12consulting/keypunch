# See keycloak api doc: https://www.keycloak.org/docs-api/21.0.1/rest-api/index.html
# See kecloak-orgs api doc: https://github.com/p2-inc/phasetwo-docs/blob/master/openapi.yaml

import requests

from keypunch.utils import logger

DEFAULT_REALM = "master"


class Endpoint:
    def __init__(self, session, url):
        self.session = session
        self.url = url

    @staticmethod
    def extract(raw_response):
        raw_response.raise_for_status()
        response = raw_response.json() if raw_response.content else {}  # ?
        return response

    def form(self, **data):
        logger.debug("POST (url-encoded): %s", self.url)
        raw_response = self.session.post(self.url, data=data)
        return self.extract(raw_response)

    def post(self, json_payload=None, /, **json):
        logger.debug("POST: %s", self.url)
        raw_response = self.session.post(self.url, json=json)
        return self.extract(raw_response)

    def put(self, json_payload=None, /, **json):
        json = json_payload or json
        logger.debug("PUT: %s (payload: %s)", self.url, json)
        raw_response = self.session.put(self.url, json=json)
        return self.extract(raw_response)

    def delete(self, **params):
        raw_response = self.session.delete(self.url, params=params)
        return self.extract(raw_response)

    def get(self, **params):
        logger.debug("GET: %s", self.url)
        raw_response = self.session.get(self.url, params=params)
        print(raw_response.content)
        return self.extract(raw_response)


class KClient:

    _paths = {
        # Base keycloak
        "token": "/realms/{realm}/protocol/openid-connect/token",
        "realms": "/admin/realms",
        "realm": "/admin/realms/{realm}",
        "user": "/admin/realms/{realm}/users/{user_id}",
        "users": "/admin/realms/{realm}/users",
        "reset-password": "/admin/realms/{realm}/users/{user_id}/reset-password",
        "execute-actions-email": "/admin/realms/{realm}/users/{user_id}/execute-actions-email",
        # Org extension
        "orgs": "/realms/{realm}/orgs",
        "members": "/realms/{realm}/orgs/{org_id}/members",
        "invitations": "/realms/{realm}/orgs/{org_id}/invitations",
    }

    def __init__(self, base_url, realm=DEFAULT_REALM):
        self.base_url = base_url.rstrip("/")
        self.realm = realm
        self.session = requests.Session()
        self.access_token = None

    def login(self, username, password, realm=DEFAULT_REALM):
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
        # attr = {**vars(self), **attr}
        path = self._paths[name]
        url = self.base_url + path.format(**attr)
        return Endpoint(self.session, url)


if __name__ == "__main__":
    from pprint import pprint

    base_url = "http://localhost:8080"
    kcli = KClient(base_url=base_url)

    # Login
    # kcli.login("admin", "admin")

    # # Get master realm info
    # pprint(kcli.endpoint('realm').get())

    # Get app realm info
    # pprint(kcli.endpoint("realm", name="django-seed").get())

    # List realms
    # pprint(kcli.endpoint("realms").get())

    # # Create realm
    # pprint(kcli.endpoint('realms').post(
    #     realm="another-new-realm",
    # ))

    # Delete realms
    # pprint(kcli.endpoint('realm', name="another-new-realm").delete())

    # List users
    # pprint(kcli.endpoint('users', realm="django-seed").get())

    # Create user
    # pprint(kcli.endpoint('users', realm="django-seed").post())

    # List orgs
    # pprint(kcli.endpoint('orgs', realm="django-seed").get())

    # Members
    # pprint(kcli.endpoint('members', realm="django-seed", org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c").get())

    # List Invitations
    pprint(
        kcli.endpoint(
            "invitations",
            realm="django-seed",
            org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
        ).get()
    )

    # Create Invitations
    # pprint(kcli.endpoint(
    #     'invitations',
    #     realm="django-seed",
    #     org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
    # ).post(
    #     email="ham@spam.com",
    #     send=True,
    # ))

    # Get indfo
    # pprint(kcli.endpoint(
    #     'user',
    #     realm="django-seed",
    #     user_id="5db4613c-e740-4617-b86e-6830d2550590", org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
    # ).get())

    # Force user to cycle password (so not a situation were the user
    # has forgot it)
    pprint(
        kcli.endpoint(
            "reset-password",
            realm="django-seed",
            user_id="5db4613c-e740-4617-b86e-6830d2550590",
        ).put(
            temporary=True,
            type="password",
            value="hamspam",
        )
    )

    # Action email with "UPDATE_PASSWORD" payload -> aka forgot password
    pprint(
        kcli.endpoint(
            "execute-actions-email",
            realm="django-seed",
            user_id="5db4613c-e740-4617-b86e-6830d2550590",
        ).put(["UPDATE_PASSWORD"])
    )
