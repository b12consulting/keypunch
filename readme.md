
Keypunch is a small client for Keycloak. Its main goal is to automate
some administrative tasks like creating a user or trigger an email.


# Install

Install latest version:

    pip install git+ssh://git@github.com/b12consulting/keypunch


Install a specific version:

    pip install git+ssh://git@github.com/b12consulting/keypunch@2c6496ca519

The revision specified in `@..` can be replaced by a tag or a branch name.


# Examples


``` python
base_url = "http://localhost:8080"
kcli = KClient(base_url=base_url)

# Login
kcli.login("admin", "admin")

# Get master realm info
pprint(kcli.endpoint('realm').get())

# Get app realm info
pprint(kcli.endpoint("realm", name="django-seed").get())

# List realms
pprint(kcli.endpoint("realms").get())

# Create realm
pprint(kcli.endpoint('realms').post(
    realm="another-new-realm",
))

# Delete realms
pprint(kcli.endpoint('realm', name="another-new-realm").delete())

# List users
pprint(kcli.endpoint('users', realm="django-seed").get())

# Create user
pprint(kcli.endpoint('users', realm="django-seed").post())

# List orgs
pprint(kcli.endpoint('orgs', realm="django-seed").get())

# Members
pprint(kcli.endpoint('members', realm="django-seed", org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c").get())

# List Invitations
pprint(
    kcli.endpoint(
        "invitations",
        realm="django-seed",
        org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
    ).get()
)

# Create Invitations
pprint(kcli.endpoint(
    'invitations',
    realm="django-seed",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).post(
    email="ham@spam.com",
    send=True,
))

# Get indfo
pprint(kcli.endpoint(
    'user',
    realm="django-seed",
    user_id="5db4613c-e740-4617-b86e-6830d2550590", org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
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
```
