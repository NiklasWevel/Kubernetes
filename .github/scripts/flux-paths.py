import pathlib
import yaml

paths = set()
for file in pathlib.Path(".").rglob("*.yaml"):
    if ".git" in file.parts:
        continue
    try:
        docs = list(yaml.safe_load_all(file.read_text()))
    except yaml.YAMLError:
        continue
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        if not str(doc.get("apiVersion", "")).startswith("kustomize.toolkit.fluxcd.io/"):
            continue
        spec = doc.get("spec", {})
        if spec.get("sourceRef", {}).get("name") == "flux-system":
            paths.add(spec["path"])

print("\n".join(sorted(paths)))
