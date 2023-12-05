from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Type, Union

from icekube.relationships import Relationship
from icekube.models._helpers import *
from icekube.models.base import RELATIONSHIP, BaseResource, Resource
from icekube.models.node import LabelSelector, NodeSelector
from icekube.models.metadata import *
from icekube.models.resources import ResourceRequirements
from pydantic import BaseModel, Field, root_validator


class RuleWithOperations(BaseResource):
    apiGroups: Optional[List[str]] = None
    apiVersions: Optional[List[str]] = None
    operations: Optional[List[Literal["CREATE", "UPDATE", "DELETE", "CONNECT"]]] = None
    resources: Optional[List[str]] = None
    scope: Optional[Literal["Cluster", "Namespaced", "*"]] = None

class WebhookClientConfig(BaseResource):
    caBundle: Optional[str] = None
    service: Optional[ServiceReference] = None
    url: Optional[str] = None

class MutatingWebhook(BaseResource):
    admissionReviewVersions: Optional[List[str]] = None
    clientConfig: Optional[WebhookClientConfig] = None
    failurePolicy: Optional[Union[Literal["Ignore"], Literal["Fail"]]] = None
    matchConditions: Optional[List[LabelSelector]] = None
    matchPolicy: Optional[Union[Literal["Exact"], Literal["Equivalent"]]] = None
    name: Optional[str] = None
    namespaceSelector: Optional[LabelSelector] = None
    objectSelector: Optional[LabelSelector] = None
    reinvocationPolicy: Optional[Union[Literal["Never"], Literal["IfNeeded"]]] = None
    rules: Optional[List[RuleWithOperations]] = None
    sideEffects: Optional[Union[Literal["None"], Literal["NoneOnDryRun"], Literal["Unknown"], Literal["Some"], Literal["Unknown"]]] = None
    timeoutSeconds: Optional[int] = None

class MutatingWebhookConfiguration(Resource):
    apiVersion: Optional[str] = None
    kind: Optional[str] = None
    metadata: Optional[ObjectMeta] = None
    webhooks: Optional[Union[List[MutatingWebhook], List[str]]] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        metadata = json.loads(values.get("raw", "{}")).get("metadata", {})
        spec = json.loads(values.get("raw", "{}")).get("spec", {})

        values["metadata"] = mock(ObjectMeta, **metadata)
        values["webhooks"] = [mock(MutatingWebhook, **i) for i in spec.get("webhooks", [])]

        return values

    @property
    def db_labels(self) -> Dict[str, Any]:
        return {
            k: (v["objHash"] if v is not None and "objHash" in v else [
                i["objHash"] if i is not None and "objHash" in i else i for i in v
                ] if isinstance(v, list) else v
                ) for k, v in self.model_dump().items()
        }
    
    @property
    def referenced_objects(self):
        return [
            self.metadata,
            *self.webhooks
        ]

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find

        if self.metadata is None:
            return []

        ownerReferences = self.metadata.ownerReferences if self.metadata.ownerReferences is not None else []
        relationships = [(self, Relationship.DEFINES, self.metadata)]

        for owner in ownerReferences:
            results = find(mock(Resource, apiVersion=owner.apiVersion, kind=owner.kind, name=owner.name))
            results = list(results)

            for result in results:
                relationships.append((result, Relationship.OWNS, self))

        return relationships