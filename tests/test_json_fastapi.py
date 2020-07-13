from functools import lru_cache
from typing import Dict, List

import link_header
from urllib.parse import urlparse, parse_qs, urlencode
from http import HTTPStatus

from urllib3.util import Url

from json_fastapi import __version__, JsonFastAPI
from fastapi.testclient import TestClient
import json

app = JsonFastAPI("tests/fixtures")
client = TestClient(app.app)


@lru_cache(maxsize=20)
def load_driver(name: str):
    with open("tests/fixtures/drivers/{}.json".format(name)) as f:
        return json.load(f)


base_path = "/drivers"
expected_item = "daniel-ricciardo"


def test_version():
    assert __version__ == "0.1.0"


def test_get_item_int_by_id():
    response = client.get("/drivers/3")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == load_driver(expected_item)


def test_get_item_by_id_field():
    response = client.get("/drivers/Daniel Ricciardo")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == load_driver(expected_item)


def test_get_item_by_id_field_slugified():
    response = client.get("/drivers/daniel-ricciardo")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == load_driver(expected_item)


def test_get_items_first_page():
    per_page = 2
    response = client.get("/drivers?per_page={}".format(per_page))
    links = link_header.parse(response.headers["Link"])
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(body) == per_page
    assert_link_match(
        links, "first", base_path, {"page": ["1"], "per_page": [str(per_page)]}
    )
    assert_link_match(
        links, "next", base_path, {"page": ["2"], "per_page": [str(per_page)]}
    )
    assert_link_match(
        links, "last", base_path, {"page": ["10"], "per_page": [str(per_page)]}
    )
    assert_no_link(links, "prev")


def test_get_items_last_page():
    per_page = 3
    response = client.get("/drivers?page=7&per_page={}".format(per_page))
    links = link_header.parse(response.headers["Link"])
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(body) == 2
    assert_link_match(
        links, "first", base_path, {"page": ["1"], "per_page": [str(per_page)]}
    )
    assert_link_match(
        links, "prev", base_path, {"page": ["6"], "per_page": [str(per_page)]}
    )
    assert_link_match(
        links, "last", base_path, {"page": ["7"], "per_page": [str(per_page)]}
    )
    assert_no_link(links, "next")


def test_get_items_sorted():
    response = client.get("/drivers?sort_by=id")
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0] == load_driver(expected_item)
    assert response.json()[19] == load_driver("antonio-giovanazzi")


def test_get_items_sorted_reverse():
    response = client.get("/drivers?sort_by=-id")
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0] == load_driver("antonio-giovanazzi")
    assert response.json()[19] == load_driver(expected_item)


def test_get_items_fields():
    response = client.get("/drivers/3?fields=id")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 3}


def assert_link_match(
    links: link_header.LinkHeader,
    rel: str,
    path: str,
    query: Dict[str, List[str]] = None,
):
    if query is None:
        query = {}
    matching_links = links.links_by_attr_pairs([("rel", rel)])
    assert len(matching_links) == 1
    link = matching_links[0]
    href = urlparse(link.href)
    assert href.path == path
    # noinspection PyDeepBugsBinOperator
    assert query.items() <= parse_qs(href.query).items()


def assert_no_link(links: link_header.LinkHeader, rel: str):
    assert len(links.links_by_attr_pairs([("rel", rel)])) == 0
