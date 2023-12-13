from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union
from icekube.models.pod import ObjectFieldSelector, ResourceFieldSelector
from icekube.models.resources import ResourceRequirements
from icekube.models.secret import Secret

from icekube.relationships import Relationship
from icekube.models._helpers import *
from icekube.models.base import RELATIONSHIP, BaseResource, Resource
from icekube.models.node import LabelSelector, NodeSelector, TopologySelectorTerm
from icekube.models.metadata import *
from pydantic import BaseModel, Field, root_validator


class AWSElasticBlockSourceVolumeSource(BaseResource):
    __name__ = "AWSElasticBlockStoreVolumeSource"

    fsType: Optional[str] = None
    partition: Optional[int] = None
    readOnly: Optional[bool] = None
    volumeID: Optional[str] = None

class AzureDiskVolumeSource(BaseResource):
    __name__ = "AzureDiskVolumeSource"

    cachingMode: Optional[str] = None
    diskName: Optional[str] = None
    diskURI: Optional[str] = None
    fsType: Optional[str] = None
    kind: Optional[str] = None
    readOnly: Optional[bool] = None

class AzureFilePersistentVolumeSource(BaseResource):
    __name__ = "AzureFilePersistentVolumeSource"

    readOnly: Optional[bool] = None
    secretName: Optional[str] = None
    secretNamespace: Optional[str] = None
    shareName: Optional[str] = None

class CephFSPersistentVolumeSource(BaseResource):
    __name__ = "CephFSPersistentVolumeSource"

    monitors: List[str] = []
    path: Optional[str] = None
    readOnly: Optional[bool] = None
    secretFile: Optional[str] = None
    secretRef: Optional[Union[SecretReference, str]] = None
    user: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]

class CinderPersistentVolumeSource(BaseResource):
    __name__ = "CinderPersistentVolumeSource"

    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[SecretReference, str]] = None
    volumeID: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class CSIPersistentVolumeSource(BaseResource):
    __name__ = "CSIPersistentVolumeSource"

    controllerExpandSecretRef: Optional[Union[SecretReference, str]] = None
    controllerPublishSecretRef: Optional[Union[SecretReference, str]] = None
    driver: Optional[str] = None
    fsType: Optional[str] = None
    nodeExpandSecretRef: Optional[Union[SecretReference, str]] = None
    nodePublishSecretRef: Optional[Union[SecretReference, str]] = None
    nodeStageSecretRef: Optional[Union[SecretReference, str]] = None
    readOnly: Optional[bool] = None
    volumeAttributes: Optional[Union[Dict[str, Any], str]] = {}
    volumeHandle: Optional[str] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        values["volumeAttributes"] = json.dumps(values.get("volumeAttributes", {}))

        controllerExpandSecretRef = values.get("controllerExpandSecretRef", None)
        controllerPublishSecretRef = values.get("controllerPublishSecretRef", None)
        nodeExpandSecretRef = values.get("nodeExpandSecretRef", None) 
        nodePublishSecretRef = values.get("nodePublishSecretRef", None)
        nodeStageSecretRef = values.get("nodeStageSecretRef", None)

        if controllerExpandSecretRef is not None:
            values["controllerExpandSecretRef"] = SecretReference(**controllerExpandSecretRef)
        if controllerPublishSecretRef is not None:
            values["controllerPublishSecretRef"] = SecretReference(**controllerPublishSecretRef)
        if nodeExpandSecretRef is not None:
            values["nodeExpandSecretRef"] = SecretReference(**nodeExpandSecretRef)
        if nodePublishSecretRef is not None:
            values["nodePublishSecretRef"] = SecretReference(**nodePublishSecretRef)
        if nodeStageSecretRef is not None:
            values["nodeStageSecretRef"] = SecretReference(**nodeStageSecretRef)

        return values

    @property
    def referenced_objects(self):
        return [
            self.controllerExpandSecretRef,
            self.controllerPublishSecretRef,
            self.nodeExpandSecretRef,
            self.nodePublishSecretRef,
            self.nodeStageSecretRef
        ]
    
