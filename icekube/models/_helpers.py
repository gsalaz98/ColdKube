from typing import Any, Dict, Type, Optional
from icekube.models.base import Resource

from kubernetes.client import ApiClient
from pydantic import BaseModel

def to_dict(resource) -> Dict[str, Any]:
    resp: Dict[str, Any] = ApiClient().sanitize_for_serialization(resource)
    return resp

def build_default(kvp: Dict[str, Any], key: str, value: Optional[Any]) -> Resource:
    kvp[key] = value
    return kvp

def build_default_resource(
    kvp: BaseModel,
    key: str,
    objRef: Type[Resource],
    value: Dict[str, Any]
) -> Resource:
    if value is not None:
        kvp[key] = objRef(**value)
    else:
        kvp[key] = None

    return kvp

def build_default_toplevel_str(
    values: BaseModel,
    key: str,
    spec: Dict[str, Any]
) -> Resource:
    build_default(values, key, spec.get(key))
    return values

def build_default_toplevel_resource(
    cls: Type[Resource],
    key: str,
    values: BaseModel,
    spec: Dict[str, Any]
) -> Resource:
    build_default_resource(values, key, cls, spec.get(key))
    return values