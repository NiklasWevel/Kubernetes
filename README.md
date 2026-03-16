# My Kubernetes GitOps Repository

This is my personal Kubernetes learning project.

> ⚠️ This repository is **rapidly changing** and also used for testing new ideas and configurations.

## Goals

- ~~ [ ] Migrate my entire Proxmox homelab into Kubernetes ~~
- [x] Rely entirely on GitOps and Infrastructure as Code using [FluxCD](https://fluxcd.io/)
- [x] Keep everything public - use [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) and [External Secrets](https://external-secrets.io/) to protect sensitive data
- [x] Implement a CI/CD pipeline to lint/prettier the configuration files
- [x] Implement [NVIDIA Container Toolkit ](https://nvidia.github.io/libnvidia-container/) to run GPU workloads in the cluster
- [ ] Make the cluster reachable from the internet while using [PocketID](https://pocketid.com/) to authenticate with passkeys


## Repository Structure

```text
.
├── apps/             # Application deployments 
├── cluster/          # FluxCD bootstrap and cluster-wide configuration
├── databases/        # Database deployments used by applications
├── docs/             # Documentation about architecture, decisions and setup
├── infrastructure/   # Core infrastructure components required for the cluster
├── platform/         # Shared platform services used by apps
├── monitoring/       # Monitoring and observability stack
├── repository/       # External or additional Git repositories referenced by Flux
└── README.md
```




## External Requirements

These components are required outside of the Kubernetes cluster:

1. An NFS server for persistent volumes  
2. A [HashiCorp Vault](https://www.vaultproject.io/) instance for secrets management  
3. [Caddy](https://caddyserver.com/) as a reverse proxy to reach the cluster in the first place
4. A public domain to enable SSL via DNS challenge (in my case Cloudflare + cert-manager)

These components are optional:

1. A [private Docker Hub Proxy Cache](https://hub.docker.com/_/registry) ,  so I don't run into the new Docker pull limit when I restart the cluster multiple times.
2. A [S3 compatible storage backend](https://github.com/deuxfleurs-org/garage) for the cloud native postgres backups jobs. I'm using Garage with a simple GUI. 

## Homelab Hardware

Currently, the cluster is running on three virtual machines in my three node Proxmox setup:

| Hostname     | Cores | RAM   | GPU       |
|--------------|-------|-------|-----------|
| K3-CP-01     | 2     | 16GB  |           |
| K3-Node-01   | 5     | 48GB  | RTX A2000 |
| K3-Node-02   | 5     | 48GB  | RTX A2000 |


## Networking

- The cluster runs in an isolated VLAN.
- The support components like NFS, reverse proxy, vault etc. run in the same VLAN.
- ~~All hostnames in this repository are used internally - the cluster is not accessible from the internet.~~
- The cluster will be accessible from the internet. Soon™.
- [Traefik](https://traefik.io/traefik/) acts as the reverse proxy and handles TLS termination for incoming traffic to the cluster.

## Storage

Storage is not part of this repository:

1. It depends heavily on the specific environment

2. I prefer not to publicly expose my file structure

## Cluster Initialization

### Install K3s (Control Plane)

```bash
curl -sfL https://get.k3s.io | sh -s - \
  --flannel-backend=none \
  --disable-kube-proxy \
  --disable servicelb \
  --disable-network-policy \
  --disable traefik \
  --cluster-init
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

