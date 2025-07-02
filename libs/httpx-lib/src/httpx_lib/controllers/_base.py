import typing as t
import logging
from pathlib import Path

import httpx
import hishel


class HttpxControllerBase:
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
        debug: bool = False
    ):
        self.use_cache = use_cache
        self.cache_type = cache_type
        self.cache_db_path = cache_db_path
        self.cache_file_dir = cache_file_dir
        self.cache_redis_host = cache_redis_host
        self.cache_redis_port = cache_redis_port
        self.cache_redis_db = cache_redis_db
        self.cache_redis_password = cache_redis_password
        self.cache_ttl = cache_ttl
        self.check_ttl_every = check_ttl_every
        self.force_cache = force_cache
        self.cacheable_methods = cacheable_methods
        self.cacheable_status_codes = cacheable_status_codes

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

        ## Remove None values so httpx/hishel get only the explicitly set params
        client_args = {
            k: v for k, v in self._client_params.items() if v is not None and v != ""
        }

        if self.use_cache:
            client_args["transport"] = self._get_cache_transport()
            self.client = hishel.CacheClient(**client_args)
        else:
            self.client = httpx.Client(**client_args)

        ## Add class logger
        self.log = logging.getLogger(__name__)
        
        ## Silence httpx, hishel logs
        if not debug:
            logging.getLogger("httpx").setLevel("ERROR")
            logging.getLogger("hishel").setLevel("ERROR")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()

        if exc_value:
            self.log.error(f"({exc_type}): {exc_value}")

            return False

        return True

    def _get_cache_storage(self):
        if self.cache_type == "sqlite":
            import sqlite3

            Path(self.cache_db_path).parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(self.cache_db_path)

            return hishel.SQLiteStorage(connection=conn, ttl=self.cache_ttl)
        elif self.cache_type == "file":
            Path(self.cache_file_dir).mkdir(parents=True, exist_ok=True)

            return hishel.FileStorage(
                base_path=self.cache_file_dir,
                ttl=self.cache_ttl,
                check_ttl_every=self.check_ttl_every,
            )
        elif self.cache_type == "redis":
            try:
                import redis
            except ImportError:
                raise ImportError("redis is required for redis cache. Please install it.")

            redis_client = redis.Redis(
                host=self.cache_redis_host,
                port=self.cache_redis_port,
                db=self.cache_redis_db,
                password=self.cache_redis_password,
                decode_responses=False,
            )

            return hishel.RedisStorage(
                client=redis_client,
                ttl=self.cache_ttl,
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

    def _get_cache_transport(self):
        storage = self._get_cache_storage()
        controller = self._get_cache_controller()

        return hishel.CacheTransport(
            transport=httpx.HTTPTransport(),
            storage=storage,
            controller=controller,
        )

    def build_request(
        self,
        method: str = "GET",
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
    ) -> httpx.Request:
        self.log.debug(f"Method: {method}, URL: {url}")

        ## Merge client-level and request-level headers
        merged_headers = (self._client_params.get("headers") or {}).copy()
        if headers:
            merged_headers.update(headers)

        ## Similarly for params, cookies, etc.
        merged_params = (self._client_params.get("params") or {}).copy()
        if params:
            merged_params.update(params)

        merged_cookies = (self._client_params.get("cookies") or {}).copy()
        if cookies:
            merged_cookies.update(cookies)

        ## For content/data/files/json/extensions, use request-level if provided, else client-level
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
            params=params,
            headers=headers,
            cookies=cookies,
            content=_content,
            data=_data,
            files=_files,
            json=_json,
            stream=stream,
            extensions=_extensions,
        )

        return request

    def send(
        self,
        request: httpx.Request,
        stream: bool = False,
        auth: t.Tuple[str, str] | t.Callable[..., t.Any] | object | None = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        try:
            res: httpx.Response = self.client.send(
                request, stream=stream, auth=auth, follow_redirects=follow_redirects
            )
            res.raise_for_status()

            return res
        except httpx.ConnectError as e:
            self.log.error(f"Connection error: {e}")
            raise
        except httpx.ConnectTimeout as e:
            self.log.error(f"Connection timeout: {e}")
            raise
        except httpx.CookieConflict as ce:
            self.log.error(f"Cookie conflict: {ce}")
            raise
        except httpx.HTTPError as e:
            self.log.error(f"HTTP error: {e}")
            raise
        except httpx.RequestError as e:
            self.log.error(f"Request error: {e}")
            raise
        except httpx.TooManyRedirects as e:
            self.log.error(f"Too many redirects: {e}")
            raise
        except httpx.InvalidURL as e:
            self.log.error(f"URL invalid: {e}")
            raise
        except httpx.UnsupportedProtocol as e:
            self.log.error(f"Unsupported protocol: {e}")
            raise
        except httpx.ReadTimeout as e:
            self.log.error(f"Read timeout: {e}")
            raise
        except Exception as exc:
            raise exc

    def get(
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

        return self.send(req)

    def post(
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

        return self.send(req)

    def patch(
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

        return self.send(req)

    def delete(
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

        return self.send(req)

    def head(
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

        return self.send(req)

    def put(
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

        return self.send(req)
