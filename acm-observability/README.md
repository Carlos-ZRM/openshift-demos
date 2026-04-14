##  Create project

~~~ bash

oc new-project quay-poc

~~~


## Copy values file and add custom values

~~~ bash
cp values.yaml myvalues.yaml
~~~


## Modify cluster domain 

~~~ bash
sed -i '' "s|domain:.*|domain: $(oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath='{.status.domain}')|" myvalues.yaml
~~~

## Obtain secret 

~~~ bash

sed -i '' "s|docker_config_secret:.*|docker_config_secret: '$(oc extract secret/pull-secret -n openshift-config --to=-)'|" myvalues.yaml


~~~
## Install


~~~ bash
helm install bucket -f myvalues.yaml .
~~~