from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, cast

from icekube.models.base import RELATIONSHIP, BaseResource, Resource
from icekube.models.metadata import ObjectMeta
from icekube.relationships import Relationship
from pydantic import root_validator


class Secret(Resource):
    __name__ = "Secret"

    name: Optional[str] = None

    metadata: Optional[ObjectMeta] = None
    immutable: Optional[bool] = None
    type: Optional[str] = None

    @root_validator(pre=True)
    def remove_secret_data(cls, values):
        data = json.loads(values.get("raw", "{}"))
        if "data" in data:
            del data["data"]

        values["raw"] = json.dumps(data)
        return values

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        relationships = super().relationships()

        if self.type == "kubernetes.io/service-account-token":
            from icekube.models.serviceaccount import ServiceAccount

            sa = self.metadata.annotations.get("kubernetes.io/service-account.name")
            if sa:
                account = ServiceAccount(
                    name=sa, 
                    namespace=self.namespace
                )
                relationships.append(
                    (
                        self,
                        Relationship.AUTHENTICATION_TOKEN_FOR,
                        account,
                    ),
                )

        return relationships

class EnvVar(BaseResource):
    __name__ = "EnvVar"

    name: Optional[str] = None
    value: Optional[str] = None
    valueFrom: Optional[Secret] = None

    @root_validator(pre=True)
    def extract_values(cls, values):
        try:
            if "valueFrom" in values:
                values["valueFrom"] = Secret(**values["valueFrom"])
            return values
        except Exception as e:
            print(e)
            exit(1)