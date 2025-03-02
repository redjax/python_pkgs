# Python Packages

My monorepo where I keep packages I repeatedly copy/paste into new projects, but that I don't want to publish to Pypi.

Libary code is in the [`libs/` directory](./libs/). All packages should be isolated from each other, meaning you can copy the `src/<package_name>` directory from any library package into your project to get up and running. Check each library's `pyproject.toml`'s `[dendencies]` section to see if you need to install any extra packages.

Most of my packages rely on `loguru`, although I'm working to implement stdlib logging.
