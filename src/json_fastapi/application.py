from os import scandir, DirEntry
from typing import Dict

from fastapi import FastAPI
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from json_fastapi.endpoints import EndpointOptions, Endpoint


class JsonFastAPI:
    def __init__(
        self,
        api_dir: str,
        *,
        app: FastAPI = FastAPI(),
        db: TinyDB = TinyDB(storage=MemoryStorage),
        opts: Dict[str, EndpointOptions] = None,
    ):
        self.api_dir = api_dir
        self.app = app
        self.db = db
        self.opts = {} if opts is None else opts
        self.endpoints = self._scan_api_dir()
        self._setup()

    def _setup(self):
        for endpoint in self.endpoints.values():
            endpoint.add_routes(self.app)

    def _scan_api_dir(self) -> (Dict[str, Endpoint]):
        endpoints: Dict[str, Endpoint] = {}
        d: DirEntry
        for d in scandir(self.api_dir):
            if d.is_dir():
                endpoint = Endpoint(d.path, self.db, opts=self.opts.get(d.name))
                endpoints[d.name] = endpoint
        return endpoints
