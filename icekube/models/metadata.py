from __future__ import annotations

import json
from typing import Dict, List, Optional, Union
from icekube.models.node import LabelSelector, NodeSelector, NodeSelectorTerm

from icekube.relationships import Relationship
from icekube.models.base import RELATIONSHIP, BaseResource, Resource

from pydantic import root_validator


class Object(BaseResource):
    key: Optional[str] = None
    value: Optional[str] = None

class KeyToPath(BaseResource):
    __name__ = "KeyToPath"

    key: Optional[str] = None
    mode: Optional[int] = None
    path: Optional[str] = None

class MatchCondition(BaseResource):
    __name__ = "MatchCondition"

    expression: Optional[str] = None
    name: Optional[str] = None

class ServiceReference(BaseResource):
    __name__ = "ServiceReference"

    name: Optional[str] = None
    namespace: Optional[str] = None
    path: Optional[str] = None
    port: Optional[int] = None

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            Resource(apiVersion="v1", kind="Service", name=self.name, namespace=self.namespace)
        )]

class OwnerReference(BaseResource):
    __name__ = "OwnerReference"

    apiVersion: str
    blockOwnerDeletion: Optional[bool] = None
    controller: Optional[bool] = None
    kind: str
    name: str
    uid: str

    @property
    def db_labels(self):
        return self.model_dump()
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            Resource(apiVersion=self.apiVersion, kind=self.kind, name=self.name)
        )]

class ManagedFieldsEntry(BaseResource):
    __name__ = "ManagedFieldsEntry"

    apiVersion: Optional[str] = None
    kind: Optional[str] = None

    fieldsType: Optional[str] = None
    fieldsV1: Optional[str] = None
    manager: Optional[str] = None
    operation: Optional[str] = None
    subresource: Optional[str] = None
    time: Optional[str] = None

    @root_validator(pre=True)
    def extract_values(cls, values):

        values["fieldsV1"] = json.dumps(values.get("fieldsV1", {}))
        return values

class ObjectMeta(BaseResource):
    __name__ = "ObjectMeta"

    annotations: Optional[Union[Dict[str, str], str]] = None
    creationTimestamp: Optional[str] = None
    deletionGracePeriodSeconds: Optional[int] = None
    deletionTimestamp: Optional[str] = None
    finalizers: Optional[List[str]] = None
    generateName: Optional[str] = None
    generation: Optional[int] = None
    labels: Optional[Union[Dict[str, str], str]] = None
    managedFields: Optional[List[ManagedFieldsEntry]] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    ownerReferences: Optional[List[OwnerReference]] = None
    resourceVersion: Optional[str] = None
    selfLink: Optional[str] = None
    uid: Optional[str] = None

    @root_validator(pre=True)
    def extract_values(cls, values):
        values["annotations"] = json.dumps(values.get("annotations", {}))
        values["labels"] = json.dumps(values.get("labels", {}))
        values["managedFields"] = [ManagedFieldsEntry(**i) for i in values.get("managedFields", [])]
        return values

    @property
    def referenced_objects(self):
        return [
            *[i for i in (self.managedFields if self.managedFields is not None else [])],
            *[i for i in (self.ownerReferences if self.ownerReferences is not None else [])]
        ]
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        relationships = super().relationships(initial=initial)
        relationships += [(self, Relationship.REFERENCES, i) for i in self.referenced_objects]
        return relationships

class SecretReference(BaseResource):
    __name__ = "SecretReference"

    name: str
    namespace: str

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.models.secret import Secret
        return [(
            self, 
            Relationship.REFERENCES, 
            Secret(apiVersion="v1", kind="Secret", name=self.name, namespace=self.namespace)
        )]

class ObjectReference(BaseResource):
    __name__ = "ObjectReference"

    apiVersion: str
    kind: str
    name: str
    namespace: Optional[str] = None

    fieldPath: Optional[str] = None
    resourceVersion: Optional[str] = None
    uid: Optional[str] = None

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            Resource(apiVersion=self.apiVersion, kind=self.kind, name=self.name, namespace=self.namespace)
        )]
    
