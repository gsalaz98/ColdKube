from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union, cast

from icekube.models.base import RELATIONSHIP, BaseResource, Resource, class_defines_relationships
from icekube.models.metadata import *
from icekube.models.networking import PodIP
from icekube.models.node import Node
from icekube.models.resources import PodResourceClaim, ResourceRequirements, Toleration
from icekube.models.scheduling import Affinity
from icekube.models.secret import EnvVar, Secret
from icekube.models.serviceaccount import ServiceAccount
from icekube.models.storage import Volume, VolumeDevice
from icekube.models.topology import TopologySpreadConstraint
from icekube.relationships import Relationship
from pydantic import root_validator

CAPABILITIES = [
    "AUDIT_CONTROL",
    "AUDIT_READ",
    "AUDIT_WRITE",
    "BLOCK_SUSPEND",
    "BPF",
    "CHECKPOINT_RESTORE",
    "CHOWN",
    "DAC_OVERRIDE",
    "DAC_READ_SEARCH",
    "FOWNER",
    "FSETID",
    "IPC_LOCK",
    "IPC_OWNER",
    "KILL",
    "LEASE",
    "LINUX_IMMUTABLE",
    "MAC_ADMIN",
    "MAC_OVERRIDE",
    "MKNOD",
    "NET_ADMIN",
    "NET_BIND_SERVICE",
    "NET_BROADCAST",
    "NET_RAW",
    "PERFMON",
    "SETFCAP",
    "SETGID",
    "SETPCAP",
    "SETUID",
    "SYSLOG",
    "SYS_ADMIN",
    "SYS_BOOT",
    "SYS_CHROOT",
    "SYS_MODULE",
    "SYS_NICE",
    "SYS_PACCT",
    "SYS_PTRACE",
    "SYS_RAWIO",
    "SYS_RESOURCE",
    "SYS_TIME",
    "SYS_TTY_CONFIG",
    "WAKE_ALARM",
]

class ContainerPort(BaseResource):
    __name__ = "ContainerPort"

    containerPort: Optional[int] = None
    hostIP: Optional[str] = None
    hostPort: Optional[int] = None
    name: Optional[str] = None
    protocol: Optional[Union[Literal["TCP"], Literal["UDP"], Literal["SCTP"]]] = None

class ContainerResizePolicy(BaseResource):
    __name__ = "ContainerResizePolicy"

    resourceName: Optional[str] = None
    restartPolicy: Optional[str] = None

class Capabilities(BaseResource):
    __name__ = "Capabilities"

    add: Optional[List[str]] = None
    drop: Optional[List[str]] = None

class SELinuxOptions(BaseResource):
    __name__ = "SELinuxOptions"

    level: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None
    user: Optional[str] = None

class SeccompProfile(BaseResource):
    __name__ = "SeccompProfile"

    localhostProfile: Optional[str] = None
    type: Optional[str] = None

class WindowsSecurityContextOptions(BaseResource):
    __name__ = "WindowsSecurityContextOptions"

    gmsaCredentialSpec: Optional[str] = None
    gmsaCredentialSpecName: Optional[str] = None
    hostProcess: Optional[bool] = None
    runAsUserName: Optional[str] = None

class SecurityContext(BaseResource):
    __name__ = "SecurityContext"

    allowPrivilegeEscalation: Optional[bool] = None
    capabilities: Optional[Capabilities] = None
    privileged: Optional[bool] = None
    procMount: Optional[str] = None
    readOnlyRootFilesystem: Optional[bool] = None
    runAsGroup: Optional[int] = None
    runAsNonRoot: Optional[bool] = None
    runAsUser: Optional[int] = None
    seLinuxOptions: Optional[SELinuxOptions] = None
    seccompOptions: Optional[SeccompProfile] = None
    windowsOptions: Optional[WindowsSecurityContextOptions] = None

class PodCondition(BaseResource):
    __name__ = "PodCondition"

    lastProbeTime: Optional[str] = None
    lastTransitionTime: Optional[str] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None

class ContainerStateRunning(BaseResource):
    __name__ = "ContainerStateRunning"

    startedAt: Optional[str] = None

