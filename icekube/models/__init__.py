from typing import List, Type

from icekube.models.api_resource import APIResource
from icekube.models.base import BaseResource, Resource
from icekube.models.cluster import Cluster
from icekube.models.clusterrole import ClusterRole
from icekube.models.clusterrolebinding import ClusterRoleBinding
from icekube.models.group import Group
from icekube.models.namespace import Namespace
from icekube.models.node import Node, NodeSelector, NodeSelectorRequirement, NodeSelectorTerm, LabelSelector, LabelSelectorRequirement
from icekube.models.storage import PersistentVolume, PersistentVolumeClaim
from icekube.models.pod import Pod
from icekube.models.resources import ResourceRequirements
from icekube.models.role import Role
from icekube.models.rolebinding import RoleBinding
from icekube.models.secret import Secret
from icekube.models.securitycontextconstraints import (
    SecurityContextConstraints,
)
from icekube.models.serviceaccount import ServiceAccount
from icekube.models.signer import Signer
from icekube.models.user import User
from icekube.models.webhooks import *

enumerate_resource_kinds: List[Type[Resource]] = [
    ClusterRole,
    ClusterRoleBinding,
    MutatingWebhookConfiguration,
    Namespace,
    Pod,
    Role,
    RoleBinding,
    Secret,
    SecurityContextConstraints,
    ServiceAccount,
    PersistentVolume,
    PersistentVolumeClaim,
]


# plurals: Dict[str, Type[Resource]] = {x.plural: x for x in enumerate_resource_kinds}


__all__ = [
    "APIResource",
    "Cluster",
    "ClusterRole",
    "ClusterRoleBinding",
    "Group",
    "MutatingWebhookConfiguration",
    "Namespace",
    "PersistentVolume",
    "PersistentVolumeClaim",
    "Pod",
    "Role",
    "RoleBinding",
    "Secret",
    "SecurityContextConstraints",
    "ServiceAccount",
    "Signer",
    "User",
]
