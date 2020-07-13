from typing import List, Dict

from fastapi import Query
from starlette.requests import Request
from starlette.responses import Response


class FieldsFilter:
    def __init__(
        self, request: Request, response: Response, fields: str = Query(""),
    ):
        self.request = request
        self.response = response
        self.fields: List[str] = list(filter(bool, fields.split(",")))

    def filter(self, obj: Dict) -> Dict:
        if not self.fields:
            return obj
        return {k: obj.get(k) for k in self.fields if obj.get(k) is not None}

    def filter_all(self, objs: List[Dict]) -> List[Dict]:
        return list(map(self.filter, objs))

    def __repr__(self):
        return str(self.__dict__)
