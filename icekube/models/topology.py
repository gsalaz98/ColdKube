from typing import Optional
from icekube.models.base import BaseResource
from icekube.models.node import LabelSelector


class TopologySpreadConstraint(BaseResource):
    __name__ = "TopologySpreadConstraint"

    labelSelector: Optional[LabelSelector] = None
    maxSkew: Optional[int] = None
    minDomains: Optional[int] = None
    nodeAffinityPolicy: Optional[str] = None
    nodeTainsPolicy: Optional[str] = None
    topologyKey: Optional[str] = None
    whenUnsatisfiable: Optional[str] = None