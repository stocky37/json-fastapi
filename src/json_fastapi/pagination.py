from fastapi import Query
from link_header import LinkHeader, Link
from starlette.requests import Request
from starlette.responses import Response
import math


class Pagination:
    _default_page: int = 1
    _default_per_page: int = 100
    _max_per_page: int = 1000

    def __init__(
        self,
        request: Request,
        response: Response,
        page: int = Query(_default_page, ge=1),
        per_page: int = Query(_default_per_page, ge=1, le=_max_per_page),
    ):
        self.page = page
        self.per_page = per_page
        self.request = request
        self.response = response

    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    def first_page(self) -> int:
        return self._default_page

    def last_page(self, count: int) -> int:
        return math.ceil(count / self.per_page)

    def next_url(self, count: int):
        if self.page == self.last_page(count):
            return None

        return self.request.url.include_query_params(page=self.page + 1)

    def prev_url(self):
        if self.page == self.first_page():
            return None

        return self.request.url.include_query_params(page=self.page - 1)

    def first_url(self):
        return self.request.url.include_query_params(page=self.first_page())

    def last_url(self, count: int):
        return self.request.url.include_query_params(page=self.last_page(count))

    def paginate(self, item_list: list):
        count = len(item_list)
        links = [
            Link(self.request.url, rel="self"),
            Link(self.first_url(), rel="first"),
            Link(self.last_url(count), rel="last"),
        ]

        next = self.next_url(count)
        if next is not None:
            links.append(Link(next, rel="next"))

        prev = self.prev_url()
        if prev is not None:
            links.append(Link(prev, rel="prev"))

        self.response.headers["Link"] = str(LinkHeader(links))

        return item_list[self.offset() : self.offset() + self.per_page]