class TypedObjectReference(BaseResource):
    __name__ = "TypedObjectReference"

    apiGroup: str
    kind: str
    name: str
    namespace: str

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            Resource(apiVersion=self.apiGroup, kind=self.kind, name=self.name, namespace=self.namespace)
        )]
    
class TypedLocalObjectReference(BaseResource):
    __name__ = "TypedLocalObjectReference"

    apiGroup: str
    kind: str
    name: str

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            Resource(apiVersion=self.apiGroup, kind=self.kind, name=self.name)
        )]
    
class LocalObjectReference(BaseResource):
    __name__ = "LocalObjectReference"

    name: str
    parent: BaseResource

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find
        found = find(self.parent, None, name=self.name, namespace=self.parent.namespace if self.parent is not None and self.parent.namespace is not None else None)
        if found is None or len(found) == 0:
            return []

        return [(
            self, 
            Relationship.REFERENCES, 
            found[0]
        )]
    
class ConfigMapKeySelector(BaseResource):
    __name__ = "ConfigMapKeySelector"

    key: Optional[str] = None
    name: Optional[str] = None
    optional: Optional[bool] = None
    namespace: Optional[str] = None

class ObjectFieldSelector(BaseResource):
    __name__ = "ObjectFieldSelector"

    apiVersion: Optional[str] = None
    fieldPath: Optional[str] = None

class ResourceFieldSelector(BaseResource):
    __name__ = "ResourceFieldSelector"

    containerName: Optional[str] = None
    divisor: Optional[str] = None
    resource: Optional[str] = None

class SecretKeySelector(BaseResource):
    __name__ = "SecretKeySelector"

    key: Optional[str] = None
    name: Optional[str] = None
    optional: Optional[bool] = None
    namespace: Optional[str] = None

class EnvVarSource(BaseResource):
    __name__ = "EnvVarSource"

    configMapKeyRef: Optional[ConfigMapKeySelector] = None
    fieldRef: Optional[ObjectFieldSelector] = None
    resourceFieldRef: Optional[ResourceFieldSelector] = None
    secretKeyRef: Optional[SecretKeySelector] = None

class ExecAction(BaseResource):
    __name__ = "ExecAction"

    command: Optional[List[str]] = None

class HTTPHeader(BaseResource):
    __name__ = "HTTPHeader"

    name: Optional[str] = None
    value: Optional[str] = None

class HTTPGetAction(BaseResource):
    __name__ = "HTTPGetAction"

    host: Optional[str] = None
    httpHeaders: Optional[List[HTTPHeader]] = None
    path: Optional[str] = None
    port: Optional[Union[int, str]] = None
    scheme: Optional[str] = None

class TCPSocketAction(BaseResource):
    __name__ = "TCPSocketAction"

    host: Optional[str] = None
    port: Optional[Union[int, str]] = None

class GRPCAction(BaseResource):
    __name__ = "GRPCAction"

    port: Optional[int] = None
    service: Optional[str] = None

class LifecycleHandler(BaseResource):
    __name__ = "LifecycleHandler"

    exec: Optional[ExecAction] = None
    httpGet: Optional[HTTPGetAction] = None
    tcpSocket: Optional[TCPSocketAction] = None

class Lifecycle(BaseResource):
    __name__ = "Lifecycle"

    postStart: Optional[LifecycleHandler] = None
    preStop: Optional[LifecycleHandler] = None

class Probe(BaseResource):
    __name__ = "Probe"

    exec: Optional[ExecAction] = None
    failureThreshold: Optional[int] = None
    grpc: Optional[GRPCAction] = None
    httpGet: Optional[HTTPGetAction] = None
    initialDelaySeconds: Optional[int] = None
    periodSeconds: Optional[int] = None
    successThreshold: Optional[int] = None
    tcpSocket: Optional[TCPSocketAction] = None
    terminationGracePeriodSeconds: Optional[int] = None
    timeoutSeconds: Optional[int] = None