from .model import ScenariosDict, Scenario, StepDelay, StepRequests, StepRequest

CADDYFILE = """
{
  auto_https disable_redirects
}

(server) {
  log {
    output stdout
    level ERROR
  }

  tls {{ certificates.server_cert }} {{ certificates.server_key }}
  reverse_proxy {{ app.hostname }}:{{ app.port }}
  encode zstd gzip

  header {
    # Enable HTTP Strict Transport Security (HSTS) to force clients to always connect via HTTPS
    Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

    # Enable cross-site filter (XSS) and tell browser to block detected attacks
    X-XSS-Protection "1; mode=block"

    # Prevent some browsers from MIME-sniffing a response away from the declared Content-Type
    X-Content-Type-Options "nosniff"

    # Disallow the site to be rendered within a frame (clickjacking protection)
    X-Frame-Options "SAMEORIGIN"

    # X-Robots-Tag
    X-Robots-Tag "noindex, noarchive, nofollow"

    # CSP
    Content-Security-Policy "default-src 'none'; style-src 'self' 'unsafe-inline'; form-action 'self'; frame-ancestors 'self'; base-uri 'self'; img-src 'self' data:; font-src 'self'; frame-src 'self'"

    # No Cache
    Cache-Control "no-cache, no-store"
    Pragma "no-cache"
  }
}

{% for port in ports %}
https://{{ hostname }}:{{ port }} {
  import server
}
{% endfor %}
"""  # noqa

SCENARIOS = ScenariosDict()

SCENARIOS += Scenario(
    id="external_search",
    name="External requests: Two sequences of searx requests, 0.5s in between",
    tries=10,
    local_ca=False,
    steps=[
        StepRequests(
            urls=[
                "https://fr.wikiversity.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",  # noqa
                "https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=linux%7CLinux&prop=extracts%7Cpageimages%7Cpageprops&ppprop=disambiguation&exintro&explaintext&pithumbsize=300&redirects",  # noqa
                "https://fr.wikiquote.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",  # noqa
                "https://www.wikidata.org/w/index.php?search=linux&ns0=1",
                "https://www.etymonline.com/search?page=1&q=linux",
                "https://api.duckduckgo.com/?q=time&format=json&pretty=0&no_redirect=1&d=1",
            ]
        ),
        StepDelay(time=0.5),
        StepRequests(
            urls=[
                "https://fr.wikiversity.org/w/api.php?action=query&list=search&srsearch=searx&format=json&sroffset=0&srlimit=5&srwhat=text",  # noqa
                "https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=searx%7CLinux&prop=extracts%7Cpageimages%7Cpageprops&ppprop=disambiguation&exintro&explaintext&pithumbsize=300&redirects",  # noqa
                "https://fr.wikiquote.org/w/api.php?action=query&list=search&srsearch=searx&format=json&sroffset=0&srlimit=5&srwhat=text",  # noqa
                "https://www.wikidata.org/w/index.php?search=searx&ns0=1",
                "https://www.etymonline.com/search?page=1&q=searx",
                "https://api.duckduckgo.com/?q=searx&format=json&pretty=0&no_redirect=1&d=1",
            ]
        ),
    ],
)

SCENARIOS += Scenario(
    id="6_2seq_8kb",
    name="Two sequences of 6 requests with a 8KB responses (various delays), 0.5s in between",
    tries=10,
    local_ca=True,
    steps=[
        StepRequests(
            urls=[
                "https://localhost:4001/800/8192",
                "https://localhost:4002/900/8192",
                "https://localhost:4003/400/8192",
                "https://localhost:4004/500/8192",
                "https://localhost:4005/600/8192",
                "https://localhost:4006/300/8192",
            ]
        ),
        StepDelay(time=0.5),
        StepRequests(
            urls=[
                "https://localhost:4001/800/8192",
                "https://localhost:4002/900/8192",
                "https://localhost:4003/600/8192",
                "https://localhost:4004/400/8192",
                "https://localhost:4005/500/8192",
                "https://localhost:4006/400/8192",
            ]
        ),
    ],
)

SCENARIOS += Scenario(
    id="6_2seq_400kb",
    name="Two sequences of 6 requests with a 400KB responses (various delays), 0.5s in between",
    tries=10,
    local_ca=True,
    steps=[
        StepRequests(
            urls=[
                "https://localhost:4001/800/400000",
                "https://localhost:4002/900/400000",
                "https://localhost:4003/400/400000",
                "https://localhost:4004/500/400000",
                "https://localhost:4005/600/400000",
                "https://localhost:4006/300/400000",
            ]
        ),
        StepDelay(time=0.5),
        StepRequests(
            urls=[
                "https://localhost:4001/800/400000",
                "https://localhost:4002/900/400000",
                "https://localhost:4003/600/400000",
                "https://localhost:4004/400/400000",
                "https://localhost:4005/500/400000",
                "https://localhost:4006/400/400000",
            ]
        ),
    ],
)


SCENARIOS += Scenario(
    id="100_2seq_2kb",
    name="Two sequences of 100 parallel requests (various delays), 0.5s in between",
    tries=10,
    local_ca=True,
    steps=[
        StepRequests(
            urls=[
                "https://localhost:4001/800/2048",
                "https://localhost:4002/900/2048",
                "https://localhost:4003/400/2048",
                "https://localhost:4004/500/2048",
                "https://localhost:4005/600/2048",
            ]
            * 20
        ),
        StepDelay(time=0.5),
        StepRequests(
            urls=[
                "https://localhost:4001/800/2048",
                "https://localhost:4002/900/2048",
                "https://localhost:4003/600/2048",
                "https://localhost:4004/400/2048",
                "https://localhost:4005/500/2048",
            ]
            * 20
        ),
    ],
)

SCENARIOS += Scenario(
    id="1_100seq_1",
    name="100 sequential requests, 1 byte response, 0 delay",
    tries=10,
    local_ca=True,
    steps=[StepRequest(url="https://localhost:4001/0/1")] * 100,
)

SCENARIOS += Scenario(
    id="1_100seq_2kb",
    name="100 sequential requests, 2KB response, 0 delay",
    tries=10,
    local_ca=True,
    steps=[StepRequest(url="https://localhost:4001/0/2048")] * 100,
)

SCENARIOS += Scenario(
    id="1_100seq_256kb",
    name="100 sequential requests, 256KB response, 0 delay",
    tries=10,
    local_ca=True,
    steps=[StepRequest(url="https://localhost:4001/0/262144")] * 100,
)

SCENARIOS += Scenario(
    id="1_100seq_1mb",
    name="100 sequential requests, 1MB response, 0 delay",
    tries=10,
    local_ca=True,
    steps=[StepRequest(url="https://localhost:4001/0/1048576")] * 100,
)

SCENARIOS += Scenario(
    id="1_30seq_8kb_400ms",
    name="30 sequential requests, 8KB response, 400ms delay",
    tries=10,
    local_ca=True,
    steps=[StepRequest(url="https://localhost:4001/400/8192")] * 30,
)

SCENARIOS += Scenario(
    id="30_1seq_8kb_400ms",
    name="One sequence of 30 requests, 8KB response, 400ms delay",
    tries=10,
    local_ca=True,
    steps=[StepRequests(urls=["https://localhost:4001/400/8192"] * 30), ],
)
