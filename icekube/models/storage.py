from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union
from icekube.models.resources import ResourceRequirements

from icekube.relationships import Relationship
from icekube.models._helpers import *
from icekube.models.base import RELATIONSHIP, BaseResource, Resource
from icekube.models.node import LabelSelector, NodeSelector, TopologySelectorTerm
from icekube.models.metadata import *
from pydantic import BaseModel, Field, root_validator


class AWSElasticBlockSourceVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "AWSElasticBlockStoreVolumeSource"

    fsType: Optional[str] = None
    partition: Optional[int] = None
    readOnly: Optional[bool] = None
    volumeID: Optional[str] = None

class AzureDiskVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "AzureDiskVolumeSource"

    cachingMode: Optional[str] = None
    diskName: Optional[str] = None
    diskURI: Optional[str] = None
    fsType: Optional[str] = None
    kind: Optional[str] = None
    readOnly: Optional[bool] = None

class AzureFilePersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "AzureFilePersistentVolumeSource"

    readOnly: Optional[bool] = None
    secretName: Optional[str] = None
    secretNamespace: Optional[str] = None
    shareName: Optional[str] = None

class CephFSPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "CephFSPersistentVolumeSource"

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
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class CinderPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "CinderPersistentVolumeSource"

    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: Optional[Union[SecretReference, str]] = None
    volumeID: Optional[str] = None

    @property
    def referenced_objects(self):
        return [
            self.secretRef
        ]
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class CSIPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "CSIPersistentVolumeSource"

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
        spec = json.loads(values.get("raw", "{}")).get("spec", {})

        volumeAttributes = spec.get("volumeAttributes", {})
        values["volumeAttributes"] = json.dumps(volumeAttributes)
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
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class FCVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "FCVolumeSource"

    fsType: Optional[str] = None
    lun: Optional[int] = None
    readOnly: Optional[bool] = None
    targetWWNs: List[str] = []
    wwids: List[str] = []

class FlexPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "FlexPersistentVolumeSource"

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

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class FlockerVolumeSource(BaseResource):
    apiversion: str = "v1"
    kind: str = "FlockerVolumeSource"

    datasetName: Optional[str] = None
    datasetUUID: Optional[str] = None

class GCEPersistentDiskVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "GCEPersistentDiskVolumeSource"

    fsType: Optional[str] = None
    partition: Optional[int] = None
    pdName: Optional[str] = None
    readOnly: Optional[bool] = None

class GlusterfsPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "GlusterfsPersistentVolumeSource"

    endpoints: Optional[str] = None
    endpointsNamespace: Optional[str] = None
    path: Optional[str] = None
    readOnly: Optional[bool] = None

class HostPathVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "HostPathVolumeSource"

    path: Optional[str] = None
    type: Optional[str] = None

class ISCSIPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "ISCSIPersistentVolumeSource"

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
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class LocalVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "LocalVolumeSource"

    fsType: Optional[str] = None
    path: Optional[str] = None

class NFSVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "NFSVolumeSource"

    path: Optional[str] = None
    readOnly: Optional[bool] = None
    server: Optional[str] = None

class VolumeNodeAffinity(BaseResource):
    apiVersion: str = "v1"
    kind: str = "VolumeNodeAffinity"

    required: NodeSelector

    @property
    def referenced_objects(self):
        return [
            self.required
        ]

class PhotonPersistentDiskVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "PhotonPersistentDiskVolumeSource"

    fsType: Optional[str] = None
    pdID: Optional[str] = None

class PortworxVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "PortworxVolumeSource"

    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    volumeID: Optional[str] = None

class QuobyteVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "QuobyteVolumeSource"

    group: Optional[str] = None
    readOnly: Optional[bool] = None
    registry: Optional[str] = None
    tenant: Optional[str] = None
    user: Optional[str] = None
    volume: Optional[str] = None

class RBDPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "RBDPersistentVolumeSource"

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
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class ScaleIOPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "ScaleIOPersistentVolumeSource"

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
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class StorageOSPersistentVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "StorageOSPersistentVolumeSource"

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
    
    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        return [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]


class VsphereVirtualDiskVolumeSource(BaseResource):
    apiVersion: str = "v1"
    kind: str = "VsphereVirtualDiskVolumeSource"

    fsType: Optional[str] = None
    storagePolicyID: Optional[str] = None
    storagePolicyName: Optional[str] = None
    volumePath: Optional[str] = None

class StorageClass(Resource):
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

        values["metadata"] = mock(ObjectMeta, **metadata)
        values["allowedTopologies"] = [mock(TopologySelectorTerm, **i) for i in spec.get("allowedTopologies", [])]

        return values
    
    @property
    def db_labels(self) -> Dict[str, Any]:
        labels = {
            k: (v["objHash"] if v is not None and "objHash" in v else [
                i["objHash"] if i is not None and "objHash" in i else i for i in v
                ] if isinstance(v, list) else v
                ) for k, v in self.model_dump().items()
        }

        return labels
    
    @property
    def referenced_objects(self):
        return [
            self.metadata,
            *self.allowedTopologies
        ]
    

