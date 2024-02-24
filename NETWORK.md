# The network protocol

The network protocol consists of 2 different files:

-   `.well-known/network/server.json` - defines the server information
-   `.well-known/network/services.json` - defines the services information

All the servers and services must support HTTPS.

## Server

The server file, `.well-known/network/server.json`, has the following structure:

```json
{
    "server": "62.171.174.136",
    "domain": "ari.lt",
    "description": "Ari-web server",
    "keywords": [
        "ari-web",
        "selfhosted",
        "email",
        "messaging",
        "webapps",
        "hosting"
    ],
    "staff": [
        {
            "name": "Ari Archer",
            "email": "ari@ari.lt",
            "website": "https://ari.lt/",
            "role": "owner",
            "matrix": "@ari:ari.lt",
            "xmpp": "ari@ari.lt",
            "of": ["*"]
        },
        {
            "name": "Sininenkissa",
            "email": "sininenkissa@ari.lt",
            "role": "admin",
            "matrix": "@sininenkissa:ari.lt",
            "xmpp": "sininenkissa@ari.lt",
            "of": ["*"]
        }
    ],
    "name": "Ari::web -> Server",
    "privacy": "https://ari.lt/privacy",
    "terms": "https://ari.lt/tos",
    "affiliated-with": ["pain.agency", "h2.gay"],
    "hardware": {
        "ram": 16,
        "cpu": 6,
        "storage": 400,
        "network": 0.8
    }
}

```

(This is an example)

And this is what the fields mean:

\*required

-   \*`server`: The server domain or IP address, a domain (or IP) that directly points to your server.
-   \*`domain`: The representative domain of the server, does not have to run on the same server as `server`.
-   \*`description`: The description of your server, usually small, up to 1024 characters.
-   \*`keywords`: The keywords of your server. This is used for categorization and discovery of your server in the network. Up to 32 tags, of up to 32 characters each.
-   \*`staff`: A list of staff contacts. See required entries below.
    -   `name`: The name of the staff member, may repeat to add alternative accounts.
    -   `email`: The email of the staff member.
    -   `role`: The role of the staff member, usually:
        -   `owner`
        -   `admin`
        -   `mod`
        -   `audit` (person who may review code, configurations, etc. from time to time)
    -   `of`: The list of services that this staff member _may_ manage. Globbing supported (such as `*.ari.lt`).
    -   Other keys will be listed as-is.
-   \*`name`: The name of your server, any string up to 128 characters.
-   `privacy`: General privacy statement of your server, such as logging,
-   `terms`: General privacy statement of your server, such as logging,
-   \*`affiliated-with`: The affiliated servers in your network. Your server won't be able to talk to other servers not listed in the this list.
-   \*`hardware`: The hardware of your server, in gigabytes
    -   `ram`: The memory/RAM your server has in total, excluding swap.
    -   `cpu`: The CPU threads on your server.
    -   `storage`: The total storage your server has.
    -   `network`: The network speed in GBit/s. (for example 0.8 is 800 mbit/s)

That is all for the server configuration

This file should be served with the following HTTP headers:

-   `Access-Control-Allow-Origin` = `*`
-   `Access-Control-Allow-Methods` = `GET`
-   `Content-Type` = `application/json`

## Services

The services configuration, `.well-known/network/server.json`, has the following structure:

```json
{
    "matrix.ari.lt": {
        "source": "https://matrix.ari.lt/git",
        "description": "The ari.lt Matrix homeserver using Dendrite",
        "license": "MIT",
        "public": false,
        "extra": "Required to contact admin for signup",
        "keywords": ["ari-web", "matrix", "messaging", "im", "dendrite"],
        "privacy": "https://ari.lt/matrix",
        "terms": "https://ari.lt/matrix"
    },
    ...
}
```

(This is an example)

This is what those fields mean:

\*required

-   The keys of the object are the domain names used for the service hosting.
-   `source`: The source code/configuration/etc. of your service.
-   \*`description`: The description of your service. Up to 1024 characters.
-   `license`: The license of your `source` or content on the page. Up to 128 characters.
-   \*`public`: Whether or not any random passer-by can sign up and use this service without any extra steps.
-   `extra`: Any extra information about the service. Up to 512 characters.
-   \*`keywords`: The keywords for your service, used for discovery and categorization. Up to 32 tags, of up to 32 characters each.
-   `privacy`: Privacy statement of your service.
-   `terms`: Terms of your service.

You may add as many services as you want.

This file should be served with the following HTTP headers:

-   `Access-Control-Allow-Origin` = `*`
-   `Access-Control-Allow-Methods` = `GET`
-   `Content-Type` = `application/json`
