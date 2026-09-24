# Talos Machine Configuration

Source of truth for the Talos Linux machine configs of this cluster (Talos 1.14, Kubernetes
pinned to 1.36.4).

## Layout

| Path | Purpose |
|---|---|
| `schematic-controlplane.yaml` | Image Factory schematic for the GPU-less control plane. ID: `88d1f7a5c4f1d3aba7df787c448c1d3d008ed29cfb34af53fa0df4336a56040b` |
| `schematic-worker.yaml` | Image Factory schematic for the GPU workers (NVIDIA lts + i915). ID: `9a8df76df029257d6d1385ae9a72d79bc995af269f3521b5723b883f3407174a` |
| `patches/patch-all.yaml` | kubelet mounts + image pin, registry mirror, kube-proxy off, typed-document fixes (Flannel/KubeProxy delete, KubeNetworkConfig subnets) |
| `patches/patch-controlplane.yaml` | static hostname, taint-free KubeNodeConfig, OIDC-discovery anonymous auth (Vault JWKS), CP installer image |
| `patches/patch-worker.yaml` | NVIDIA kernel modules, worker installer image |
| `cilium-bootstrap-values.yaml` | one-time Cilium install before Flux takes over |
| `secrets.sops.yaml` | cluster PKI bundle, sops/age-encrypted |

## Regenerating machine configs

The secrets bundle keeps the cluster identity stable — never run `gen config` without it:

```bash
sops --decrypt talos/secrets.sops.yaml > secrets.yaml

talosctl gen config homelab https://192.168.20.11:6443 \
  --with-secrets secrets.yaml \
  --kubernetes-version 1.36.4 \
  --config-patch @talos/patches/patch-all.yaml \
  --config-patch-control-plane @talos/patches/patch-controlplane.yaml \
  --config-patch-worker @talos/patches/patch-worker.yaml \
  --output configs/

shred -u secrets.yaml
```

Talos 1.14 quirk: document patches replace whole documents and `gen config` emits typed documents
before applying v1alpha1 patches — keep settings in exactly one world per concern (see the
migration doc for the four incidents behind this rule).

## Secrets handling

- Encrypted with [sops](https://github.com/getsops/sops) + age; the recipient is pinned in
  [.sops.yaml](../.sops.yaml).
- The age private key exists only in the password manager. Without it, `secrets.sops.yaml` is
  irrecoverable — by design.
- Edit in place with `sops talos/secrets.sops.yaml`.
