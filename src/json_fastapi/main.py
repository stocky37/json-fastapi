from os import scandir, DirEntry

from fastapi import FastAPI
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from json_fastapi.endpoints import EntityEndpoint


def init_api(
    root_dir: str, app: FastAPI = FastAPI(), db: TinyDB = TinyDB(storage=MemoryStorage)
) -> (FastAPI, TinyDB):
    d: DirEntry
    for d in scandir(root_dir):
        if d.is_dir():
            EntityEndpoint(d.name, d.path, app, db)
    return app, db
