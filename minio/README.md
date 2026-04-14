##  Create project

~~~ bash

oc new-project minio

~~~


## Copy values file and add custom values

~~~ bash
cp values.yaml myvalues.yaml
~~~

## Modify cluster domain 

~~~ bash
sed -i '' "s|domain:.*|domain: $(oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath='{.status.domain}')|" myvalues.yaml
~~~

## Install


~~~ bash
helm install bucket .
~~~