class FCVolumeSource(BaseResource):
    __name__ = "FCVolumeSource"

    fsType: Optional[str] = None
    lun: Optional[int] = None
    readOnly: Optional[bool] = None
    targetWWNs: List[str] = []
    wwids: List[str] = []

class FlexPersistentVolumeSource(BaseResource):
    __name__ = "FlexPersistentVolumeSource"

    driver: Optional[str] = None
    fsType: Optional[str] = None
    options: Dict[str, Any] = {}
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[SecretReference, str]] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]

class FlockerVolumeSource(BaseResource):
    __name__ = "FlockerVolumeSource"

    datasetName: Optional[str] = None
    datasetUUID: Optional[str] = None

class GCEPersistentDiskVolumeSource(BaseResource):
    __name__ = "GCEPersistentDiskVolumeSource"

    fsType: Optional[str] = None
    partition: Optional[int] = None
    pdName: Optional[str] = None
    readOnly: Optional[bool] = None

class GlusterfsPersistentVolumeSource(BaseResource):
    __name__ = "GlusterfsPersistentVolumeSource"

    endpoints: Optional[str] = None
    endpointsNamespace: Optional[str] = None
    path: Optional[str] = None
    readOnly: Optional[bool] = None

class HostPathVolumeSource(BaseResource):
    __name__ = "HostPathVolumeSource"

    path: Optional[str] = None
    type: Optional[str] = None

class ISCSIPersistentVolumeSource(BaseResource):
    __name__ = "ISCSIPersistentVolumeSource"

    chapAuthDiscovery: Optional[bool] = None
    chapAuthSession: Optional[bool] = None
    fsType: Optional[str] = None
    initiatorName: Optional[str] = None
    iqn: Optional[str] = None
    iscsiInterface: Optional[str] = None
    lun: Optional[int] = None
    portals: Optional[List[str]] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[SecretReference, str]] = None
    targetPortal: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class LocalVolumeSource(BaseResource):
    __name__ = "LocalVolumeSource"

    fsType: Optional[str] = None
    path: Optional[str] = None

class NFSVolumeSource(BaseResource):
    __name__ = "NFSVolumeSource"

    path: Optional[str] = None
    readOnly: Optional[bool] = None
    server: Optional[str] = None

class VolumeNodeAffinity(BaseResource):
    __name__ = "VolumeNodeAffinity"

    required: NodeSelector

    @property
    def referenced_objects(self):
        return [
            self.required
        ]

class PhotonPersistentDiskVolumeSource(BaseResource):
    __name__ = "PhotonPersistentDiskVolumeSource"

    fsType: Optional[str] = None
    pdID: Optional[str] = None

class PortworxVolumeSource(BaseResource):
    __name__ = "PortworxVolumeSource"

    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    volumeID: Optional[str] = None

class QuobyteVolumeSource(BaseResource):
    __name__ = "QuobyteVolumeSource"

    group: Optional[str] = None
    readOnly: Optional[bool] = None
    registry: Optional[str] = None
    tenant: Optional[str] = None
    user: Optional[str] = None
    volume: Optional[str] = None

class RBDPersistentVolumeSource(BaseResource):
    __name__ = "RBDPersistentVolumeSource"

    fsType: Optional[str] = None
    image: Optional[str] = None
    keyring: Optional[str] = None
    monitors: Optional[List[str]] = None
    pool: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[SecretReference, str]] = None
    user: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class ScaleIOPersistentVolumeSource(BaseResource):
    __name__ = "ScaleIOPersistentVolumeSource"

    fsType: Optional[str] = None
    gateway: Optional[str] = None
    protectionDomain: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[SecretReference, str]] = None
    sslEnabled: Optional[bool] = None
    storageMode: Optional[str] = None
    storagePool: Optional[str] = None
    system: Optional[str] = None
    volumeName: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class StorageOSPersistentVolumeSource(BaseResource):
    __name__ = "StorageOSPersistentVolumeSource"

    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[ObjectReference, str]] = None
    volumeName: Optional[str] = None
    volumeNamespace: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class VsphereVirtualDiskVolumeSource(BaseResource):
    __name__ = "VsphereVirtualDiskVolumeSource"

    fsType: Optional[str] = None
    storagePolicyID: Optional[str] = None
    storagePolicyName: Optional[str] = None
    volumePath: Optional[str] = None

