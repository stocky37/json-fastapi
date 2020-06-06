import json
import os
from dataclasses import dataclass, field
from os import DirEntry, scandir
from typing import List, Any, Type

from fastapi import FastAPI, Depends, HTTPException
from slugify import slugify
from tinydb import where, TinyDB

from json_fastapi.pagination import Pagination


@dataclass
class EndpointOptions:
    id_fields: List[str] = field(default_factory=lambda: ["id", "name", "slug"])
    slugify_id: bool = True
    response_model: Type[Any] = None


class Endpoint:
    route_get_all: str = "get_all"
    route_get_by_id: str = "get_by_id"

    def __init__(
        self, path: str, db: TinyDB, opts: EndpointOptions = EndpointOptions()
    ):
        self.name = os.path.basename(path)
        self.opts = EndpointOptions() if opts is None else opts
        self.table = self._build_table(path, db)

    async def get_all(self, pager: Pagination = Depends(Pagination)):
        return pager.paginate(self.table.all())

    async def get_by_id(self, name: str):
        for id_field in self.opts.id_fields:
            entity = self.table.get(where(id_field) == self._slugify(name))
            if entity is not None:
                return entity
        raise HTTPException(404, "Entity not found")

    def add_routes(self, app: FastAPI) -> FastAPI:
        app.add_api_route(
            "/{}".format(self.name),
            self.get_all,
            response_model=None
            if self.opts.response_model is None
            else List[self.opts.response_model],
        )
        app.add_api_route(
            "/{}/{{name}}".format(self.name),
            self.get_by_id,
            response_model=self.opts.response_model,
        )
        return app

    def _build_table(self, path: str, db: TinyDB) -> TinyDB.table_class:
        table = db.table(self.name)
        file: DirEntry
        for file in scandir(path):
            if file.is_file and file.name.endswith(".json"):
                with open(file.path, encoding="utf-8") as f:
                    table.insert(json.load(f))
        return table

    def _slugify(self, str_: str) -> str:
        return slugify(str_) if self.opts.slugify_id else str_
