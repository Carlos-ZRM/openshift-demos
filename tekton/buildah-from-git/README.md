##  Create project

~~~ bash
 oc new-project python-app
~~~

## Copy values file and add custom values

~~~ bash
cp values.yaml myvalues.yaml
~~~

## Install Chart into specific namespace

~~~ bash
helm install buildah-from-git --values myvalues.yaml .
~~~

~~~ bash
helm install buildah-from-git -n  python-app --values myvalues.yaml .
~~~


~~~ bash
helm upgrade buildah-from-git --values myvalues.yaml .
~~~


## Execute with tekton cli

~~~ bash
tkn pipeline list
~~~

~~~ bash
kubectl get pvc,secret -l app.kubernetes.io/instance=buildah-from-git
~~~

### Example

~~~ bash
c9screyesma@creyesma-mac buildah-from-git % tkn pipeline list                                                    

NAME                              AGE              LAST RUN   STARTED   DURATION   STATUS
buildah-from-git-pipeline-clone   20 minutes ago   ---        ---       ---        ---
c9screyesma@creyesma-mac buildah-from-git % kubectl get pvc -l app.kubernetes.io/instance=buildah-from-git 

NAME                   STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
buildah-from-git-pvc   Pending                                      managed-csi    20m
c9screyesma@creyesma-mac buildah-from-git % 

~~~

### Example without auth

~~~ bash

tkn pipeline start buildah-from-git-pipeline-clone --workspace name=buildah-from-git,claimName=buildah-from-git-pvc

~~~

### Example

~~~ bash
c9screyesma@creyesma-mac buildah-from-git % tkn pipeline start buildah-from-git-pipeline-clone --workspace name=buildah-from-git,claimName=buildah-from-git-pvc
? Value for param `git-host` of type `string`? (Default is `https://gitlab.com/xpk/python-app-code.git`) https://gitlab.com/xpk/python-app-code.git
? Value for param `git-revision` of type `string`? (Default is `dev`) dev
? Value for param `git-verbose` of type `string`? (Default is `true`) true
? Value for param `git-ssl-verify` of type `string`? (Default is `true`) true
PipelineRun started: buildah-from-git-pipeline-clone-run-zdxcz

In order to track the PipelineRun progress run:
tkn pipelinerun logs buildah-from-git-pipeline-clone-run-zdxcz -f -n python-app
~~~