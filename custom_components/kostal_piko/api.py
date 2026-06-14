"""HTTP client for the Kostal PIKO inverter web page.

Replaces KostalClient.cs / KostalClientResult.cs from the C# project.
Uses Home Assistant's shared aiohttp session.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import aiohttp
import async_timeout

from .const import PAGE_PATH, REQUEST_TIMEOUT


@dataclass
class KostalClientResult:
    """Result of a page fetch (mirrors KostalClientResult.cs)."""

    page: str
    download_time_ms: int
    status_code: int
    is_success: bool


class KostalAuthError(Exception):
    """Raised when the inverter rejects the credentials (HTTP 401)."""


class KostalConnectionError(Exception):
    """Raised when the inverter cannot be reached."""


class KostalClient:
    """Reads the inverter status page over HTTP Basic Auth."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        host: str,
        username: str,
        password: str,
    ) -> None:
        self._session = session
        self._host = host.rstrip("/")
        self._url = f"http://{self._host}{PAGE_PATH}"
        self._auth = aiohttp.BasicAuth(username, password or "")

    @property
    def url(self) -> str:
        """Return the full status page URL."""
        return self._url

    async def read_page(self) -> KostalClientResult:
        """Fetch the inverter HTML page.

        Raises KostalAuthError on 401 and KostalConnectionError on network
        problems; otherwise returns the result (including non-2xx statuses).
        """
        before = time.monotonic()
        try:
            async with async_timeout.timeout(REQUEST_TIMEOUT.total_seconds()):
                async with self._session.get(self._url, auth=self._auth) as response:
                    page = await response.text()
                    status = response.status
        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                raise KostalAuthError("invalid credentials") from err
            raise KostalConnectionError(str(err)) from err
        except (aiohttp.ClientError, TimeoutError) as err:
            raise KostalConnectionError(str(err)) from err

        if status == 401:
            raise KostalAuthError("invalid credentials")

        download_ms = int((time.monotonic() - before) * 1000)
        return KostalClientResult(
            page=page,
            download_time_ms=download_ms,
            status_code=status,
            is_success=200 <= status < 300,
        )
