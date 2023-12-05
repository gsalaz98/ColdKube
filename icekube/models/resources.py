from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from icekube.relationships import Relationship
from icekube.models.base import RELATIONSHIP, BaseResource, Resource
from icekube.models.node import NodeSelector
from icekube.models.metadata import *
from pydantic import BaseModel, Field, root_validator


class ResourceClaim(BaseResource):
    apiVersion: str = "v1"
    kind: str = "ResourceClaim"
    name: str

class ResourceRequirements(BaseResource):
    apiVersion: str = "v1"
    kind: str = "ResourceRequirements"

    claims: Optional[List[ResourceClaim]] = None
    limits: Optional[Union[Dict[str, Any], str]] = None
    requests: Optional[Union[Dict[str, Any], str]] = None

    @property
    def db_labels(self) -> Dict[str, Any]:
        claims = self.claims if self.claims is not None else []
        return {
            "claims": [x.objHash for x in claims],
            "limits": json.dumps(self.limits),
            "requests": json.dumps(self.requests),
        }
    
    @property
    def referenced_objects(self):
        return self.claims if self.claims is not None else []
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        claims = self.claims if self.claims is not None else []
        return [
            (self, Relationship.DEFINES, i) for i in claims
        ]