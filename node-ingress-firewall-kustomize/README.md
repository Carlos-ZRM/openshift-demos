## create directory and kustomization files

~~~ bash
mkdir -p  base overlays/{dev,prod}
touch  base/kustomization.yaml overlays/{dev,prod}/kustomization.yaml

~~~


## Fill kustomization files

~~~ bash
find . -name "kustomization.yaml" -type f -exec sh -c 'cat <<EOF > "{}"
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
EOF' \;

~~~
