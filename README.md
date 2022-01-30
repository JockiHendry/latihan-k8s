This is an exercise project.  I put the code for services and Kubernetes manifest in this monorepo because GitHub doesn't support grouping
multiple repositories into one logical project (folder).  In real world where the code is maintained by different teams, it is sensible to 
convert each folder in this project as standalone repository.

## How to Run?

Make sure required tools like git and kpt v1.0.0.0-beta.12 or recent are installed.  Then, run the following command to initialize kpt in a folder:

```
$ mkdir deployment

$ cd deployment

$ git init

$ kpt pkg init

$ kpt live init

$ kpt pkg get https://github.com/JockiHendry/latihan-k8s.git/kubernetes@v0.0.3

$ git add .

$ git commit -m "First commit"
```

This is a platform repository that represents the app deployment.  It can be set to run a script that will run `kpt live apply` on 
every new commit, for example:

```shell
#!/usr/bin/env bash
kpt fn eval --image gcr.io/kpt-fn-contrib/sops:v0.3.0 --env SOPS_IMPORT_PGP="$(gpg --armor --export-secret-keys FFA6D9C42D878F5C)" \
--include-meta-resources --fn-config kubernetes/decrypt.yaml kubernetes
kpt fn render
kpt live apply
```

After the application has been deployed successfully, run any Day 0 imperative functions if required.  For example, 
if the server is for development, run the following script to expose node ports and add localhost CORS headers:

```
$ kpt fn eval --image gcr.io/kpt-fn/starlark:v0.3.0 --fn-config kubernetes/setup-dev.yaml

$ git add kubernetes/kong/kong.yaml kubernetes/kong/cors-plugin.yaml

$ git commit -m "Add dev setup"
```

There is also a function to refresh public key used by Kong Ingress Controller to verify JWT by getting it directly from Keycloak 
that should be run every time Keycloak realm's public key is updated.  It can be executed by running the following commands 
after Keycloak and Kong has been deployed:

```
$ kpt fn eval --image gcr.io/kpt-fn-contrib/sops:v0.3.0 --env SOPS_IMPORT_PGP="$PRIVATE_KEY" \
--include-meta-resources --fn-config kubernetes/decrypt.yaml kubernetes

$ kpt fn eval --image gcr.io/kpt-fn/starlark:v0.3.0 --network --fn-config kubernetes/kong/refresh-jwt-secret.yaml

$ kpt fn eval --image gcr.io/kpt-fn-contrib/sops:v0.3.0 --include-meta-resources --fn-config kubernetes/encrypt.yaml kubernetes

$ git add .

$ git commit -m "Update JWT public key"
```

## How to Update?

Assuming that Kubernetes is currently serving app `v0.0.3`, as developers add new features, the operation team might decide 
to release new features tagged as `v0.0.4`.  To update existing Kubernetes to serve app `v0.0.4`, run the following commands:

```
$ kpt pkg update kubernetes@v0.0.4

$ git add .

$ git commit -m "Update to v0.0.4"
```

When this commit is pushed to upstream and triggered the CI script as described in the previous version, updates to the 
Kubernetes resources will be deployed. If a resource has been declared in previous version but not declared anymore in 
current version, kpt will remove it. 

Assuming that new version turned out to be a regression, the operation team might decide to rollback the deployment.  To do 
that, just revert to previous commit (for example, by using `git reset --hard HEAD~1`).
