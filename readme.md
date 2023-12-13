
Keypunch is a small client for Keycloak. Its main goal is to automate
some administrative tasks like creating a user or trigger an email.


# Install

Install latest version:

    pip install git+ssh://git@github.com/b12consulting/keypunch


Install a specific version:

    pip install git+ssh://git@github.com/b12consulting/keypunch@2c6496ca519

The revision specified in `@..` can be replaced by a tag or a branch name.

# Testing

In order to run non-mocked test you will have to start a container:

    docker run --name keypunch_test --rm -p 8080:8080 \
     -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin -e KC_HTTP_RELATIVE_PATH=/ \
     quay.io/phasetwo/phasetwo-keycloak:22.0.5 \
    start-dev --spi-email-template-provider=freemarker-plus-mustache \
     --spi-email-template-freemarker-plus-mustache-enabled=true --spi-theme-cache-themes=false

Install test dependencies


    pip install ".[test]"

Run tests

    pytest tests/


# Examples

``` python
base_url = "http://localhost:8080"
kcli = KClient(base_url=base_url)

# Login
kcli.login("admin", "admin")
```

## Realms

``` python
# Get master realm info
kcli.endpoint('realm').get()

# Get app realm info
kcli.endpoint("realm", name="django-seed").get()

# List realms
kcli.endpoint("realms").get()

# Create realm
kcli.endpoint('realms').post(
    realm="another-new-realm",
)

# Delete realms
kcli.endpoint('realm', name="another-new-realm").delete()
```


## Users

``` python
# List users
kcli.endpoint('users', realm="django-seed").get()

# Create user
kcli.endpoint('users', realm="django-seed").post(username="new-user")
```


## Organisations

``` python
# List orgs
kcli.endpoint('orgs', realm="django-seed").get()

# Members
kcli.endpoint(
    'members',
    realm="django-seed",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).get()

# List Invitations
kcli.endpoint(
    "invitations",
    realm="django-seed",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).get()

# Create Invitations
kcli.endpoint(
    'invitations',
    realm="django-seed",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).post(
    email="ham@spam.com",
    send=True,
)

# Get membership info
kcli.endpoint(
    'user',
    realm="django-seed",
    user_id="5db4613c-e740-4617-b86e-6830d2550590",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).get()
```


## Trigger mails

``` python
# Force user to cycle password (so not a situation were the user
# has forgot it)

kcli.endpoint(
    "reset-password",
    realm="django-seed",
    user_id="5db4613c-e740-4617-b86e-6830d2550590",
).put(
    temporary=True,
    type="password",
    value="hamspam",
)

# Action email with "UPDATE_PASSWORD" payload -> aka forgot password
kcli.endpoint(
    "execute-actions-email",
    realm="django-seed",
    user_id="5db4613c-e740-4617-b86e-6830d2550590",
).put(["UPDATE_PASSWORD"])

```
