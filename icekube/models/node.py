from __future__ import annotations
from typing import Dict, List, Optional, Union

from icekube.models.base import BaseResource, Resource


class TopologySelectorLabelRequirement(BaseResource):
    apiVersion: str = "v1"
    kind: str = "TopologySelectorLabelRequirement"

    key: str
    values: List[str]

    @property
    def db_labels(self):
        return self.model_dump()

class TopologySelectorTerm(BaseResource):
    apiVersion: str = "v1"
    kind: str = "TopologySelectorTerm"

    matchLabelExpressions: Optional[TopologySelectorLabelRequirement] = None

    @property
    def db_labels(self):
        return {
            "matchLabelExpressions": self.matchLabelExpressions.objHash
        }
    
    @property
    def referenced_objects(self):
        return [
            self.matchLabelExpressions
        ]

class LabelSelectorRequirement(BaseResource):
    apiVersion: str = "v1"
    kind: str = "LabelSelectorRequirement"

    key: str
    operator: str
    values: List[str]

class LabelSelector(BaseResource):
    matchExpressions: Optional[LabelSelectorRequirement] = None
    matchLabels: Optional[Union[Dict[str, str], str]] = None

class NodeSelectorRequirement(BaseResource):
    apiVersion: str = "v1"
    kind: str = "NodeSelectorRequirement"

    key: str
    operator: str
    values: List[str]

    @property
    def db_labels(self):
        return self.model_dump()

class NodeSelectorTerm(BaseResource):
    apiVersion: str = "v1"
    kind: str = "NodeSelectorTerm"

    matchExpressions: Optional[NodeSelectorRequirement]
    matchFields: Optional[NodeSelectorRequirement]

    @property
    def db_labels(self):
        return {
            "matchExpressions": self.matchExpressions.objHash,
            "matchFields": self.matchFields.objHash
        }
    
    @property
    def referenced_objects(self):
        return [
            self.matchExpressions,
            self.matchFields
        ]

class NodeSelector(BaseResource):
    apiVersion: str = "v1"
    kind: str = "NodeSelector"

    nodeSelectorTerms: NodeSelectorTerm

    @property
    def db_labels(self):
        return {
            "nodeSelectorTerms": self.nodeSelectorTerms.objHash
        }
    
    @property
    def referenced_objects(self):
        return [
            self.nodeSelectorTerms
        ]



class Node(Resource):
    ...
