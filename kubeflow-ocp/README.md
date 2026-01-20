##  Create project

~~~ bash

oc new-project pipe-server

~~~


## Copy values file and add custom values

~~~ bash
cp values.yaml myvalues.yaml
~~~

## Install


~~~ bash
helm install kfp .
~~~