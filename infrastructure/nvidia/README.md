# NVIDIA GPU on Talos

The NVIDIA driver and the container toolkit are **not** managed by the gpu-operator on Talos.
Both are baked into the node image as system extensions (worker Image Factory schematic):

- `siderolabs/nonfree-kmod-nvidia-production`
- `siderolabs/nvidia-container-toolkit-production`

The kernel modules (`nvidia`, `nvidia_uvm`, `nvidia_drm`, `nvidia_modeset`) are loaded via the
worker machine config, which is maintained outside of this repository.

The gpu-operator therefore runs with `driver.enabled: false` and `toolkit.enabled: false` and only
manages the device plugin (with the time-slicing config from `configmap.yaml`), DCGM exporter and
node feature discovery. The `nvidia` RuntimeClass is provided by `runtimeclass.yaml` in this
directory; the matching containerd runtime comes from the toolkit extension on the host.

## Upgrading the driver

Driver upgrades happen through a new Image Factory schematic / Talos upgrade
(`talosctl upgrade --image factory.talos.dev/installer/<schematic>:<version>`), not through apt or
the operator.

## Test

You can deploy a test pod that uses the GPU:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nvidia-smi
spec:
  nodeSelector:
    nvidia.com/gpu.present: "true"
  runtimeClassName: nvidia
  restartPolicy: OnFailure
  containers:
    - name: nvidia-smi
      image: nvidia/cuda:12.1.0-base-ubuntu22.04
      command: ['sh', '-c', "nvidia-smi"]
      resources:
        limits:
            nvidia.com/gpu: "1"
```

The following section is crucial to ensure the pod requests GPU resources:

```yaml
spec:
  nodeSelector:
    nvidia.com/gpu.present: "true"
  runtimeClassName: nvidia
```

With time-slicing enabled (`configmap.yaml`, 4 replicas) each physical GPU shows up as
4 allocatable `nvidia.com/gpu` units.