class VolumeDevice(BaseResource):
    __name__ = "VolumeDevice"

    devicePath: Optional[str] = None
    name: Optional[str] = None

class StorageClass(Resource):
    __name__ = "StorageClass"

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "StorageClass"
    namespace: Optional[str] = None
    metadata: Optional[ObjectMeta] = None

    allowVolumeExpansion: Optional[bool] = None
    allowedTopologies: Optional[List[TopologySelectorTerm]] = None

    apiVersion: Optional[str] = None
    kind: Optional[str] = None
    metadata: Optional[ObjectMeta] = None
    mountOptions: Optional[List[str]] = None
    provisioner: Optional[str] = None
    reclaimPolicy: Optional[str] = None
    volumeBindingMode: Optional[str] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        metadata = json.loads(values.get("raw", "{}")).get("metadata", {})
        spec = json.loads(values.get("raw", "{}")).get("spec", {})

        values["metadata"] = ObjectMeta(**metadata)
        values["allowedTopologies"] = [TopologySelectorTerm(**i) for i in spec.get("allowedTopologies", [])]

        return values
    
    @property
    def referenced_objects(self):
        return [
            self.metadata,
            *self.allowedTopologies
        ]
    
class AzureFileVolumeSource(BaseResource):
    __name__ = "AzureFileVolumeSource"

    fsType: Optional[str] = None
    partition: Optional[int] = None
    readonly: Optional[bool] = None
    volumeID: Optional[str] = None

class CephFSVolumeSource(BaseResource):
    __name__ = "CephFSVolumeSource"

    monitors: List[str] = []
    path: Optional[str] = None
    readOnly: Optional[bool] = None
    secretFile: Optional[str] = None
    secretRef: Optional[Union[LocalObjectReference, str]] = None
    user: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class CinderVolumeSource(BaseResource):
    __name__ = "CinderVolumeSource"

    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[LocalObjectReference, str]] = None
    volumeID: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class ConfigMapVolumeSource(BaseResource):
    __name__ = "ConfigMapVolumeSource"

    defaultMode: Optional[int] = None
    items: Optional[List[KeyToPath]] = None
    name: Optional[str] = None
    optional: Optional[bool] = None

    @property
    def referenced_objects(self):
        return [
            *self.items
        ]
    
class CSIVolumeSource(BaseResource):
    __name__ = "CSIVolumeSource"

    driver: Optional[str] = None
    fsType: Optional[str] = None
    nodePublishSecretRef: Optional[Union[LocalObjectReference, str]] = None
    readOnly: Optional[bool] = None
    volumeAttributes: Optional[Union[Dict[str, Any], str]] = {}

class DownwardAPIVolumeFile(BaseResource):
    __name__ = "DownwardAPIVolumeFile"

    fieldRef: Optional[ObjectFieldSelector] = None
    mode: Optional[int] = None
    path: Optional[str] = None
    resourceFieldRef: Optional[ResourceFieldSelector] = None

    @property
    def referenced_objects(self):
        return [
            self.fieldRef,
            self.resourceFieldRef
        ]

class DownwardAPIVolumeSource(BaseResource):
    __name__ = "DownwardAPIVolumeSource"

    defaultMode: Optional[int] = None
    items: Optional[List[DownwardAPIVolumeFile]] = None

    @property
    def referenced_objects(self):
        return [
            *self.items
        ]
    
class EmptyDirVolumeSource(BaseResource):
    __name__ = "EmptyDirVolumeSource"

    medium: Optional[str] = None
    sizeLimit: Optional[str] = None

def FCVolumeSource(BaseResource):
    __name__ = "FCVolumeSource"

    fsType: Optional[str] = None
    lun: Optional[int] = None
    readOnly: Optional[bool] = None
    targetWWNs: Optional[List[str]] = None
    wwids: Optional[List[str]] = None

class FlexVolumeSource(BaseResource):
    __name__ = "FlexVolumeSource"

    driver: Optional[str] = None
    fsType: Optional[str] = None
    options: Optional[Union[Dict[str, Any], str]] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[LocalObjectReference, str]] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]

