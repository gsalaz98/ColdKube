from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from icekube.relationships import Relationship
from icekube.models._helpers import *
from icekube.models.base import RELATIONSHIP, BaseResource, Resource
from icekube.models.node import LabelSelector, NodeSelector
from icekube.models.metadata import *
from icekube.models.resources import ResourceRequirements
from pydantic import BaseModel, Field, root_validator


class RuleWithOperations(BaseResource):
    __name__ = "RuleWithOperations"

    apiGroups: Optional[List[str]] = None
    apiVersions: Optional[List[str]] = None
    operations: Optional[List[Literal["CREATE", "UPDATE", "DELETE", "CONNECT"]]] = None
    resources: Optional[List[str]] = None
    scope: Optional[Literal["Cluster", "Namespaced", "*"]] = None

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find, get_resource_kind

        r = super().relationships(initial=initial)

        for apiGroup in self.apiGroups:
            for apiVersion in self.apiVersions:
                for resource in self.resources:
                    if resource is None:
                        continue

                    objApiVersion = '/'.join((apiGroup, apiVersion))
                    resource_first = resource.split('/')[0]

                    if resource_first != '*':
                        r.append((
                            self, 
                            Relationship.REFERENCES, 
                            Resource(
                                apiVersion=apiVersion, 
                                kind=resource.split('/')[0] if resource is not None else None
                            )
                        ))

                        continue

                    # Wildcard all means all resources under the apiVersion, so let's pull
                    # every resource matching the apiVersion and add a relationship to it.
                    resources = list(find(None, False, apiVersion=objApiVersion))
                    for foundResource in resources:
                        kind = get_resource_kind(foundResource)
                        for operation in self.operations:
                            r.append((self, Relationship.generate_grant(operation, f"{kind.upper()}S"), foundResource))

        return r

class WebhookClientConfig(BaseResource):
    __name__ = "WebhookClientConfig"

    caBundle: Optional[str] = None
    service: Optional[ServiceReference] = None
    url: Optional[str] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        values["service"] = ServiceReference(**values.get("service")) if values.get("service") is not None else None
        return values
    
    @property
    def db_labels(self):
        return {
            **super().db_labels,
            "service": self.service.objHash if self.service is not None else None
        }
    
    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            self.service
        ]
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [
            (self, Relationship.DEFINES, self.service)
        ]

class MutatingWebhook(BaseResource):
    __name__ = "MutatingWebhook"

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

    @root_validator(pre=True)
    def extract_fields(cls, values):
        values["clientConfig"] = WebhookClientConfig(**values.get("clientConfig", {}))
        values["matchConditions"] = [LabelSelector(**i) for i in values.get("matchConditions", [])]
        values["namespaceSelector"] = LabelSelector(**values.get("namespaceSelector", {}))
        values["objectSelector"] = LabelSelector(**values.get("objectSelector", {}))
        values["rules"] = [RuleWithOperations(**i) for i in values.get("rules", [])]
        return values

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [i for i in [
            self.clientConfig,
            *(self.matchConditions if self.matchConditions is not None else []),
            self.namespaceSelector,
            self.objectSelector,
            *(self.rules if self.rules is not None else [])
        ] if i is not None]

class MutatingWebhookConfiguration(Resource):
    __name__ = "MutatingWebhookConfiguration"

    apiVersion: Optional[str] = None
    kind: Optional[str] = None
    metadata: Optional[ObjectMeta] = None
    webhooks: Optional[Union[List[MutatingWebhook], List[str]]] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        metadata = json.loads(values.get("raw", "{}")).get("metadata", {})
        spec = json.loads(values.get("raw", "{}"))

        values["metadata"] = ObjectMeta(**metadata)
        values["webhooks"] = [MutatingWebhook(**i) for i in spec.get("webhooks", [])]

        return values
    
    @property
    def db_labels(self):
        return {
            **super().db_labels,
            "metadata": self.metadata.objHash if self.metadata is not None else None,
            "webhooks": [i.objHash for i in self.webhooks] if self.webhooks is not None else None
        }

    @property
    def referenced_objects(self):
        return [
            self.metadata,
            *(self.webhooks if self.webhooks is not None else [])
        ]

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find

        relationships = super().relationships(initial=initial)

        if self.metadata is None:
            return relationships

        ownerReferences = self.metadata.ownerReferences if self.metadata.ownerReferences is not None else []
        relationships += [(self, Relationship.DEFINES, self.metadata)]
        relationships += [(self, Relationship.DEFINES, i) for i in self.webhooks if i is not None]

        for owner in ownerReferences:
            results = find(Resource(apiVersion=owner.apiVersion, kind=owner.kind, name=owner.name))
            results = list(results)

            for result in results:
                relationships.append((result, Relationship.OWNS, self))

        return relationships

class ValidatingWebhook(BaseResource):
    __name__ = "ValidatingWebhook"

    admissionReviewVersions: Optional[List[str]] = None
    clientConfig: Optional[WebhookClientConfig] = None
    failurePolicy: Optional[Union[Literal["Ignore"], Literal["Fail"]]] = None
    matchConditions: Optional[List[LabelSelector]] = None
    matchPolicy: Optional[Union[Literal["Exact"], Literal["Equivalent"]]] = None
    name: Optional[str] = None
    namespaceSelector: Optional[LabelSelector] = None
    objectSelector: Optional[LabelSelector] = None
    rules: Optional[List[RuleWithOperations]] = None
    sideEffects: Optional[Union[Literal["None"], Literal["NoneOnDryRun"], Literal["Some"], Literal["Unknown"]]] = None
    timeoutSeconds: Optional[int] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        values["clientConfig"] = WebhookClientConfig(**values.get("clientConfig", {}))
        values["matchConditions"] = [LabelSelector(**i) for i in values.get("matchConditions", [])]
        values["namespaceSelector"] = LabelSelector(**values.get("namespaceSelector", {}))
        values["objectSelector"] = LabelSelector(**values.get("objectSelector", {}))
        values["rules"] = [RuleWithOperations(**i) for i in values.get("rules", [])]
        return values

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [i for i in [
            self.clientConfig,
            *(self.matchConditions if self.matchConditions is not None else []),
            self.namespaceSelector,
            self.objectSelector,
            *(self.rules if self.rules is not None else [])
        ] if i is not None]


class ValidatingWebhookConfiguration(Resource):
    __name__ = "ValidatingWebhookConfiguration"

    apiVersion: Optional[str] = None
    kind: Optional[str] = None
    metadata: Optional[ObjectMeta] = None
    webhooks: Optional[Union[List[ValidatingWebhook], List[str]]] = None

    @property
    def db_labels(self):
        return {
            **super().db_labels,
            "metadata": self.metadata.objHash if self.metadata is not None else None,
            "webhooks": [i.objHash for i in self.webhooks] if self.webhooks is not None else None
        }

    @property
    def referenced_objects(self):
        return [
            self.metadata,
            *(self.webhooks if self.webhooks is not None else [])
        ]

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find

        relationships = super().relationships(initial=initial)

        if self.metadata is None:
            return relationships

        ownerReferences = self.metadata.ownerReferences if self.metadata.ownerReferences is not None else []
        relationships += [(self, Relationship.DEFINES, self.metadata)]
        relationships += [(self, Relationship.DEFINES, i) for i in self.webhooks if i is not None]

        for owner in ownerReferences:
            results = find(Resource(apiVersion=owner.apiVersion, kind=owner.kind, name=owner.name))
            results = list(results)

            for result in results:
                relationships.append((result, Relationship.OWNS, self))

        return relationships