

from typing import Optional
from icekube.models.base import BaseResource


class PodIP(BaseResource):
    __name__ = "PodIP"

    ip: Optional[str] = None