import json
from typing import Any, Dict, List, Optional
from icekube.models.base import RELATIONSHIP, BaseResource, Resource, class_defines_relationships
from icekube.models.metadata import ObjectMeta
from icekube.models.node import LabelSelector
from icekube.models.pod import Pod
from icekube.relationships import Relationship

from pydantic import root_validator

class RollingUpdateDeployment(BaseResource):
    __name__ = "RollingUpdateDeployment"

    maxSurge: Optional[str] = None
    maxUnavailable: Optional[str] = None

class DeploymentStrategy(BaseResource):
    __name__ = "DeploymentStrategy"

    rollingUpdate: Optional[RollingUpdateDeployment] = None
    type: Optional[str] = None

class DeploymentCondition(BaseResource):
    __name__ = "DeploymentCondition"

    lastTransitionTime: Optional[str] = None
    lastUpdateTime: Optional[str] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None

class PodTemplateSpec(BaseResource):
    __name__ = "PodTemplateSpec"

    metadata: Optional[ObjectMeta] = None
    spec: Optional[Pod] = None

class DeploymentStatus(BaseResource):
    __name__ = "DeploymentStatus"

    availableReplicas: Optional[int] = None
    collisionCount: Optional[int] = None
    conditions: Optional[DeploymentCondition] = None
    observedGeneration: Optional[int] = None
    readyReplicas: Optional[int] = None
    replicas: Optional[int] = None
    unavailableReplicas: Optional[int] = None
    updatedReplicas: Optional[int] = None

class Deployment(Resource):
    __name__ = "Deployment"

    apiVersion: str = "apps/v1"
    kind: str = "Deployment"
    metadata: Optional[ObjectMeta] = None

    minReadySeconds: Optional[int] = None
    paused: Optional[bool] = None
    progressDeadlineSeconds: Optional[int] = None
    replicas: Optional[int] = None
    revisionHistoryLimit: Optional[int] = None
    selector: Optional[LabelSelector] = None
    strategy: Optional[DeploymentStrategy] = None
    template: Optional[PodTemplateSpec] = None

    status: Optional[DeploymentStatus] = None

    @root_validator(pre=True)
    def extract_values(cls, values):
        raw = json.loads(values.get("raw")) if values.get("raw") is not None else None
        if raw is None:
            raw = values
            values["raw"] = json.dumps(raw)

        metadata = raw.get("metadata")
        spec = raw.get("spec")
        if metadata is not None:
            values["metadata"] = ObjectMeta(**metadata)

        if spec is None:
            return values

        values["minReadySeconds"] = spec.get("minReadySeconds")
        values["paused"] = spec.get("paused")
        values["progressDeadlineSeconds"] = spec.get("progressDeadlineSeconds")
        values["replicas"] = spec.get("replicas")
        values["revisionHistoryLimit"] = spec.get("revisionHistoryLimit")
        values["selector"] = LabelSelector(**spec["selector"]) if spec.get("selector") is not None else None
        values["strategy"] = DeploymentStrategy(**values["strategy"]) if values.get("strategy") is not None else None
        values["template"] = PodTemplateSpec(**values["template"]) if values.get("template") is not None else None
        values["status"] = DeploymentStatus(**values["status"]) if values.get("status") is not None else None

        return values
    
    @property
    def db_labels(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.objHash if self.metadata is not None else None,
            "minReadySeconds": self.minReadySeconds,
            "paused": self.paused,
            "progressDeadlineSeconds": self.progressDeadlineSeconds,
            "replicas": self.replicas,
            "revisionHistoryLimit": self.revisionHistoryLimit,
            "selector": self.selector.objHash if self.selector is not None else None,
            "strategy": self.strategy.objHash if self.strategy is not None else None,
            "template": self.template.objHash if self.template is not None else None,
            "status": self.status.objHash if self.status is not None else None,
            "raw": self.raw,
        }
    
    @property
    def referenced_objects(self):
        return [
            self.metadata,
            self.selector,
            self.strategy,
            self.template,
            self.status
        ]

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        relationships = class_defines_relationships(self)
        relationships += super().relationships()

        if self.template is not None:
            relationships += (
                (self, Relationship.OWNS, self.template.spec),
            )

        return relationships