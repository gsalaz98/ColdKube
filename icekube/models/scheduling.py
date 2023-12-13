from typing import List, Optional
from icekube.relationships import Relationship
from icekube.models.base import RELATIONSHIP, BaseResource
from icekube.models.node import LabelSelector, NodeSelector, NodeSelectorTerm


class PreferredSchedulingTerm(BaseResource):
    __name__ = "PreferredSchedulingTerm"

    preference: Optional[NodeSelectorTerm] = None
    weight: Optional[int] = None

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            self.preference
        ]
    
    def relationships(self, initial=False) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, self.preference)]

class NodeAffinity(BaseResource):
    __name__ = "NodeAffinity"

    preferredDuringSchedulingIgnoredDuringExecution: Optional[List[PreferredSchedulingTerm]] = None
    requiredDuringSchedulingIgnoredDuringExecution: Optional[NodeSelector] = None

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            *(self.preferredDuringSchedulingIgnoredDuringExecution if self.preferredDuringSchedulingIgnoredDuringExecution else []),
            self.requiredDuringSchedulingIgnoredDuringExecution
        ]
    
    def relationships(self, initial=False) -> List[RELATIONSHIP]:
        ro = self.referenced_objects
        return [(self, Relationship.DEFINES, o) for o in ro]

class PodAffinityTerm(BaseResource):
    __name__ = "PodAffinityTerm"

    labelSelector: Optional[NodeSelector] = None
    namespaceSelector: Optional[LabelSelector] = None
    namespaces: Optional[List[str]] = None
    topologyKey: Optional[str] = None

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            self.labelSelector,
            self.namespaceSelector,
        ]
    
    def relationships(self, initial=False) -> List[RELATIONSHIP]:
        return [
            (self, Relationship.DEFINES, self.labelSelector),
            (self, Relationship.DEFINES, self.namespaceSelector),
        ]

class WeightedPodAffinityTerm(BaseResource):
    __name__ = "WeightedPodAffinityTerm"

    podAffinityTerm: Optional[PodAffinityTerm] = None
    weight: Optional[int] = None

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            self.podAffinityTerm,
        ]
    
    def relationships(self, initial=False) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, self.podAffinityTerm)]

class PodAffinity(BaseResource):
    __name__ = "PodAffinity"

    preferredDuringSchedulingIgnoredDuringExecution: Optional[List[WeightedPodAffinityTerm]] = None
    requiredDuringSchedulingIgnoredDuringExecution: Optional[List[PodAffinityTerm]] = None

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            *(self.preferredDuringSchedulingIgnoredDuringExecution if self.preferredDuringSchedulingIgnoredDuringExecution else []),
            *(self.requiredDuringSchedulingIgnoredDuringExecution if self.requiredDuringSchedulingIgnoredDuringExecution else [])
        ]
    
    def relationships(self, initial=False) -> List[RELATIONSHIP]:
        ro = self.referenced_objects
        return [(self, Relationship.DEFINES, o) for o in ro]

class PodAntiAffinity(BaseResource):
    __name__ = "PodAntiAffinity"

    preferredDuringSchedulingIgnoredDuringExecution: Optional[List[WeightedPodAffinityTerm]] = None
    requiredDuringSchedulingIgnoredDuringExecution: Optional[List[PodAffinityTerm]] = None

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            *(self.preferredDuringSchedulingIgnoredDuringExecution if self.preferredDuringSchedulingIgnoredDuringExecution else []),
            *(self.requiredDuringSchedulingIgnoredDuringExecution if self.requiredDuringSchedulingIgnoredDuringExecution else [])
        ]
    
    def relationships(self, initial=False) -> List[RELATIONSHIP]:
        ro = self.referenced_objects
        return [(self, Relationship.DEFINES, o) for o in ro]

class Affinity(BaseResource):
    __name__ = "Affinity"

    nodeAffinity: Optional[NodeAffinity] = None
    podAffinity: Optional[PodAffinity] = None
    podAntiAffinity: Optional[PodAntiAffinity] = None


    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            self.nodeAffinity,
            self.podAffinity,
            self.podAntiAffinity,
        ]
    
    def relationships(self, initial=False) -> List[RELATIONSHIP]:
        return [
            (self, Relationship.DEFINES, self.nodeAffinity),
            (self, Relationship.DEFINES, self.podAffinity),
            (self, Relationship.DEFINES, self.podAntiAffinity),
        ]