class GitRepoVolumeSource(BaseResource):
    __name__ = "GitRepoVolumeSource"

    directory: Optional[str] = None
    repository: Optional[str] = None
    revision: Optional[str] = None

class GlusterfsVolumeSource(BaseResource):
    __name__ = "GlusterfsVolumeSource"

    endpoints: Optional[str] = None
    path: Optional[str] = None
    readOnly: Optional[bool] = None

class ISCSIVolumeSource(BaseResource):
    __name__ = "ISCSIVolumeSource"

    chapAuthDiscovery: Optional[bool] = None
    chapAuthSession: Optional[bool] = None
    fsType: Optional[str] = None
    initiatorName: Optional[str] = None
    iqn: Optional[str] = None
    iscsiInterface: Optional[str] = None
    lun: Optional[int] = None
    portals: Optional[List[str]] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[LocalObjectReference, str]] = None
    targetPortal: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class PersistentVolumeClaimVolumeSource(BaseResource):
    __name__ = "PersistentVolumeClaimSource"

    claimName: Optional[str] = None
    readOnly: Optional[bool] = None

class ConfigMapProjection(BaseResource):
    __name__ = "ConfigMapProjection"

    items: Optional[List[KeyToPath]] = None
    name: Optional[str] = None
    optional: Optional[bool] = None

    @property
    def referenced_objects(self):
        return [
            *self.items
        ]
    
class DownwardAPIProjection(BaseResource):
    __name__ = "DownwardAPIProjection"

    items: Optional[List[DownwardAPIVolumeFile]] = None

    @property
    def referenced_objects(self):
        return [
            *self.items
        ]
    
class SecretProjection(BaseResource):
    __name__ = "SecretProjection"

    items: Optional[List[KeyToPath]] = None
    name: Optional[str] = None
    optional: Optional[bool] = None

    @property
    def referenced_objects(self):
        return [
            *self.items
        ]
    
class ServiceAccountTokenProjection(BaseResource):
    __name__ = "ServiceAccountTokenProjection"

    audience: Optional[str] = None
    expirationSeconds: Optional[int] = None
    path: Optional[str] = None

    
class VolumeProjection(BaseResource):
    configMap: Optional[ConfigMapProjection] = None
    downwardAPI: Optional[DownwardAPIProjection] = None
    secret: Optional[SecretProjection] = None
    serviceAccountToken: Optional[ServiceAccountTokenProjection] = None


class ProjectedVolumeSource(BaseResource):
    __name__ = "ProjectedVolumeSource"

    defaultMode: Optional[int] = None
    sources: Optional[List[VolumeProjection]] = None

    @property
    def referenced_objects(self):
        return [
            *(self.sources if self.sources is not None else [])
        ]
    
class RBDVolumeSource(BaseResource):
    __name__ = "RBDVolumeSource"

    fsType: Optional[str] = None
    image: Optional[str] = None
    keyring: Optional[str] = None
    monitors: Optional[List[str]] = None
    pool: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[LocalObjectReference, str]] = None
    user: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class ScaleIOVolumeSource(BaseResource):
    __name__ = "ScaleIOVolumeSource"

    fsType: Optional[str] = None
    gateway: Optional[str] = None
    protectionDomain: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[LocalObjectReference, str]] = None
    sslEnabled: Optional[bool] = None
    storageMode: Optional[str] = None
    storagePool: Optional[str] = None
    system: Optional[str] = None
    volumeName: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
class StorageOSVolumeSource(BaseResource):
    __name__ = "StorageOSVolumeSource"

    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[LocalObjectReference, str]] = None
    volumeName: Optional[str] = None
    volumeNamespace: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]

