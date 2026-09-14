# My Kubernetes GitOps Repository

This is my personal Kubernetes learning project running on my home infrastructure. I'm using it daily, constantly adding and removing things.

> ⚠️ This repository is **rapidly changing** and also used for testing new ideas and configurations.

## Goals

- ~~Migrate my entire Proxmox homelab into Kubernetes~~
- [x] Rely entirely on GitOps and Infrastructure as Code using [FluxCD](https://fluxcd.io/)
- [x] Keep everything public - use ~~[Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)~~ and [External Secrets](https://external-secrets.io/) with individual SecretStores to protect sensitive data
- [x] Implement a CI/CD pipeline to lint/prettier the configuration files
- [x] Implement [NVIDIA Container Toolkit](https://nvidia.github.io/libnvidia-container/) to run GPU workloads in the cluster
- [ ] Implement [Intel Device Plugin](https://github.com/intel/intel-device-plugins-for-kubernetes/) to run GPU workloads in the cluster
- [x] Make the cluster reachable from the internet while using [PocketID](https://pocketid.com/) to authenticate with passkeys


## Repository Structure

```text
.
├── apps/             # Application deployments 
├── cluster/          # FluxCD bootstrap and cluster-wide configuration
├── databases/        # Database deployments used by applications
├── docs/             # Documentation about architecture, decisions and setup
├── infrastructure/   # Core infrastructure components required for the cluster
├── monitoring/       # Monitoring and observability stack
├── platform/         # Shared platform services used by apps
├── repository/       # External or additional Git repositories referenced by Flux
└── README.md
```




## External Requirements

These components are required outside of the Kubernetes cluster:

1. An SMB server for persistent volumes  
2. A [HashiCorp Vault](https://www.vaultproject.io/) instance for secrets management  
3. [Caddy](https://caddyserver.com/) as a reverse proxy to reach the cluster and other homelab services in the first place
4. A public domain to enable SSL via DNS challenge (in my case Cloudflare + cert-manager)
5. Gitea + runner outside the cluster for various tasks like building Docker images or running Terraform against the HashiCorp Vault

These components are optional:

1. A [private Docker Hub Proxy Cache](https://hub.docker.com/_/registry), so I don't run into the new Docker pull limit when I restart the cluster multiple times.
2. An [S3 compatible storage backend](https://github.com/deuxfleurs-org/garage) for the CloudNative Postgres backups jobs. I'm using Garage with a simple GUI. 

## Homelab Hardware

Currently, the cluster is running on three virtual machines in my three node Proxmox setup:

| Hostname      | Cores | RAM   | GPU       |
|---------------|-------|-------|-----------|
| talos-cp-01   | 10    | 40GB  |           |
| talos-node-01 | 5     | 48GB  | RTX A2000 |
| talos-node-02 | 5     | 48GB  | RTX A2000 |


## Networking

- The cluster runs in an isolated VLAN.
- The support components like SMB, reverse proxy, vault etc. run in the same VLAN.
- ~~All hostnames in this repository are used internally - the cluster is not accessible from the internet.~~
- Selected services are reachable from the internet through Traefik, mTLS and/or authenticated via PocketID.
- [Traefik](https://traefik.io/traefik/) acts as the reverse proxy and handles TLS termination for incoming traffic to the cluster.

## Storage

NFS/SMB storage is not part of this repository:

1. It depends heavily on the specific environment

2. I prefer not to publicly expose my file structure

## Cluster Initialization

The cluster runs on [Talos Linux](https://www.talos.dev/). The Image Factory schematics and the
machine config patches are not part of this repository:

1. They depend heavily on the specific environment

2. I prefer not to publicly expose my infrastructure details

### Install Talos

```bash
talosctl gen config <cluster-name> https://<controlplane-ip>:6443 \
  --config-patch @patch-all.yaml \
  --config-patch-control-plane @patch-controlplane.yaml \
  --config-patch-worker @patch-worker.yaml

talosctl apply-config --insecure -n <controlplane-ip> --file controlplane.yaml
talosctl apply-config --insecure -n <node-ip> --file worker.yaml

talosctl bootstrap -n <controlplane-ip>
talosctl kubeconfig -n <controlplane-ip>
```

### Install Cilium (once, adopted by Flux afterwards)

Talos ships without CNI (`cni: none`), but Flux needs a CNI to run — install Cilium once with
the exact values from [infrastructure/cilium/helmrelease.yaml](infrastructure/cilium/helmrelease.yaml),
the Flux HelmRelease adopts it on the first reconcile:

```bash
helm template cilium cilium/cilium --version 1.20.1 \
  --namespace kube-system -f cilium-bootstrap-values.yaml | kubectl apply -f -
```

### Bootstrap FluxCD

```bash
kubectl create namespace flux-system
flux bootstrap github \
  --token-auth \
  --owner=NiklasWevel \
  --repository=Kubernetes \
  --branch=main \
  --path=cluster \
  --personal
```

