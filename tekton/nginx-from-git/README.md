## Copy values file and add custom values

~~~ bash
cp values.yaml myvalues.yaml
~~~

## Example

~~~ bash

git:
  hostname: https://gitlab.com/xpk/webstatic-app-code.git
  authType: basic
  revision: main
  verbose: true
  sslVerify: true

~~~

## Install Chart into specific namespace

~~~ bash
helm install appweb --values myvalues.yaml .
~~~
