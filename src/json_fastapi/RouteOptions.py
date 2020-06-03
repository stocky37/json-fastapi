from dataclasses import dataclass
from typing import Type, Any, List, Sequence, Union, Dict

from fastapi.encoders import SetIntStr, DictIntStrAny
from fastapi.params import Depends
from starlette.responses import Response


@dataclass
class RouteOptions:
    response_model: Type[Any] = None
    status_code: int = None
    tags: List[str] = None
    dependencies: Sequence[Depends] = None
    summary: str = None
    description: str = None
    response_description: str = None
    responses: Dict[Union[int, str], Dict[str, Any]] = None
    deprecated: bool = None
    methods: List[str] = None
    operation_id: str = None
    response_model_include: Union[SetIntStr, DictIntStrAny] = None
    response_model_exclude: Union[SetIntStr, DictIntStrAny] = None
    response_model_by_alias: bool = None
    response_model_skip_defaults: bool = None
    response_model_exclude_unset: bool = None
    response_model_exclude_defaults: bool = None
    response_model_exclude_none: bool = None
    include_in_schema: bool = None
    response_class: Type[Response] = None
    name: str = None
