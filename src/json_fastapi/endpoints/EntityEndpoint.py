import json
from os import DirEntry, scandir
from typing import Dict

from fastapi import FastAPI, Depends
from slugify import slugify
from tinydb import where, TinyDB

from json_fastapi.RouteOptions import RouteOptions
from json_fastapi.pagination import Pagination
from json_fastapi.util import as_dict


class EntityEndpoint(object):
    route_all_name: str = "all"
    route_one_name: str = "one"

    def __init__(
        self,
        name: str,
        path: str,
        app: FastAPI,
        db: TinyDB,
        *,
        route_opts: Dict[str, RouteOptions] = None
    ):
        self.name = name
        self.db = db
        self.route_opts = {} if route_opts is None else route_opts
        self.table = self._build_table(path)
        self._add_routes(app)

    def _add_routes(self, app: FastAPI) -> FastAPI:
        app.add_api_route(
            "/{}".format(self.name),
            self.get_all,
            **as_dict(self.route_opts.get(EntityEndpoint.route_all_name))
        )
        app.add_api_route(
            "/{}/{{name}}".format(self.name),
            self.get_one,
            **as_dict(self.route_opts.get(EntityEndpoint.route_one_name))
        )
        return app

    def _build_table(self, path: str) -> TinyDB.table_class:
        table = self.db.table(self.name)
        file: DirEntry
        for file in scandir(path):
            if file.is_file and file.name.endswith(".json"):
                with open(file.path, encoding="utf-8") as f:
                    table.insert(json.load(f))
        return table

    async def get_all(self, pager: Pagination = Depends(Pagination)):
        return pager.paginate(self.table.all())

    async def get_one(self, name: str):
        return self.table.get(where("slug") == slugify(name))
