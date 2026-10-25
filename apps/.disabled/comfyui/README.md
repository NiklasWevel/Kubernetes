When deploying **ComfyUI** in a Kubernetes cluster, you may encounter crashes if memory `requests` are set lower than `limits`, even when the node has sufficient available resources.



```yaml
          resources:
            requests:
              cpu: "200m"
              memory: "16Gi"
            limits:
              cpu: "500m"
              memory: "16Gi"
              nvidia.com/gpu: "1"
```	  
			  
			  