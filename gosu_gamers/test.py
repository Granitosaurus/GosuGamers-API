import asyncio
import aiohttp
import requests

urls = [
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/?new',
    'http://www.gosugamers.net/dota2/events',
    'http://www.gosugamers.net/dota2/events',
    'http://www.gosugamers.net/dota2/gosubet',
    'http://www.gosugamers.net/dota2/gosubet',
    'http://www.gosugamers.net/dota2/rankings'
    'http://www.gosugamers.net/dota2/rankings'
]


def get_body(url):
    response = yield from aiohttp.request('GET', url)
    body = yield from response.read()
    print(body)


def main():
    response = yield from aiohttp.request('GET', 'http://python.org')
    body = yield from response.read()
    print(body)


def async():
    for url in urls:
        asyncio.get_event_loop().run_until_complete(get_body(url))


def normal():
    for url in urls:
        print(requests.get(url))


if __name__ == '__main__':
    normal()