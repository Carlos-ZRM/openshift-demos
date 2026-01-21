## Set domain into myvalues file

~~~ bash
sed -i '' "s|domain:.*|domain: $(oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath='{.status.domain}')|" myvalues.yaml
~~~
##  Create project

~~~ bash

oc new-project quay-poc

~~~


## Copy values file and add custom values

~~~ bash
cp values.yaml myvalues.yaml
~~~

## Install


~~~ bash
helm install loki i -f myvalues.yaml .
~~~

~~~ bash
helm upgrade loki -f myvalues.yaml .
~~~