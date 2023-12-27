<h1 align="center">Website</h1>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/ari-lt/ari.lt?color=red&style=flat-square">
  <img src="https://img.shields.io/github/repo-size/ari-lt/ari.lt?color=red&style=flat-square">
  <img src="https://img.shields.io/github/issues/ari-lt/ari.lt?color=red&style=flat-square">
  <img src="https://img.shields.io/github/stars/ari-lt/ari.lt?color=red&style=flat-square">
</p>

<p align="center">
    <a href="https://app.netlify.com/sites/ari-lt/deploys">
        <img alt="Netlify Status" src="https://api.netlify.com/api/v1/badges/d82361d9-c471-41d0-ba9b-b5fbe07ca843/deploy-status" /> </a>
</p>

### [My website's](https://www.ari.lt/) source code.

# Badge

the badge( s ) is licensed under UNLICENSE :

```
UNLICENSE

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
```

## original

author : Ari Archer - [@TruncatedDinosour](https://ari.lt/gh) - <https://ari.lt/> - <ari.web.xyz@gmail.com>

in html :

```html
<a href="https://ari.lt/"> <img src="https://ari.lt/badge.png" loading="lazy" alt="ari-web badge" height="31px" width="88px" /> </a>
```

in markdown :

```md
[![ari-web badge](https://ari.lt/badge.png)](https://ari.lt/)
```

[![ari-web badge](https://ari.lt/badge.png)](https://ari.lt/)

## yellow

author : Tobskep - <https://tobskep.com/>

in html :

```html
<a href="https://ari.lt/"> <img src="https://ari.lt/badge-yellow.png" loading="lazy" alt="ari-web badge" height="31px" width="88px" /> </a>
```

in markdown :

```md
[![ari-web badge](https://ari.lt/badge-yellow.png)](https://ari.lt/)
```

[![ari-web badge](https://ari.lt/badge-yellow.png)](https://ari.lt/)

# Customising when self-hosting

1. Clone the repository: `git clone https://ari.lt/git ari-web`
2. Enter the directory: `cd ari-web`
3. See the `/content/styles/config` and `/content/js/config` directories.
4. Open it in live server: `python3 -m http.server 5500`
5. Go to http://0.0.0.0:5500/ in your browser
6. Edit all stuff that is `ARI-WEB-SPECIFIC` in [netlify.toml](/netlify.toml)
7. Publish on [netlify](https://netlify.com/)

# API hashes

If you want to call to a very expensive API it might become
slow, so there's hashes for them, they are sha256 hashes of
those JSON files in the api

So what you do, replace all `.` in the API name with \_,
then make the request to `/api_hash/..._hash.txt` and you will
get the hash, for example: <https://www.ari.lt/api_hash/apis_json_hash.txt>

# Standard

See [the standard](/STANDARD.md) to see how ari-web is structured and
how to properly modify ari-web

# Usage API

The [usage api](https://www.ari.lt/api/usage.json)
has all the statistics I get from netlify, it serves as
an archive and growth monitor

Schema:

```json
{
    "<YYYY-MM-DD>": {
        "total": <total bandwidth used in MB>,
        "top": {
            "<top usage site 1>": <total bandwidth used in MB>,
            "<top usage site 2>": <total bandwidth used in MB>,
            "<top usage site 3>": <total bandwidth used in MB>
        }
    }
}
```

The date is the day I added those stats, total is total
bandwidth used up to that point, top is the top 3 site's
usage and its keys are the (sub)domain names and the values
of those keys are the used bandwidth out of the total

The bandwidth keys are all floats for easy parsing, they
represent the bandwidth used in MB

The top sites will most likely not have the total bandwidth
fully used, so as a measure you can use this formula to calculate
how much per avg sites are using:

```py
(data["<YYYY-MM-DD>"]["total"] - sum(data["<YYYY-MM-DD>"]["top"].values())) / (len(ari_web_sites) - 3)
```

# Subdomains

-   https://www.ari.lt/ (source: https://ari.lt/git)
-   https://files.ari.lt/ (source: https://files.ari.lt/git)
-   https://blog.ari.lt/ (source: https://blog.ari.lt/git)
-   https://legacy.blog.ari.lt/ (source: https://legacy.blog.ari.lt/git)
-   https://school.ari.lt/ (source: proprietary (I don't want people snooping on my homework lol))
-   https://user.ari.lt/ (source: https://user.ari.lt/git)
-   https://etc.ari.lt/ (source: https://etc.ari.lt/git)
-   https://a.ari.lt/ (source: https://a.ari.lt/git)