class ContainerStateTerminated(BaseResource):
    __name__ = "ContainerStateTerminated"

    containerID: Optional[str] = None
    exitCode: Optional[int] = None
    finishedAt: Optional[str] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    signal: Optional[int] = None
    startedAt: Optional[str] = None

class ContainerStateWaiting(BaseResource):
    __name__ = "ContainerStateWaiting"

    message: Optional[str] = None
    reason: Optional[str] = None

class ContainerState(BaseResource):
    __name__ = "ContainerState"

    running: Optional[ContainerStateRunning] = None
    terminated: Optional[ContainerStateTerminated] = None
    waiting: Optional[ContainerStateWaiting] = None

class ContainerStatus(BaseResource):
    __name__ = "ContainerStatus"

    allocatedResources: Optional[Union[Dict[str, Any], str]] = None
    containerID: Optional[str] = None
    image: Optional[str] = None
    imageID: Optional[str] = None
    lastState: Optional[ContainerState] = None
    name: Optional[str] = None
    ready: Optional[bool] = None
    resources: Optional[ResourceRequirements] = None
    restartCount: Optional[int] = None
    started: Optional[bool] = None
    state: Optional[ContainerState] = None



class PodStatus(BaseResource):
    __name__ = "PodStatus"

    conditions: Optional[List[PodCondition]] = None
    containerStatuses: Optional[List[ContainerStatus]] = None
    ephemeralContainerStatuses: Optional[List[ContainerStatus]] = None
    hostIP: Optional[str] = None
    initContainerStatuses: Optional[List[ContainerStatus]] = None
    message: Optional[str] = None
    nominatedNodeName: Optional[str] = None
    phase: Optional[str] = None
    podIP: Optional[str] = None
    podIPs: Optional[List[PodIP]] = None
    qosClass: Optional[str] = None
    reason: Optional[str] = None
    resize: Optional[str] = None
    startTime: Optional[str] = None


class Container(BaseResource):
    __name__ = "Container"

    args: Optional[List[str]] = None
    command: Optional[List[str]] = None
    env: Optional[List[EnvVar]] = None
    envFrom: Optional[List[EnvVarSource]] = None
    image: Optional[str] = None
    imagePullPolicy: Optional[Union[Literal["Always"], Literal["IfNotPresent"], Literal["Never"]]] = None
    lifecycle: Optional[Lifecycle] = None
    livenessProbe: Optional[Probe] = None
    name: Optional[str] = None
    ports: Optional[List[ContainerPort]] = None
    readinessProbe: Optional[Probe] = None
    resizePolicy: Optional[ContainerResizePolicy] = None
    resources: Optional[ResourceRequirements] = None
    securityContext: Optional[SecurityContext] = None
    startupProbe: Optional[Probe] = None
    stdin: Optional[bool] = None
    stdinOnce: Optional[bool] = None
    terminationMessagePath: Optional[str] = None
    terminationMessagePolicy: Optional[Union[Literal["File"], Literal["FallbackToLogsOnError"]]] = None
    tty: Optional[bool] = None
    volumeDevices: Optional[List[VolumeDevice]] = None
    volumeMounts: Optional[List[VolumeDevice]] = None
    workingDir: Optional[str] = None

    @root_validator(pre=True)
    def extract_values(cls, values):
        values["env"] = [EnvVar(**i) for i in (values.get("env"))] if values.get("env") is not None else None
        values["envFrom"] = [EnvVarSource(**i) for i in (values.get("envFrom"))] if values.get("envFrom") is not None else None
        values["lifecycle"] = Lifecycle(**values.get("lifecycle")) if values.get("lifecycle") is not None else None
        values["livenessProbe"] = Probe(**values.get("livenessProbe")) if values.get("livenessProbe") is not None else None
        values["ports"] = [ContainerPort(**i) for i in (values.get("ports"))] if values.get("ports") is not None else None
        values["readinessProbe"] = Probe(**values.get("readinessProbe")) if values.get("readinessProbe") is not None else None
        values["resizePolicy"] = ContainerResizePolicy(**values.get("resizePolicy")) if values.get("resizePolicy") is not None else None
        values["resources"] = ResourceRequirements(**values.get("resources")) if values.get("resources") is not None else None
        values["securityContext"] = SecurityContext(**values.get("securityContext")) if values.get("securityContext") is not None else None
        values["startupProbe"] = Probe(**values.get("startupProbe")) if values.get("startupProbe") is not None else None
        values["volumeDevices"] = [VolumeDevice(**i) for i in (values.get("volumeDevices"))] if values.get("volumeDevices") is not None else None
        values["volumeMounts"] = [VolumeDevice(**i) for i in (values.get("volumeMounts"))] if values.get("volumeMounts") is not None else None

        return values

