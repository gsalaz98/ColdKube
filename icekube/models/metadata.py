from __future__ import annotations

import json
from typing import Dict, List, Optional, Union

from icekube.relationships import Relationship
from icekube.models.base import RELATIONSHIP, BaseResource, Resource
from icekube.models.secret import Secret
from icekube.neo4j_util import mock

from pydantic import root_validator


class MatchCondition(BaseResource):
    expression: Optional[str] = None
    name: Optional[str] = None

class ServiceReference(BaseResource):
    name: Optional[str] = None
    namespace: Optional[str] = None
    path: Optional[str] = None
    port: Optional[int] = None

class OwnerReference(BaseResource):
    apiVersion: str
    blockOwnerDeletion: Optional[bool] = None
    controller: Optional[bool] = None
    kind: str
    name: str
    uid: str

    @property
    def db_labels(self):
        return self.model_dump()

class ManagedFieldsEntry(BaseResource):
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

    @property
    def db_labels(self):
        return super().db_labels

class ObjectMeta(BaseResource):
    apiVersion: str = "v1"
    kind: str = "ObjectMeta"

    annotations: Optional[Union[Dict[str, str], str]] = None
    creationTimestamp: Optional[str] = None
    deletionGracePeriodSeconds: Optional[int] = None
    deletionTimestamp: Optional[str] = None
    finalizers: Optional[List[str]] = None
    generateName: Optional[str] = None
    generation: Optional[int] = None
    labels: Optional[Union[Dict[str, str], str]] = None
    managedFields: Optional[Union[List[ManagedFieldsEntry], List[str]]] = None
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
        values["managedFields"] = [json.dumps(i) for i in values.get("managedFields", [])]
        return values

    @property
    def db_labels(self):
        return self.model_dump()
    
    @property
    def referenced_objects(self):
        return [
            *[mock(ManagedFieldsEntry, **json.loads(i)) for i in (self.managedFields if self.managedFields is not None else [])],
            *[mock(OwnerReference, **json.loads(i)) for i in (self.ownerReferences if self.ownerReferences is not None else [])]
        ]
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return []

class SecretReference(BaseResource):
    apiVersion: str = "v1"
    kind: str = "SecretReference"

    name: str
    namespace: str

    @property
    def db_labels(self):
        return self.model_dump()
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            mock(Secret, apiVersion="v1", kind="Secret", name=self.name, namespace=self.namespace)
        )]

class ObjectReference(BaseResource):
    apiVersion: str
    kind: str
    name: str
    namespace: Optional[str] = None
    corekind: Optional[str] = "ObjectReference"

    fieldPath: Optional[str] = None
    resourceVersion: Optional[str] = None
    uid: Optional[str] = None

    @property
    def db_labels(self):
        return self.model_dump()
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            mock(Resource, apiVersion=self.apiVersion, kind=self.kind, name=self.name, namespace=self.namespace)
        )]
    
class TypedObjectReference(BaseResource):
    corekind: Optional[str] = "TypedObjectReference"

    apiGroup: str
    kind: str
    name: str
    namespace: str

    @property
    def db_labels(self):
        return self.model_dump()
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            mock(Resource, apiVersion=self.apiGroup, kind=self.kind, name=self.name, namespace=self.namespace)
        )]
    
class TypedLocalObjectReference(BaseResource):
    corekind: Optional[str] = "TypedLocalObjectReference"

    apiGroup: str
    kind: str
    name: str

    @property
    def db_labels(self):
        return self.model_dump()
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(
            self, 
            Relationship.REFERENCES, 
            mock(Resource, apiVersion=self.apiGroup, kind=self.kind, name=self.name)
        )]