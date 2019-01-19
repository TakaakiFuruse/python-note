import asyncio
import logging
import re
import sys
import urllib.parse
import urllib.rror
from typing import IO

import aiohttp
from aiohttp import ClientSession

import aioiles

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disables = True

HREF_RE = re.compile(r'href="(.*?)"')


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got reponse [%s] for URL : %s", resp.status, url)
    html = await resp.text()

    return html


async def parse(url: str, sesion: ClinentSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()

    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found
    else:
        for link in HREF_RE.findall(html):
            try:
            	abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
            	logger.exception("ERROR PARSING URL: %s", link)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        return found

async def write_one(file: IO, url: str, **kwargs) -> None:
      	res = await parse(url=url, **kwargs)
        if not res:
            return None
        async with aiofiles.open(file, "a") as f:
            for p in res:
                await f.write(f"{url}\t{p}\n")
            logger.info("wrote results for source url: %s", url)

async def bulk_crawl_and_write(file: IO, urls: set, **kwars) -> None:
    async with ClientSession as session:
        tasks = []
        for url  in urls:
            tasks.append
