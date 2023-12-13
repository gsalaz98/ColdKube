from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

from icekube.relationships import Relationship
from icekube.models.base import RELATIONSHIP, BaseResource
from icekube.models.metadata import *
from pydantic import BaseModel, Field, root_validator


class Toleration(BaseResource):
    __name__ = "Toleration"

    effect: Optional[str] = None
    key: Optional[str] = None
    operator: Optional[str] = None
    tolerationSeconds: Optional[int] = None
    value: Optional[str] = None

class ResourceClaim(BaseResource):
    __name__ = "ResourceClaim"

    name: Optional[str] = None

class ResourceRequirements(BaseResource):
    __name__ = "ResourceRequirements"

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
    
class ClaimSource(BaseResource):
    __name__ = "ClaimSource"

    # TODO: Add reference for claim template
    resourceClaimName: Optional[str] = None
    resourceClaimTemplateName: Optional[str] = None


class PodResourceClaim(BaseResource):
    __name__ = "PodResourceClaim"

    name: Optional[str] = None
    source: Optional[ClaimSource] = None