class PersistentVolume(Resource):
    __name__ = "PersistentVolume"

    apiVersion: str = "v1"
    kind: str = "PersistentVolume"
    namespace: Optional[str] = None
    metadata: Optional[ObjectMeta] = None

    accessModes: Optional[List[str]] = None
    awsElasticBlockStore: Optional[AWSElasticBlockSourceVolumeSource] = None
    azureDisk: Optional[AzureDiskVolumeSource] = None
    azureFile: Optional[AzureFilePersistentVolumeSource] = None
    capacity: Optional[Union[Dict[str, Any], str]] = None
    cephfs: Optional[CephFSPersistentVolumeSource] = None
    cinder: Optional[CinderPersistentVolumeSource] = None
    claimRef: Optional[Union[ObjectReference, str]] = None
    csi: Optional[CSIPersistentVolumeSource] = None
    fc: Optional[FCVolumeSource] = None
    flexVolume: Optional[FlexPersistentVolumeSource] = None
    flocker: Optional[FlockerVolumeSource] = None
    gcePersistentDisk: Optional[GCEPersistentDiskVolumeSource] = None
    glusterfs: Optional[GlusterfsPersistentVolumeSource] = None
    hostPath: Optional[HostPathVolumeSource] = None
    iscsi: Optional[ISCSIPersistentVolumeSource] = None
    local: Optional[LocalVolumeSource] = None
    mountOptions: Optional[List[str]] = None
    nfs: Optional[NFSVolumeSource] = None
    nodeAffinity: Optional[VolumeNodeAffinity] = None
    persistentVolumeReclaimPolicy: Optional[str] = None
    photonPersistentDisk: Optional[PhotonPersistentDiskVolumeSource] = None
    portworxVolume: Optional[PortworxVolumeSource] = None
    quobyte: Optional[QuobyteVolumeSource] = None
    rbd: Optional[RBDPersistentVolumeSource] = None
    scaleIO: Optional[ScaleIOPersistentVolumeSource] = None
    storageClassName: Optional[str] = None
    storageos: Optional[StorageOSPersistentVolumeSource] = None
    volumeMode: Optional[str] = None
    vsphereVolume: Optional[VsphereVirtualDiskVolumeSource] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        metadata = json.loads(values.get("raw", "{}")).get("metadata", {})
        spec = json.loads(values.get("raw", "{}")).get("spec", {})

        build_default_toplevel_resource(AWSElasticBlockSourceVolumeSource, "awsElasticBlockStore", values, spec)
        build_default_toplevel_resource(AzureDiskVolumeSource, "azureDisk", values, spec)
        build_default_toplevel_resource(AzureFilePersistentVolumeSource, "azureFile", values, spec)
        build_default_toplevel_resource(CephFSPersistentVolumeSource, "cephfs", values, spec)
        build_default_toplevel_resource(CinderPersistentVolumeSource, "cinder", values, spec)
        build_default_toplevel_resource(CSIPersistentVolumeSource, "csi", values, spec)
        build_default_toplevel_resource(FCVolumeSource, "fc", values, spec)
        build_default_toplevel_resource(FlexPersistentVolumeSource, "flexVolume", values, spec)
        build_default_toplevel_resource(FlockerVolumeSource, "flocker", values, spec)
        build_default_toplevel_resource(GCEPersistentDiskVolumeSource, "gcePersistentDisk", values, spec)
        build_default_toplevel_resource(GlusterfsPersistentVolumeSource, "glusterfs", values, spec)
        build_default_toplevel_resource(HostPathVolumeSource, "hostPath", values, spec)
        build_default_toplevel_resource(ISCSIPersistentVolumeSource, "iscsi", values, spec)
        build_default_toplevel_resource(LocalVolumeSource, "local", values, spec)
        build_default_toplevel_resource(NFSVolumeSource, "nfs", values, spec)
        build_default_toplevel_resource(PhotonPersistentDiskVolumeSource, "photonPersistentDisk", values, spec)
        build_default_toplevel_resource(PortworxVolumeSource, "portworxVolume", values, spec)
        build_default_toplevel_resource(QuobyteVolumeSource, "quobyte", values, spec)
        build_default_toplevel_resource(RBDPersistentVolumeSource, "rbd", values, spec)
        build_default_toplevel_resource(ScaleIOPersistentVolumeSource, "scaleIO", values, spec)
        build_default_toplevel_resource(StorageOSPersistentVolumeSource, "storageos", values, spec)
        build_default_toplevel_resource(VsphereVirtualDiskVolumeSource, "vsphereVolume", values, spec)
        build_default_toplevel_resource(VolumeNodeAffinity, "nodeAffinity", values, spec)

        # We define it as a generic dictionary, but we store it in the DB as a string.
        # We need to deserialize it by converting it back into a dictionary when validating.
        capacity = spec.get("capacity")
        if isinstance(capacity, str):
            capacity = json.loads(capacity)

        values["metadata"] = ObjectMeta(**metadata)

        values["capacity"] = capacity
        values["accessModes"] = spec.get("accessModes")
        values["mountOptions"] = spec.get("mountOptions")
        values["persistentVolumeReclaimPolicy"] = spec.get("persistentVolumeReclaimPolicy")
        values["storageClassName"] = spec.get("storageClassName")
        values["volumeMode"] = spec.get("volumeMode")
        
        return values

    @property
    def referenced_objects(self):
        objects = [
            self.metadata,
            self.awsElasticBlockStore,
            self.azureDisk,
            self.azureFile,
            self.cephfs,
            self.cinder,
            self.csi,
            self.fc,
            self.flexVolume,
            self.flocker,
            self.gcePersistentDisk,
            self.glusterfs,
            self.hostPath,
            self.iscsi,
            self.local,
            self.nfs,
            self.photonPersistentDisk,
            self.portworxVolume,
            self.quobyte,
            self.rbd,
            self.scaleIO,
            self.storageos,
            self.vsphereVolume,
            self.nodeAffinity
        ]
        return objects
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find

        # Any None types will be filtered out before insertion
        relationships = [(self, Relationship.DEFINES, i) for i in self.referenced_objects]
        storageclasses = list(find(StorageClass, raw=False, name=self.storageClassName))
        if len(storageclasses) > 0:
            storageclass = storageclasses[0]
            relationships.append((self, Relationship.USES, storageclass))

        return relationships
    
