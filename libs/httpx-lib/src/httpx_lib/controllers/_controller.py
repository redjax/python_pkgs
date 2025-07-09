from __future__ import annotations

import typing as t

from ._base import HttpxControllerBase

import httpx

__all__ = ["HttpxController"]


class HttpxController(HttpxControllerBase):
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
        debug: bool = False,
        *args,
        **kwargs,
    ):
        # super().__init__(*args, **kwargs)
        super().__init__(
            use_cache=use_cache,
            force_cache=force_cache,
            cache_ttl=cache_ttl,
            check_ttl_every=check_ttl_every,
            cache_type=cache_type,
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
            cache_db_path=cache_db_path,
            cache_file_dir=cache_file_dir,
            cache_redis_host=cache_redis_host,
            cache_redis_port=cache_redis_port,
            cache_redis_db=cache_redis_db,
            cache_redis_password=cache_redis_password,
            cacheable_methods=cacheable_methods,
            cacheable_status_codes=cacheable_status_codes,
            debug=debug,
            *args,
            **kwargs,
        )
