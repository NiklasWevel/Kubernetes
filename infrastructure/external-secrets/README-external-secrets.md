## External Secrets Operator – FluxCD Installation Structure

The installation of the External Secrets Operator is intentionally split into two parts:

1. `external-secrets/` – contains the Helm chart installation (`helmrelease.yaml`)  
2. `external-secrets/crs/` – contains the Custom Resources like `ClusterSecretStore`

### Why is this split necessary?

FluxCD performs a full validation (`dry-run`) of all resources before applying them.  
If everything is in one directory, Flux tries to validate the `ClusterSecretStore` resource before the Helm chart has installed its required CustomResourceDefinition (CRD).

This results in the following error:

```
no matches for kind "ClusterSecretStore" in version "external-secrets.io/v1beta1"
```

### Solution

To avoid this issue, the Helm chart (which installs the CRDs) is applied first via:

```yaml
infrastructure/external-secrets/
```

And only after that, the custom resources like `cluster-secret-store.yaml` are applied from:

```yaml
infrastructure/external-secrets/crs/
```

### Source

[Link to external secrets documentation](https://external-secrets.io/v0.17.0/examples/gitops-using-fluxcd/)