class VolumeMount(BaseResource):
    __name__ = "VolumeMount"

    mountPath: Optional[str] = None
    mountPropagation: Optional[str] = None
    name: Optional[str] = None
    readOnly: Optional[bool] = None
    subPath: Optional[str] = None
    subPathExpr: Optional[str] = None


class PersistentVolumeClaim(Resource):
    __name__ = "PersistentVolumeClaim"

    apiVersion: str = "v1"
    kind: str = "PersistentVolumeClaim"
    metadata: Optional[ObjectMeta] = None

    accessModes: Optional[List[str]] = None
    dataSource: Optional[Union[TypedLocalObjectReference, str]] = None
    dataSourceRef: Optional[Union[TypedObjectReference, str]] = None
    resources: Optional[ResourceRequirements] = None
    labelSelector: Optional[LabelSelector] = None
    storageClassName: Optional[str] = None
    volumeName: Optional[str] = None
    volumeMode: Optional[str] = None

    @root_validator(pre=True)
    def extract_fields(cls, values):
        metadata = json.loads(values.get("raw", "{}")).get("metadata", {})
        spec = json.loads(values.get("raw", "{}")).get("spec", {})

        build_default_toplevel_resource(TypedLocalObjectReference, "dataSource", values, spec)
        build_default_toplevel_resource(TypedObjectReference, "dataSourceRef", values, spec)
        build_default_toplevel_resource(ResourceRequirements, "resources", values, spec)
        build_default_toplevel_resource(LabelSelector, "labelSelector", values, spec)

        values["metadata"] = ObjectMeta(**metadata)
        values["accessModes"] = spec.get("accessModes")
        values["storageClassName"] = spec.get("storageClassName")
        values["volumeName"] = spec.get("volumeName")
        values["volumeMode"] = spec.get("volumeMode")

        return values

    @property
    def referenced_objects(self):
        objects = [
            self.metadata,
            self.dataSource,
            self.dataSourceRef,
            self.resources,
            self.labelSelector
        ]
        return objects

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find
        relationships = BaseResource.relationships(self, initial=initial)
        relationships += super().relationships(initial=initial)

        # Find the PersistentVolume that this PersistentVolumeClaim is bound to
        results = list(find(
            PersistentVolume, 
            raw=False, 
            name=self.volumeName
        ))

        if len(results) != 0:
            pv = results[0]
            relationships += [
                (self, Relationship.CONSUMES, pv) 
            ]

        relationships += [
            (self, Relationship.DEFINES, self.dataSource),
            (self, Relationship.DEFINES, self.dataSourceRef),
            (self, Relationship.DEFINES, self.resources),
            (self, Relationship.DEFINES, self.labelSelector),
        ]

        return relationships
    
