EXTERNAL = {
    "name": "Real searx requests",
    "tries": 20,
    "cafile": None,
    "url1": [
        "https://fr.wikiversity.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",
        "https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=linux%7CLinux&prop=extracts%7Cpageimages%7Cpageprops&ppprop=disambiguation&exintro&explaintext&pithumbsize=300&redirects",
        "https://fr.wikiquote.org/w/api.php?action=query&list=search&srsearch=linux&format=json&sroffset=0&srlimit=5&srwhat=text",
        "https://www.wikidata.org/w/index.php?search=linux&ns0=1",
        "https://www.etymonline.com/search?page=1&q=linux",
        "https://api.duckduckgo.com/?q=time&format=json&pretty=0&no_redirect=1&d=1"
    ],
    "delay_in_between": 0.5,
    "url2": [
        "https://fr.wikiversity.org/w/api.php?action=query&list=search&srsearch=searx&format=json&sroffset=0&srlimit=5&srwhat=text",
        "https://fr.wikipedia.org/w/api.php?action=query&format=json&titles=searx%7CLinux&prop=extracts%7Cpageimages%7Cpageprops&ppprop=disambiguation&exintro&explaintext&pithumbsize=300&redirects",
        "https://fr.wikiquote.org/w/api.php?action=query&list=search&srsearch=searx&format=json&sroffset=0&srlimit=5&srwhat=text",
        "https://www.wikidata.org/w/index.php?search=searx&ns0=1",
        "https://www.etymonline.com/search?page=1&q=searx",
        "https://api.duckduckgo.com/?q=searx&format=json&pretty=0&no_redirect=1&d=1"
    ]
}

LOCALHOST = {
    "name": "Localhost, 8KB responses",
    "tries": 10,
    "cafile": "server/server.crt",
    "url1": [
        "https://localhost:4001/800/8192",
        "https://localhost:4002/900/8192",
        "https://localhost:4003/400/8192",
        "https://localhost:4004/500/8192",
        "https://localhost:4005/600/8192",
        "https://localhost:4006/300/8192",
    ],
    "delay_in_between": 0.5,
    "url2": [
        "https://localhost:4001/800/8192",
        "https://localhost:4002/900/8192",
        "https://localhost:4003/600/8192",
        "https://localhost:4004/400/8192",
        "https://localhost:4005/500/8192",
        "https://localhost:4006/400/8192",
    ]
}

LOCALHOST2 = {
    "name": "Localhost, 400KB responses",
    "tries": 10,
    "cafile": "server/server.crt",
    "url1": [
        "https://localhost:4001/800/400000",
        "https://localhost:4002/900/400000",
        "https://localhost:4003/400/400000",
        "https://localhost:4004/500/400000",
        "https://localhost:4005/600/400000",
        "https://localhost:4006/300/400000",
    ],
    "delay_in_between": 0.5,
    "url2": [
        "https://localhost:4001/800/400000",
        "https://localhost:4002/900/400000",
        "https://localhost:4003/600/400000",
        "https://localhost:4004/400/400000",
        "https://localhost:4005/500/400000",
        "https://localhost:4006/400/400000",
    ]
}

LOCALHOST3 = {
    "name": "Localhost, 100 requests at the same time",
    "tries": 10,
    "cafile": "server/server.crt",
    "url1": [
        "https://localhost:4001/800/2048",
        "https://localhost:4002/900/2048",
        "https://localhost:4003/400/2048",
        "https://localhost:4004/500/2048",
        "https://localhost:4005/600/2048",
    ] * 20,
    "delay_in_between": 0.5,
    "url2": [
        "https://localhost:4001/800/2048",
        "https://localhost:4002/900/2048",
        "https://localhost:4003/600/2048",
        "https://localhost:4004/400/2048",
        "https://localhost:4005/500/2048",
    ] * 20
}
