# Setup

Run `keycloak/setup-job.yaml` to create Keycloak realms, clients, default user and password that is needed for a quick demo.

When running in minikube for development, execute the following command to expose Kong Ingress Controller and http://localhost:4200 as allowed origin for CORS:

```
$ kpt fn eval --image gcr.io/kpt-fn/starlark:v0.3.0 --fn-config setup-dev.yaml
```

To refresh public key used by Kong by automatically retrieving from Keycloak, run the following function:

```
$ kpt fn eval --image gcr.io/kpt-fn/starlark:v0.3.0 --network --fn-config kong/refresh-jwt-secret.yaml
```