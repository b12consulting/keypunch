
Keypunch is a small client for Keycloak. Its main goal is to automate
some administrative tasks like creating a user or trigger an email.


# Install

Install latest version:

    pip install git+ssh://git@github.com/b12consulting/keypunch


Install a specific version:

    pip install git+ssh://git@github.com/b12consulting/keypunch@2c6496ca519

The revision specified in `@..` can be replaced by a tag or a branch name.


# Usage

## Client & endpoint

The first thing to do once a client instance is created is to log in:

``` python
from keypunch import KClient

base_url = "http://localhost:8080"
kcli = KClient(base_url=base_url)

# Login
kcli.login("admin", "admin")
```

The `kcli` object holds a requests session that manages the cookies,
session refresh is not implemented so queries can fail after a few
minutes (depending on your Keycloak settings).


The `KClient` class main job is to instanciate an `Endpoint` object
based on a known path. For example in order to instanciate an
endpoint for the "my-new-realm" realm we use the `endpoint` method
that take as first argument the name of the endpoint and any extra
argument needed to format the route:

``` python
ep = kcli.endpoint("realm", realm="my-new-realm")
print(ep.url)  #'http://localhost:8080/admin/realms/my-new-realm'
```

We can then trigger the actual query with either `post`, `get`,
`delete`, `put` or `form` (form is like post but with
"application/x-www-form-urlencoded" instead of the default
"application/json"):

``` python
realm_info = ep.get()
```

To create a new realm (note that we use the "realms" endpoint this
time):

``` python
ep = kcli.endpoint("realms")
ep.post(realm="another-new-realm")
```

In the example above the json payload `{"realm":"another-new-realm"}`
will be sent in the request body.

For GET queries, the method argument will be used as query parameters, so this:

``` python
kcli.endpoint("clients", realm="master").get(max=1)
```

Will query this url: `http://localhost:8080/admin/realms/master/clients?max=1`



## API support

The `_paths` attribute contains some pre-defined endpoints:

``` python
>>> pprint(KClient._paths)
{
 ...
 'realm': '/admin/realms/{realm}',
 ...
}
 ```


Only a few API endpoint are supported and are added in opportunistic
fashion. You can easily add extra endpoints by updating the
`KClient._paths` dictionary, like this:

``` python
KClient._paths.update({
    "roles": "/admin/{realm}/clients/{id}/roles",
    "client-scopes": "/admin//{realm}/client-scopes/{id}/scope-mappings/clients/{client}",
    })
```


Keycloak API is documented here:
https://www.keycloak.org/docs-api/21.0.1/rest-api/index.html,
Kecloak-orgs OpenAPI document:
https://github.com/p2-inc/phasetwo-docs/blob/master/openapi.yaml


## Logging

Enable logging
```
from keypunch.utils import logger
logger.setLevel("DEBUG")
```

Alternatively you can set the environment variable:

``` sh
export KEYPUNCH_DEBUG=1
```


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

## Realms

``` python
# Get master realm info
kcli.endpoint('realm').get()

# Get app realm info
kcli.endpoint("realm", realm="my-new-realm").get()

# List realms
kcli.endpoint("realms").get()

# Create realm
kcli.endpoint('realms').post(
    realm="another-new-realm",
)

# Delete realms
kcli.endpoint('realm', realm="another-new-realm").delete()
```


## Users

``` python
# List users
kcli.endpoint('users', realm="my-new-realm").get()

# Create user
kcli.endpoint('users', realm="my-new-realm").post(username="new-user")
```


## Organisations

``` python
# List orgs
kcli.endpoint('orgs', realm="my-new-realm").get()

# Members
kcli.endpoint(
    'members',
    realm="my-new-realm",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).get()

# List Invitations
kcli.endpoint(
    "invitations",
    realm="my-new-realm",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).get()

# Create Invitations
kcli.endpoint(
    'invitations',
    realm="my-new-realm",
    org_id="c501122a-e007-46d0-b620-cdcc2aa13f4c",
).post(
    email="ham@spam.com",
    send=True,
)

# Get membership info
kcli.endpoint(
    'user',
    realm="my-new-realm",
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
    realm="my-new-realm",
    user_id="5db4613c-e740-4617-b86e-6830d2550590",
).put(
    temporary=True,
    type="password",
    value="hamspam",
)

# Action email with "UPDATE_PASSWORD" payload -> aka forgot password
kcli.endpoint(
    "execute-actions-email",
    realm="my-new-realm",
    user_id="5db4613c-e740-4617-b86e-6830d2550590",
).put(["UPDATE_PASSWORD"])

```
