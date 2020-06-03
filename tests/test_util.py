from dataclasses import dataclass

from json_fastapi.util import as_dict


def test_as_dict():
    @dataclass
    class BasicClass:
        a: str = None
        b: str = "b"

    assert as_dict(BasicClass()) == {"b": "b"}


def test_as_dict_none():
    assert as_dict(None) == {}