class PodDNSConfigOption(BaseResource):
    __name__ = "PodDNSConfigOption"

    name: Optional[str] = None
    value: Optional[str] = None

class EphemeralContainer(BaseResource):
    __name__ = "EphemeralContainer"

    args: Optional[List[str]] = None
    command: Optional[List[str]] = None
    env: Optional[List[EnvVar]] = None
    envFrom: Optional[List[EnvVarSource]] = None
    image: Optional[str] = None
    imagePullPolicy: Optional[Union[Literal["Always"], Literal["IfNotPresent"], Literal["Never"]]] = None
    lifecycle: Optional[Lifecycle] = None
    livenessProbe: Optional[Probe] = None
    name: Optional[str] = None
    ports: Optional[List[ContainerPort]] = None
    readinessProbe: Optional[Probe] = None
    resizePolicy: Optional[ContainerResizePolicy] = None
    resources: Optional[ResourceRequirements] = None
    securityContext: Optional[SecurityContext] = None
    startupProbe: Optional[Probe] = None
    stdin: Optional[bool] = None
    stdinOnce: Optional[bool] = None
    terminationMessagePath: Optional[str] = None
    terminationMessagePolicy: Optional[Union[Literal["File"], Literal["FallbackToLogsOnError"]]] = None
    tty: Optional[bool] = None
    volumeDevices: Optional[List[VolumeDevice]] = None
    volumeMounts: Optional[List[VolumeDevice]] = None
    workingDir: Optional[str] = None

class PodDNSConfig(BaseResource):
    __name__ = "PodDNSConfig"

    nameservers: Optional[List[str]] = None
    options: Optional[List[PodDNSConfigOption]] = None
    searches: Optional[List[str]] = None

class HostAlias(BaseResource):
    __name__ = "HostAlias"

    hostnames: Optional[List[str]] = None
    ip: Optional[str] = None

class PodOS(BaseResource):
    __name__ = "PodOS"

    name: Optional[str] = None

class PodReadinessGate(BaseResource):
    __name__ = "PodReadinessGate"

    conditionType: Optional[str] = None

class PodSchedulingGate(BaseResource):
    __name__ = "PodSchedulingGate"

    name: Optional[str] = None

class Sysctl(BaseResource):
    __name__ = "Sysctl"

    name: Optional[str] = None
    value: Optional[str] = None

class PodSecurityContext(BaseResource):
    __name__ = "PodSecurityContext"

    fsGroup: Optional[int] = None
    fsGroupChangePolicy: Optional[str] = None
    runAsGroup: Optional[int] = None
    runAsNonRoot: Optional[bool] = None
    runAsUser: Optional[int] = None
    seLinuxOptions: Optional[SELinuxOptions] = None
    seccompProfile: Optional[SeccompProfile] = None
    supplementalGroups: Optional[List[int]] = None
    sysctls: Optional[List[Sysctl]] = None
    windowsOptions: Optional[WindowsSecurityContextOptions] = None

    @root_validator(pre=True)
    def extract_values(cls, values):
        values["seLinuxOptions"] = SELinuxOptions(**values.get("seLinuxOptions")) if values.get("seLinuxOptions") is not None else None
        values["seccompProfile"] = SeccompProfile(**values.get("seccompProfile")) if values.get("seccompProfile") is not None else None
        values["sysctls"] = [Sysctl(**i) for i in (values.get("sysctls"))] if values.get("sysctls") is not None else None
        values["windowsOptions"] = WindowsSecurityContextOptions(**values.get("windowsOptions")) if values.get("windowsOptions") is not None else None
        return values

    @property
    def db_labels(self):
        return {
            "fsGroup": self.fsGroup,
            "fsGroupChangePolicy": self.fsGroupChangePolicy,
            "runAsGroup": self.runAsGroup,
            "runAsNonRoot": self.runAsNonRoot,
            "runAsUser": self.runAsUser,
            "seLinuxOptions": self.seLinuxOptions.objHash if self.seLinuxOptions is not None else None,
            "seccompProfile": self.seccompProfile.objHash if self.seccompProfile is not None else None,
            "supplementalGroups": self.supplementalGroups,
            "sysctls": [i.objHash for i in self.sysctls] if self.sysctls is not None else None,
            "windowsOptions": self.windowsOptions.objHash if self.windowsOptions is not None else None
        }
    
    @property
    def referenced_objects(self):
        return [
            self.seLinuxOptions,
            self.seccompProfile,
            *(self.sysctls if self.sysctls is not None else []),
            self.windowsOptions
        ]

