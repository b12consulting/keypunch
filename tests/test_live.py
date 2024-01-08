from keypunch import KClient


def test_invite_user():
    base_url = "http://localhost:8080"
    kclient = KClient(base_url=base_url)
    kclient.login("admin", "admin")

    # List realms
    realms = kclient.endpoint('realms').get()
    test_realm = [r for r in realms if r["realm"] == "test-realm"]
    if test_realm:
        # Delete realm
        kclient.endpoint('realm', realm="test-realm").delete()

    # Create realm
    kclient.endpoint('realms').post(realm="test-realm")

    # Read it back
    res = kclient.endpoint('realms').get()
    assert "test-realm" in [r["realm"] for r in res]

    # Create user
    kclient.endpoint('users', realm="test-realm").post(
        username="new-user",
        email="new-user@example.com",
    )

    # Read it back
    res = kclient.endpoint('users', realm="test-realm").get()
    assert "new-user" in [u["username"] for u in res]

    # List orgs
    orgs = kclient.endpoint("orgs", realm="test-realm").get()
    test_org = [o for o in orgs if o["name"] == "test-org"]
    if test_org:
        org_id = test_org[0]["id"]
        # Delete test org
        kclient.endpoint('org', org_id=org_id).delete()

    # Create test org
    kclient.endpoint('orgs', realm="test-realm").post(name="test-org")
    orgs = kclient.endpoint("orgs", realm="test-realm").get()
    org_id, =  [o["id"] for o in orgs if o["name"] == "test-org"]

    # List invitations
    invitations = kclient.endpoint(
        'invitations',
        realm="test-realm",
        org_id=org_id,
    ).get()

    # Delete pending invitation
    for invitation in invitations:
        kclient.endpoint(
            'invitation',
            realm="test-realm",
            org_id=org_id,
            invitation=invitation["id"],
        ).delete()

    # Create invitation
    kclient.endpoint(
        'invitations',
        realm="test-realm",
        org_id=org_id,
    ).post(email="new-user@example.com", send=True)

    # List invitations
    res = kclient.endpoint(
        'invitations',
        realm="test-realm",
        org_id=org_id,
    ).get()
    invitation = [u for u in res if u["email"] == "new-user@example.com"]
    assert invitation

    # Delete it
    kclient.endpoint(
            'invitation',
        realm="test-realm",
        org_id=org_id,
        invitation_id=invitation[0]["id"],
    ).delete()
