from ._async_base import AsyncHttpxControllerBase

__all__ = ["AsyncHttpxController"]


class AsyncHttpxController(AsyncHttpxControllerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