class PersistentVolume(Resource):
    __name__ = "PersistentVolume"

    apiVersion: str = "v1"
    kind: str = "PersistentVolume"

    accessModes: Optional[List[str]] = None
    awsElasticBlockStore: Optional[AWSElasticBlockSourceVolumeSource] = None
    azureDisk: Optional[AzureDiskVolumeSource] = None
    azureFile: Optional[AzureFilePersistentVolumeSource] = None
    capacity: Optional[Dict[str, Any]] = None
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
        spec = json.loads(values.get("raw", "{}")).get("spec", {})

        values = build_default_toplevel_resource(AWSElasticBlockSourceVolumeSource, "awsElasticBlockStore", values, spec)
        values = build_default_toplevel_resource(AzureDiskVolumeSource, "azureDisk", values, spec)
        values = build_default_toplevel_resource(AzureFilePersistentVolumeSource, "azureFile", values, spec)
        values = build_default_toplevel_resource(CephFSPersistentVolumeSource, "cephfs", values, spec)
        values = build_default_toplevel_resource(CinderPersistentVolumeSource, "cinder", values, spec)
        values = build_default_toplevel_resource(CSIPersistentVolumeSource, "csi", values, spec)
        values = build_default_toplevel_resource(FCVolumeSource, "fc", values, spec)
        values = build_default_toplevel_resource(FlexPersistentVolumeSource, "flexVolume", values, spec)
        values = build_default_toplevel_resource(FlockerVolumeSource, "flocker", values, spec)
        values = build_default_toplevel_resource(GCEPersistentDiskVolumeSource, "gcePersistentDisk", values, spec)
        values = build_default_toplevel_resource(GlusterfsPersistentVolumeSource, "glusterfs", values, spec)
        values = build_default_toplevel_resource(HostPathVolumeSource, "hostPath", values, spec)
        values = build_default_toplevel_resource(ISCSIPersistentVolumeSource, "iscsi", values, spec)
        values = build_default_toplevel_resource(LocalVolumeSource, "local", values, spec)
        values = build_default_toplevel_resource(NFSVolumeSource, "nfs", values, spec)
        values = build_default_toplevel_resource(PhotonPersistentDiskVolumeSource, "photonPersistentDisk", values, spec)
        values = build_default_toplevel_resource(PortworxVolumeSource, "portworxVolume", values, spec)
        values = build_default_toplevel_resource(QuobyteVolumeSource, "quobyte", values, spec)
        values = build_default_toplevel_resource(RBDPersistentVolumeSource, "rbd", values, spec)
        values = build_default_toplevel_resource(ScaleIOPersistentVolumeSource, "scaleIO", values, spec)
        values = build_default_toplevel_resource(StorageOSPersistentVolumeSource, "storageos", values, spec)
        values = build_default_toplevel_resource(VsphereVirtualDiskVolumeSource, "vsphereVolume", values, spec)
        values = build_default_toplevel_resource(VolumeNodeAffinity, "nodeAffinity", values, spec)

        values["accessModes"] = spec.get("accessModes")

        # We define it as a generic dictionary, but we store it in the DB as a string.
        # We need to deserialize it by converting it back into a dictionary when validating.
        capacity = spec.get("capacity")
        if capacity is not None and isinstance(capacity, str):
            capacity = json.loads(capacity)

        values["capacity"] = capacity
        values["mountOptions"] = spec.get("mountOptions")
        values["persistentVolumeReclaimPolicy"] = spec.get("persistentVolumeReclaimPolicy")
        values["storageClassName"] = spec.get("storageClassName")
        values["volumeMode"] = spec.get("volumeMode")

        return values

    @property
    def db_labels(self) -> Dict[str, Any]:
        labels = {
            **super().db_labels,
            **{k: (v["objHash"] if v is not None and "objHash" in v else v) for k, v in self.model_dump().items()}
        }

        # No support for Maps in neo4j, so we need to convert capacity to a string
        labels["capacity"] = json.dumps(labels["capacity"])
        return labels
    
    @property
    def referenced_objects(self):
        objects = [
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

        relationships = [(self, Relationship.DEFINES, i) for i in self.referenced_objects if i is not None]
        storageclasses = list(find(StorageClass, raw=False, name=self.storageClassName))
        if len(storageclasses) > 0:
            storageclass = storageclasses[0]
            relationships.append((self, Relationship.USES, storageclass))

        return relationships


class PersistentVolumeClaim(Resource):
    apiVersion: str = "v1"
    kind: str = "PersistentVolumeClaim"

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
        spec = json.loads(values.get("raw", "{}")).get("spec", {})

        values = build_default_toplevel_resource(TypedLocalObjectReference, "dataSource", values, spec)
        values = build_default_toplevel_resource(TypedObjectReference, "dataSourceRef", values, spec)
        values = build_default_toplevel_resource(ResourceRequirements, "resources", values, spec)
        values = build_default_toplevel_resource(LabelSelector, "labelSelector", values, spec)

        values["accessModes"] = spec.get("accessModes")
        values["storageClassName"] = spec.get("storageClassName")
        values["volumeName"] = spec.get("volumeName")
        values["volumeMode"] = spec.get("volumeMode")

        return values

    @property
    def db_labels(self) -> Dict[str, Any]:
        return {
            **super().db_labels,
            **{k: (v["objHash"] if v is not None and "objHash" in v else json.dumps(v) if isinstance(v, dict) else v) for k, v in self.model_dump().items()}
        }
    
    @property
    def referenced_objects(self):
        objects = [
            self.dataSource,
            self.dataSourceRef,
            self.resources,
            self.labelSelector
        ]
        return objects

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        from icekube.neo4j import find

        # Find the PersistentVolume that this PersistentVolumeClaim is bound to
        results = list(find(
            PersistentVolume, 
            raw=False, 
            apiVersion="v1",
            kind="PersistentVolume",
            name=self.volumeName
        ))

        relationships = []

        if len(results) != 0:
            pv = results[0]
            relationships += [
                (self, Relationship.BOUND_TO, pv),
                (self, Relationship.CONSUMES, pv) 
            ]

        relationships += [
            (self, Relationship.DEFINES, self.dataSource),
            (self, Relationship.DEFINES, self.dataSourceRef),
            (self, Relationship.DEFINES, self.resources),
            (self, Relationship.DEFINES, self.labelSelector),
        ]

        return relationships