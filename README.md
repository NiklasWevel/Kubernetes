# My Kubernetes GitOps Repository

This is my learning Kubernetes repository.

> ⚠️ This repo is **rapidly changing** and used for testing as I go.

## Goals

- [ ] Implement my complete Proxmox homelab into Kubernetes
- [ ] Rely entirely on GitOps and Infrastructure as Code using
- [ ] Keep everything public – so encrypt secrets using 
- [ ] Implement a full CI/CD pipeline

## Repository Structure

```text
.
├── apps/             # Applications (e.g. Homepage, Paperless)
├── infrastructure/   # Infrastructure components (e.g. Traefik, cert-manager)
├── cluster/          # Cluster-scoped settings (e.g. Flux system, storage)
└── README.md
```

## Stack Highlights

- Kubernetes with kubeadm
- FluxCD for GitOps management
- Helm for package management
- Kustomize for customizing Kubernetes resources
- Traefik as Ingress Controller
- MetalLB for LoadBalancer support in bare metal
- cert-manager for automated TLS
- Sealed Secrets for encrypted Secret management

## Notes

This repo is intended to be:
- Fully declarative
- Automatically applied to the cluster via FluxCD
- Public and secure using Sealed Secrets

PRs, issues or suggestions are welcome, but keep in mind this is a personal learning project.

