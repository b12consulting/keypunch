from keypunch import KClient


def test_add_realm_and_user():
    base_url = "http://localhost:8080"
    kclient = KClient(base_url=base_url)
    kclient.login("admin", "admin")

    # Create realm
    kclient.endpoint('realms').post(realm="test-realm")

    # Read it back
    res = kclient.endpoint('realms').get()
    assert "test-realm" in [r["realm"] for r in res]

    # Create user
    kclient.endpoint('users', realm="test-realm").post(username="new-user")

    # Read it back
    res = kclient.endpoint('users', realm="test-realm").get()
    assert "new-user" in [u["username"] for u in res]
