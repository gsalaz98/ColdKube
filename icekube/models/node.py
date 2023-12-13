from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Union

from icekube.models.base import BaseResource, Resource


class TopologySelectorLabelRequirement(BaseResource):
    __name__ = "TopologySelectorLabelRequirement"

    key: Optional[str] = None
    values: Optional[List[str]] = None

class TopologySelectorTerm(BaseResource):
    __name__ = "TopologySelectorTerm"

    matchLabelExpressions: Optional[TopologySelectorLabelRequirement] = None

class LabelSelectorRequirement(BaseResource):
    __name__ = "LabelSelectorRequirement"

    key: Optional[str] = None
    operator: Optional[str] = None
    values: Optional[List[str]] = None

class LabelSelector(BaseResource):
    __name__ = "LabelSelector"

    matchExpressions: Optional[LabelSelectorRequirement] = None
    matchLabels: Optional[Union[Dict[str, str], str]] = None

    @property
    def db_labels(self):
        return {
            "matchExpressions": self.matchExpressions.objHash if self.matchExpressions is not None else None,
            "matchLabels": json.dumps(self.matchLabels) if self.matchLabels is not None else None
        }

class NodeSelectorRequirement(BaseResource):
    __name__ = "NodeSelectorRequirement"

    key: Optional[str] = None
    operator: Optional[str] = None
    values: Optional[List[str]] = None

class NodeSelectorTerm(BaseResource):
    __name__ = "NodeSelectorTerm"

    matchExpressions: Optional[List[NodeSelectorRequirement]] = None
    matchFields: Optional[List[NodeSelectorRequirement]] = None

class NodeSelector(BaseResource):
    __name__ = "NodeSelector"

    nodeSelectorTerms: Optional[List[NodeSelectorTerm]] = None

class Node(Resource):
    __name__ = "Node"

    apiVersion: str = "v1"
    kind: str = "Node"

    @property
    def db_labels(self) -> Dict[str, Any]:
        return {
            **super().db_labels,
            "name": self.name,
        }