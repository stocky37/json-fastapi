from os import scandir, DirEntry

from fastapi import FastAPI
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from json_fastapi.endpoints import EntityEndpoint


def init_api(
    root_dir: str,
    *,
    app: FastAPI = FastAPI(),
    db: TinyDB = TinyDB(storage=MemoryStorage),
    route_opts=None,
    opts=None,
) -> (FastAPI, TinyDB):
    if route_opts is None:
        route_opts = {}

    d: DirEntry
    for d in scandir(root_dir):
        if d.is_dir():
            EntityEndpoint(
                d.name,
                d.path,
                app,
                db,
                opts=opts.get(d.name),
                route_opts=route_opts.get(d.name),
            )
    return app, db
