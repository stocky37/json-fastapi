from enum import Enum
from operator import itemgetter
from typing import Dict, List

from fastapi import Query


class SortDirection(Enum):
    ASC = 1
    DESC = 2


class Sorting:
    def __init__(
        self, sort_by: str = Query(None),
    ):
        if sort_by.startswith("-"):
            self.sort_direction = SortDirection.DESC
            self.sort_field = sort_by[1:]
        else:
            self.sort_direction = SortDirection.ASC
            self.sort_field = sort_by

    def sort(self, objs: List[Dict]):
        return sorted(
            objs,
            key=itemgetter(self.sort_field),
            reverse=self.sort_direction == SortDirection.DESC,
        )
