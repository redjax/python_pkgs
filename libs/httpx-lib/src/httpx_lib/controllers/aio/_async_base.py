import typing as t
import logging
from pathlib import Path

import httpx
import hishel


class AsyncHttpxControllerBase:
    def __init__(
        self,
        use_cache: bool = False,
        force_cache: bool = False,
        cache_ttl: int = 900,
        check_ttl_every: float = 60,
        ## "sqlite", "file", "redis"
        cache_type: str = "sqlite",
        base_url: str = "",
        params: dict[str, str | list[str]] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        auth: t.Any = None,
        timeout: float | httpx.Timeout | None = None,
        follow_redirects: bool = False,
        limits: httpx.Limits | None = None,
        max_redirects: int = 20,
        event_hooks: dict[str, t.List[t.Callable]] | None = None,
        app: t.Any = None,
        trust_env: bool = True,
        verify: bool | str | None = True,
        cert: str | tuple[str, str] | None = None,
        http2: bool = False,
        proxies: dict[str, str] | str | None = None,
        transport: t.Any = None,
        local_address: str | None = None,
        uds: str | None = None,
        network_backend: t.Any = None,
        cache_db_path: str = ".cache/hishel/cache.db",
        cache_file_dir: str = ".cache/hishel/cache_files",
        cache_redis_host: str = "localhost",
        cache_redis_port: int = 6379,
        cache_redis_db: int = 0,
        cache_redis_password: str | None = None,
        cacheable_methods: list[str] = ["GET"],
        cacheable_status_codes: list[int] = [200, 201, 202, 301, 302, 308],
    ):
        self.use_cache = use_cache
        self.force_cache = force_cache
        self.cache_ttl = cache_ttl
        self.check_ttl_every = check_ttl_every
        self.cache_type = cache_type
        self.cacheable_methods = cacheable_methods
        self.cacheable_status_codes = cacheable_status_codes
        
        self.cache_db_path = cache_db_path
        self.cache_file_dir = cache_file_dir
        self.cache_redis_host = cache_redis_host
        self.cache_redis_port = cache_redis_port
        self.cache_redis_db = cache_redis_db
        self.cache_redis_password = cache_redis_password
        
        self._client_params = dict(
            base_url=base_url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            timeout=timeout,
            follow_redirects=follow_redirects,
            limits=limits,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            app=app,
            trust_env=trust_env,
            verify=verify,
            cert=cert,
            http2=http2,
            proxies=proxies,
            transport=transport,
            local_address=local_address,
            uds=uds,
            network_backend=network_backend,
        )
        
        client_args = {
            k: v for k, v in self._client_params.items() if v is not None and v != ""
        }

        if self.use_cache:
            self.client = hishel.AsyncCacheClient(**client_args)
        else:
            self.client = httpx.AsyncClient(**client_args)

        ## Disable class logging until I have a good way to do it asynchronously
        # self.log = logging.getLogger(__name__)

    async def __aenter__(self):
        await self._ensure_client()

        self._entered = True

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.client:
            await self.client.aclose()
            self.client = None

        self._entered = False

        return exc_value is None

    async def _ensure_client(self):
        if self.client is not None:
            return

        client_args = {
            k: v for k, v in self._client_params.items() if v is not None and v != ""
        }

        if self.use_cache:
            transport = await self._get_async_cache_transport()
            client_args["transport"] = transport

        self.client = httpx.AsyncClient(**client_args)

    async def _get_async_cache_storage(self):
        if self.cache_type == "sqlite":
            try:
                import aiosqlite
            except ImportError:
                raise ImportError("aiosqlite is required for sqlite async cache. Please install it.")

            Path(self.cache_db_path).parent.mkdir(parents=True, exist_ok=True)

            conn = await aiosqlite.connect(self.cache_db_path)

            return hishel.AsyncSQLiteStorage(connection=conn, ttl=self.cache_ttl)
        elif self.cache_type == "file":
            Path(self.cache_file_dir).mkdir(parents=True, exist_ok=True)

            return hishel.AsyncFileStorage(
                base_path=self.cache_file_dir,
                ttl=self.cache_ttl,
                check_ttl_every=self.check_ttl_every,
            )
        elif self.cache_type == "redis":
            try:
                import redis.asyncio as aioredis
            except ImportError:
                raise ImportError("redis is required for redis async cache. Please install it.")

            redis_client = aioredis.Redis(
                host=self.cache_redis_host,
                port=self.cache_redis_port,
                db=self.cache_redis_db,
                password=self.cache_redis_password,
            )

            return hishel.AsyncRedisStorage(
                client=redis_client,
                ttl=self.cache_ttl
            )
        else:
            raise ValueError(f"Unknown cache_type: {self.cache_type}")

    def _get_cache_controller(self):
        return hishel.Controller(
            force_cache=self.force_cache,
            cacheable_methods=self.cacheable_methods,
            cacheable_status_codes=self.cacheable_status_codes,
            allow_heuristics=True,
            allow_stale=False,
        )

    async def _get_async_cache_transport(self):
        storage = await self._get_async_cache_storage()
        
        controller = self._get_cache_controller()
        
        return hishel.AsyncCacheTransport(
            transport=httpx.AsyncHTTPTransport(),
            storage=storage,
            controller=controller,
        )

    def build_request(
        self,
        method: str = "GET",
        url: str = "",
        params: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
        content: bytes | None = None,
        data: dict | None = None,
        files: dict[str, t.Any] | None = None,
        json: t.Any | None = None,
        stream: t.Any | None = None,
        extensions: dict[str, t.Any] | None = None,
    ) -> httpx.Request:
        # self.log.debug(f"Method: {method}, URL: {url}")
        merged_headers = (self._client_params.get("headers") or {}).copy()
        if headers:
            merged_headers.update(headers)

        merged_params = (self._client_params.get("params") or {}).copy()
        if params:
            merged_params.update(params)

        merged_cookies = (self._client_params.get("cookies") or {}).copy()
        if cookies:
            merged_cookies.update(cookies)

        _content = (
            content if content is not None else self._client_params.get("content")
        )
        _data = data if data is not None else self._client_params.get("data")
        _files = files if files is not None else self._client_params.get("files")
        _json = json if json is not None else self._client_params.get("json")
        _extensions = (
            extensions
            if extensions is not None
            else self._client_params.get("extensions")
        )

        request: httpx.Request = httpx.Request(
            method=method,
            url=url,
            params=merged_params,
            headers=merged_headers,
            cookies=merged_cookies,
            content=_content,
            data=_data,
            files=_files,
            json=_json,
            stream=stream,
            extensions=_extensions,
        )
        return request

    async def send(
        self,
        request: httpx.Request,
        stream: bool = False,
        auth: t.Tuple[str, str] | t.Callable[..., t.Any] | object | None = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        await self._ensure_client()

        try:
            res: httpx.Response = await self.client.send(
                request, stream=stream, auth=auth, follow_redirects=follow_redirects
            )
            res.raise_for_status()
            return res
        except httpx.ConnectError:
            # self.log.error(f"Connection error: {e}")
            raise
        except httpx.ConnectTimeout:
            # self.log.error(f"Connection timeout: {e}")
            raise
        except httpx.CookieConflict:
            # self.log.error(f"Cookie conflict: {ce}")
            raise
        except httpx.HTTPError:
            # self.log.error(f"HTTP error: {e}")
            raise
        except httpx.RequestError:
            # self.log.error(f"Request error: {e}")
            raise
        except httpx.TooManyRedirects:
            # self.log.error(f"Too many redirects: {e}")
            raise
        except httpx.InvalidURL:
            # self.log.error(f"URL invalid: {e}")
            raise
        except httpx.UnsupportedProtocol:
            # self.log.error(f"Unsupported protocol: {e}")
            raise
        except httpx.ReadTimeout:
            # self.log.error(f"Read timeout: {e}")
            raise
        except Exception:
            raise

    async def get(
        self,
        url: str = "",
        params: dict | None = {},
        headers: dict | None = {},
        cookies: dict | None = [],
        content: bytes | None = None,
        data: dict | None = {},
        files: dict[str, t.Any] | None = {},
        json: t.Any | None = None,
        stream: t.Any | None = None,
        extensions: dict[str, t.Any] | None = {},
    ):
        await self._ensure_client()

        req: httpx.Request = self.build_request(
            method="GET",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            stream=stream,
            extensions=extensions,
        )

        return await self.send(req)

    async def post(
        self,
        url: str = "",
        params: dict | None = {},
        headers: dict | None = {},
        cookies: dict | None = [],
        content: bytes | None = None,
        data: dict | None = {},
        files: dict[str, t.Any] | None = {},
        json: t.Any | None = None,
        stream: t.Any | None = None,
        extensions: dict[str, t.Any] | None = {},
    ):
        await self._ensure_client()

        req: httpx.Request = self.build_request(
            method="POST",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            stream=stream,
            extensions=extensions,
        )

        return await self.send(req)

    async def patch(
        self,
        url: str = "",
        params: dict | None = {},
        headers: dict | None = {},
        cookies: dict | None = [],
        content: bytes | None = None,
        data: dict | None = {},
        files: dict[str, t.Any] | None = {},
        json: t.Any | None = None,
        stream: t.Any | None = None,
        extensions: dict[str, t.Any] | None = {},
    ):
        await self._ensure_client()

        req: httpx.Request = self.build_request(
            method="PATCH",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            stream=stream,
            extensions=extensions,
        )

        return await self.send(req)

    async def delete(
        self,
        url: str = "",
        params: dict | None = {},
        headers: dict | None = {},
        cookies: dict | None = [],
        content: bytes | None = None,
        data: dict | None = {},
        files: dict[str, t.Any] | None = {},
        json: t.Any | None = None,
        stream: t.Any | None = None,
        extensions: dict[str, t.Any] | None = {},
    ):
        await self._ensure_client()

        req: httpx.Request = self.build_request(
            method="DELETE",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            stream=stream,
            extensions=extensions,
        )

        return await self.send(req)

    async def head(
        self,
        url: str = "",
        params: dict | None = {},
        headers: dict | None = {},
        cookies: dict | None = [],
        content: bytes | None = None,
        data: dict | None = {},
        files: dict[str, t.Any] | None = {},
        json: t.Any | None = None,
        stream: t.Any | None = None,
        extensions: dict[str, t.Any] | None = {},
    ):
        await self._ensure_client()

        req: httpx.Request = self.build_request(
            method="HEAD",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            stream=stream,
            extensions=extensions,
        )

        return await self.send(req)

    async def put(
        self,
        url: str = "",
        params: dict | None = {},
        headers: dict | None = {},
        cookies: dict | None = [],
        content: bytes | None = None,
        data: dict | None = {},
        files: dict[str, t.Any] | None = {},
        json: t.Any | None = None,
        stream: t.Any | None = None,
        extensions: dict[str, t.Any] | None = {},
    ):
        await self._ensure_client()

        req: httpx.Request = self.build_request(
            method="PUT",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            stream=stream,
            extensions=extensions,
        )

        return await self.send(req)
