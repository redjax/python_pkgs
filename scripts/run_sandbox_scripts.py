import logging
import typing as t
import subprocess as sp

from pathlib import Path

log = logging.getLogger(__name__)

def main():
    sandbox_scripts: list[Path] = [p for p in Path("sandbox").rglob("**/*.py")] or []
    log.info(f"Found [{len(sandbox_scripts)}] sandbox script(s)")
    
    success: list[Path] = []
    failure: list[Path] = []
    
    for _script in sandbox_scripts:
        cmd = ["uv", "run", _script]
        log.debug(f"Command: {cmd}")
        
        log.info(f"Executing sandbox script: {_script}")
        try:
            sp.run(cmd, check=True)
            log.info(f"Sandbox script '{_script}' executed successfully")
            
            success.append(_script)
        except Exception as exc:
            msg = f"({type(exc)}) Error running script '{_script}'. Details: {exc}"
            log.error(msg)
            
            failure.append(_script)
            
            continue
        
    log.info(f"Succeeded on [{len(success)}] script(s), failed on [{len(failure)}] script(s)")
    
    if len(failure) > 0:
        log.error(f"Failed on [{len(failure)}] script(s): {failure}")

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG", format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    main()
