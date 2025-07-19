## 1. Add the NVIDIA repo

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

---

## 2. Update packages and install NVIDIA components

```bash
sudo apt update
sudo apt install -y nvidia-driver-550-server nvidia-container-toolkit nvidia-container-runtime
```

---

## 3. Remove K3s Containerd config files (K3s will regenerate them when restarting)

```bash
sudo rm /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl
sudo rm /var/lib/rancher/k3s/agent/etc/containerd/config.toml
```

---

## 4. Restart the K3s agent

```bash
sudo systemctl restart k3s-agent
```

> After the restart, K3s will regenerate the `config.toml` and detect the NVIDIA runtime if correctly installed.

---

## 5.Test

You can now deploy a test pod that uses the GPU.

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