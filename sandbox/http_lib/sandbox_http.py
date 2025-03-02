# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "hishel",
#     "http-lib",
#     "httpx",
# ]
#
# [tool.uv.sources]
# http-lib = { path = "../../libs/http-lib" }
# ///

from loguru import logger as log

import httpx
import hishel
import http_lib

if __name__ == "__main__":
    log.info("Start http_lib sandbox")
    
    url = "https://www.google.com"
    req = http_lib.build_request(url=url, headers={"User-Agent": "python_pkgs / 1.0.0"})
    controller  = http_lib.get_http_controller(use_cache=False)
    
    log.info(f"Requesting URL: {url}")
    with controller as http_ctl:
        res: httpx.Response = http_ctl.send_request(req)
        res.raise_for_status()
        
    if not res.status_code == 200:
        log.warning(f"Non-200 response: [{res.status_code}: {res.reason_phrase}]: {res.text}")
        
    log.info(f"Response: [{res.status_code}: {res.reason_phrase}]")
    