class Pod(Resource):
    __name__ = "Pod"

    apiVersion: str = "v1"
    metadata: Optional[ObjectMeta] = None
    kind: str = "Pod"

    activeDeadlineSeconds: Optional[int] = None
    affinity: Optional[Affinity] = None
    automountServiceAccountToken: Optional[bool] = None
    containers: Optional[List[Container]] = None
    dnsConfig: Optional[PodDNSConfig] = None
    dnsPolicy: Optional[str] = None
    enableServiceLinks: Optional[bool] = None
    ephemeralContainers: Optional[List[EphemeralContainer]] = None
    hostAlias: Optional[List[HostAlias]] = None
    hostIPC: Optional[bool] = None
    hostNetwork: Optional[bool] = None
    hostPID: Optional[bool] = None
    hostUsers: Optional[bool] = None
    hostname: Optional[str] = None
    imagePullSecrets: Optional[List[LocalObjectReference]] = None
    initContainers: Optional[List[Container]] = None
    nodeName: Optional[str] = None
    nodeSelector: Optional[Union[Dict[str, str], str]] = None
    os: Optional[PodOS] = None
    overhead: Optional[Union[Dict[str, Any], str]] = None
    preemptionPolicy: Optional[str] = None
    priority: Optional[int] = None
    # TODO: add PriorityClass reference
    priorityClassName: Optional[str] = None
    readinessGates: Optional[List[PodReadinessGate]] = None
    resourceClaims: Optional[List[PodResourceClaim]] = None
    restartPolicy: Optional[Union[Literal["Always"], Literal["OnFailure"], Literal["Never"]]] = None
    runtimeClassName: Optional[str] = None
    schedulerName: Optional[str] = None
    schedulingGates: Optional[List[PodSchedulingGate]] = None
    securityContext: Optional[PodSecurityContext] = None
    serviceAccount: Optional[str] = None
    serviceAccountName: Optional[str] = None
    setHostnameAsFQDN: Optional[bool] = None
    shareProcessNamespace: Optional[bool] = None
    subdomain: Optional[str] = None
    terminationGracePeriodSeconds: Optional[int] = None
    tolerations: Optional[List[Toleration]] = None
    topologySpreadConstraints: Optional[List[TopologySpreadConstraint]] = None
    volumes: Optional[List[Volume]] = None

    status: Optional[PodStatus] = None

    @root_validator(pre=True)
    def extract_values(cls, values):
        raw = json.loads(values.get("raw")) if values.get("raw") is not None else None
        if raw is None:
            raw = values
            values["raw"] = json.dumps(raw)

        metadata = raw.get("metadata", {})
        spec = raw.get("spec", {})
        status = raw.get("status")

        values["metadata"] = ObjectMeta(**metadata) if metadata is not None else None
        values["name"] = metadata.get("name")
        values["namespace"] = metadata.get("namespace")

        values["affinity"] = Affinity(**spec.get("affinity")) if spec.get("affinity") is not None else None
        values["containers"] = [Container(**i) for i in (spec.get("containers"))] if spec.get("containers") is not None else None
        values["dnsConfig"] = PodDNSConfig(**spec.get("dnsConfig")) if spec.get("dnsConfig") is not None else None
        values["ephemeralContainers"] = [EphemeralContainer(**i) for i in (spec.get("ephemeralContainers"))] if spec.get("ephemeralContainers") is not None else None
        values["hostAlias"] = [HostAlias(**i) for i in (spec.get("hostAlias"))] if spec.get("hostAlias") is not None else None
        values["imagePullSecrets"] = [LocalObjectReference(**i) for i in (spec.get("imagePullSecrets"))] if spec.get("imagePullSecrets") is not None else None
        values["initContainers"] = [Container(**i) for i in (spec.get("initContainers"))] if spec.get("initContainers") is not None else None
        values["os"] = PodOS(**spec.get("os")) if spec.get("os") is not None else None
        values["readinessGates"] = [PodReadinessGate(**i) for i in (spec.get("readinessGates"))] if spec.get("readinessGates") is not None else None
        values["resourceClaims"] = [PodResourceClaim(**i) for i in (spec.get("resourceClaims"))] if spec.get("resourceClaims") is not None else None
        values["schedulingGates"] = [PodSchedulingGate(**i) for i in (spec.get("schedulingGates"))] if spec.get("schedulingGates") is not None else None
        values["securityContext"] = PodSecurityContext(**spec.get("securityContext")) if spec.get("securityContext") is not None and spec.get("securityContext") != {} else None
        values["resourceClaims"] = [PodResourceClaim(**i) for i in (spec.get("resourceClaims"))] if spec.get("resourceClaims") is not None else None
        values["tolerations"] = [Toleration(**i) for i in (spec.get("tolerations"))] if spec.get("tolerations") is not None else None
        values["topologySpreadConstraints"] = [TopologySpreadConstraint(**i) for i in (spec.get("topologySpreadConstraints", []))] if spec.get("topologySpreadConstraints") is not None else None
        values["volumes"] = [Volume(namespace=values["namespace"], **i) for i in (spec.get("volumes"))] if spec.get("volumes") is not None else None
        values["status"] = PodStatus(**status) if status is not None else None
        
        return values

    @property
    def db_labels(self):
        return {
            "name": self.name,
            "namespace": self.namespace,
            "metadata": self.metadata.objHash if self.metadata is not None else None,
            "raw": self.raw,

            "activeDeadlineSeconds": self.activeDeadlineSeconds,
            "affinity": self.affinity.objHash if self.affinity is not None else None,
            "automountServiceAccountToken": self.automountServiceAccountToken,
            "containers": [i.objHash for i in self.containers] if self.containers is not None else None,
            "dnsConfig": [i.objHash for i in self.dnsConfig] if self.dnsConfig is not None else None,
            "dnsPolicy": self.dnsPolicy,
            "enableServiceLinks": self.enableServiceLinks,
            "ephemeralContainers": [i.objHash for i in self.ephemeralContainers] if self.ephemeralContainers is not None else None,
            "hostAlias": [i.objHash for i in self.hostAlias] if self.hostAlias is not None else None,
            "hostIPC": self.hostIPC,
            "hostNetwork": self.hostNetwork,
            "hostPID": self.hostPID,
            "hostUsers": self.hostUsers,
            "hostname": self.hostname,
            "imagePullSecrets": [i.objHash for i in self.imagePullSecrets] if self.imagePullSecrets is not None else None,
            "initContainers": [i.objHash for i in self.initContainers] if self.initContainers is not None else None,
            "nodeName": self.nodeName,
            "nodeSelector": json.dumps(self.nodeSelector),
            "os": self.os.objHash if self.os is not None else None,
            "overhead": json.dumps(self.overhead),
            "preemptionPolicy": self.preemptionPolicy,
            "priority": self.priority,
            "priorityClassName": self.priorityClassName,
            "readinessGates": [i.objHash for i in self.readinessGates] if self.readinessGates is not None else None,
            "resourceClaims": [i.objHash for i in self.resourceClaims] if self.resourceClaims is not None else None,
            "restartPolicy": self.restartPolicy,
            "runtimeClassName": self.runtimeClassName,
            "schedulerName": self.schedulerName,
            "schedulingGates": [i.objHash for i in self.schedulingGates] if self.schedulingGates is not None else None,
            "securityContext": self.securityContext.objHash if self.securityContext is not None else None,
            "serviceAccount": self.serviceAccount,
            "serviceAccountName": self.serviceAccountName,
            "setHostnameAsFQDN": self.setHostnameAsFQDN,
            "shareProcessNamespace": self.shareProcessNamespace,
            "subdomain": self.subdomain,
            "terminationGracePeriodSeconds": [i.objHash for i in self.terminationGracePeriodSeconds] if self.terminationGracePeriodSeconds is not None else None,
            "tolerations": [i.objHash for i in self.tolerations] if self.tolerations is not None else None,
            "topologySpreadConstraints": [i.objHash for i in self.topologySpreadConstraints] if self.topologySpreadConstraints is not None else None,
            "volumes": [i.objHash for i in self.volumes] if self.volumes is not None else None,
            "status": self.status.objHash if self.status is not None else None
        }

    @property
    def referenced_objects(self):
        return [
            self.metadata,
            self.affinity,
            *(self.containers if self.containers is not None else []),
            self.dnsConfig,
            *(self.ephemeralContainers if self.ephemeralContainers is not None else []),
            *(self.hostAlias if self.hostAlias is not None else []),
            *(self.imagePullSecrets if self.imagePullSecrets is not None else []),
            *(self.initContainers if self.initContainers is not None else []),
            self.os,
            *(self.readinessGates if self.readinessGates is not None else []),
            *(self.resourceClaims if self.resourceClaims is not None else []),
            *(self.schedulingGates if self.schedulingGates is not None else []),
            self.securityContext,
            *(self.resourceClaims if self.resourceClaims is not None else []),
            *(self.tolerations if self.tolerations is not None else []),
            *(self.topologySpreadConstraints if self.topologySpreadConstraints is not None else []),
            *(self.volumes if self.volumes  is not None else []),
            self.status
        ]

    @property
    def dangerous_host_path(self) -> bool:
        # Dangerous paths to check for
        # Not all of these give direct node compromise, but will grant enough
        # permissions to maybe steal certificates to help with API server
        # as the node, or the like
        dangerous_paths = [
            "/etc/kubernetes/admin.conf",
            "/etc/kubernetes/kubeconfig",
            "/etc/shadow",
            "/proc/sys/kernel",
            "/root/.kube/config",
            "/root/.ssh/authorized_keys",
            "/run/containerd/containerd.sock",
            "/run/containerd/containerd.sock",
            "/run/crio/crio.sock",
            "/run/cri-dockerd.sock",
            "/run/docker.sock",
            "/run/dockershim.sock",
            "/var/lib/kubelet/pods/",
            "/var/lib/kubernetes/",
            "/var/lib/minikube/certs/apiserver.key",
            "/var/log",
            "/var/run/containerd/containerd.sock",
            "/var/run/containerd/containerd.sock",
            "/var/run/crio/crio.sock",
            "/var/run/cri-dockerd.sock",
            "/var/run/docker.sock",
            "/var/run/dockershim.sock",
        ]
        for volume, test_path in product(self.host_path_volumes, dangerous_paths):
            try:
                Path(test_path).relative_to(Path(volume))
                return True
            except ValueError:
                pass
        return False

    @property
    def mounted_secrets(self) -> List[str]:
        if self.raw:
            data = json.loads(self.raw)
        else:
            return []

        secrets = []

        volumes = data.get("spec", {}).get("volumes") or []

        for volume in volumes:
            if volume.get("secret"):
                secrets.append(volume["secret"]["secretName"])

        for container in data.get("spec", {}).get("containers") or []:
            if not container.get("env"):
                continue
            for env in container["env"]:
                try:
                    secrets.append(env["valueFrom"]["secretKeyRef"]["name"])
                except (KeyError, TypeError):
                    pass

        return secrets

    def relationships(self, initial: bool = True) -> List[RELATIONSHIP]:
        relationships = class_defines_relationships(self)
        relationships += super().relationships(initial=initial)

        node = Node(name=self.nodeName) if self.nodeName is not None else None
        sa = self.serviceAccountName if self.serviceAccountName is not None else self.serviceAccount
        if sa is not None:
            serviceAccount = ServiceAccount(name=sa, namespace=self.namespace) 
            relationships += [(self, Relationship.USES_ACCOUNT, serviceAccount)]
        if node:
            relationships += [(node, Relationship.HOSTS_POD, self)]
        for secret in self.mounted_secrets:
            relationships += [
                (
                    self,
                    Relationship.MOUNTS_SECRET,
                    Secret(namespace=self.namespace, name=secret),
                )
            ]

        return relationships