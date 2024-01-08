from keypunch.client import Endpoint


def test_login(kclient):
    kclient.login("admin", "admin")
    Endpoint.form.assert_called_once_with(
        client_id="admin-cli",
        username="admin",
        password="admin",
        grant_type="password",
    )


def test_get_realm_info(kclient):
    ep = kclient.endpoint("realm", realm="test-realm")
    ep.get()
    assert ep.url == "http://localhost:8080/admin/realms/test-realm"
    Endpoint.get.assert_called_once_with()


def test_get_other_realm(kclient):
    ep = kclient.endpoint(
        "execute-actions-email",
        realm="test-realm",
        user_id="5db4613c-e740-4617-b86e-6830d2550590",
    )
    ep.put(["UPDATE_PASSWORD"])
    assert (
        ep.url
        == "http://localhost:8080/admin/realms/test-realm/users/5db4613c-e740-4617-b86e-6830d2550590/execute-actions-email"
    )
    Endpoint.put.assert_called_once_with(["UPDATE_PASSWORD"])


def test_create_realm(kclient):
    kclient.endpoint("realms").post(
        realm="another-new-realm",
    )
    Endpoint.post.assert_called_once_with(
        realm="another-new-realm",
    )
