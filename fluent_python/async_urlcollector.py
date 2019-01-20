import asyncio
import re
import sys
import urllib.error
import urllib.parse
from typing import IO

import aiofiles
import aiohttp
from aiohttp import ClientSession

"""
===aiohttp example===

import aiohttp
import asyncio

async def fetch(client):
    async with client.get('http://python.org') as resp:
        assert resp.status == 200
        return await resp.text()

async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
"""


HREF_RE = re.compile(r'href="(.*?)"')

URLS = [
    "https://www.google.com/search?num=100&q=cat",
    "https://search.yahoo.com/search?p=cat",
    "https://duckduckgo.com/?q=cat&t=h_&ia=web",
    "https://duckduckgo.com/?q=dog&t=h_&ia=web",
    "https://www.google.com/search?num=100&q=dog",
    "https://search.yahoo.com/search?p=dog",
]


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    print(f"Got response [{resp.status}] for URL: {url}")
    html = await resp.text()
    return html


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()
    html = await fetch_html(url=url, session=session, **kwargs)
    for link in HREF_RE.findall(html):
        try:
            abslink = urllib.parse.urljoin(url, link)
        except (urllib.error.URLError, ValueError):
            print(f"Error parsing URL: {link}")
            pass
        else:
            found.add(abslink)
    print(f"Found {len(found)} links for {url}")
    return found


async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, **kwargs)

    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        print(f"Wrote results for source URL: {url}")


async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    import pathlib
    import sys

    here = pathlib.Path(__file__).parent
    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=URLS))