class PersistentVolumeClaimTemplate(BaseResource):
    __name__ = "PersistentVolumeClaimTemplate"

    metadata: Optional[ObjectMeta] = None
    spec: Optional[PersistentVolumeClaim] = None


class EphemeralVolumeSource(BaseResource):
    __name__ = "EphemeralVolumeSource"

    volumeClaimTemplate: Optional[PersistentVolumeClaimTemplate] = None

    @property
    def referenced_objects(self):
        return [
            self.volumeClaimTemplate
        ]
    
class Volume(BaseResource):
    __name__ = "Volume"
    namespace: Optional[str] = None

    awsElasticBlockStore: Optional[AWSElasticBlockSourceVolumeSource] = None
    azureDisk: Optional[AzureDiskVolumeSource] = None
    azureFile: Optional[AzureFileVolumeSource] = None
    cephfs: Optional[CephFSVolumeSource] = None
    cinder: Optional[CinderVolumeSource] = None
    configmap: Optional[ConfigMapVolumeSource] = None
    csi: Optional[CSIVolumeSource] = None
    downwardAPI: Optional[DownwardAPIVolumeSource] = None
    emptyDir: Optional[EmptyDirVolumeSource] = None
    ephemeral: Optional[EphemeralVolumeSource] = None
    fc: Optional[FCVolumeSource] = None
    flexVolume: Optional[FlexVolumeSource] = None
    flocker: Optional[FlockerVolumeSource] = None
    gcePersistentDisk: Optional[GCEPersistentDiskVolumeSource] = None
    gitRepo: Optional[GitRepoVolumeSource] = None

    glusterfs: Optional[GlusterfsVolumeSource] = None
    hostPath: Optional[HostPathVolumeSource] = None
    iscsi: Optional[ISCSIVolumeSource] = None
    name: Optional[str] = None
    nfs: Optional[NFSVolumeSource] = None
    persistentVolumeClaim: Optional[PersistentVolumeClaimVolumeSource] = None
    photonPersistentDisk: Optional[PhotonPersistentDiskVolumeSource] = None
    portworxVolume: Optional[PortworxVolumeSource] = None
    projected: Optional[ProjectedVolumeSource] = None
    quobyte: Optional[QuobyteVolumeSource] = None
    rbd: Optional[RBDVolumeSource] = None
    scaleIO: Optional[ScaleIOVolumeSource] = None
    secretName: Optional[str] = None
    storageos: Optional[StorageOSVolumeSource] = None
    vsphereVolume: Optional[VsphereVirtualDiskVolumeSource] = None

    @property
    def referenced_objects(self) -> List[BaseResource | None]:
        return [
            self.awsElasticBlockStore,
            self.azureDisk,
            self.azureFile,
            self.cephfs,
            self.cinder,
            self.configmap,
            self.csi,
            self.downwardAPI,
            self.emptyDir,
            self.ephemeral,
            self.fc,
            self.flexVolume,
            self.flocker,
            self.gcePersistentDisk,
            self.gitRepo,
            self.glusterfs,
            self.hostPath,
            self.iscsi,
            self.nfs,
            self.persistentVolumeClaim,
            self.photonPersistentDisk,
            self.portworxVolume,
            self.projected,
            self.quobyte,
            self.rbd,
            self.scaleIO,
            self.storageos,
            self.vsphereVolume
        ]
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find

        r = [(self, Relationship.DEFINES, i) for i in self.referenced_objects]

        if self.persistentVolumeClaim is not None:
            claim_name = self.persistentVolumeClaim.claimName
            pvcs = find(PersistentVolumeClaim, False, name=claim_name, namespace=self.namespace)
            for pvc in pvcs:
                r.append((self.persistentVolumeClaim, Relationship.REFERENCES, pvc))

        if self.secretName is not None:
            secrets = find(Secret, False, name=self.secretName, namespace=self.namespace)
            for secret in secrets:
                r.append((self, Relationship.REFERENCES, secret))

        return r