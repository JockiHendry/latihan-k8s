# kubernetes

## Description
sample description

## Usage

### Fetch the package
`kpt pkg get REPO_URI[.git]/PKG_PATH[@VERSION] kubernetes`
Details: https://kpt.dev/reference/cli/pkg/get/

### View package content
`kpt pkg tree kubernetes`
Details: https://kpt.dev/reference/cli/pkg/tree/

### Apply the package
```
kpt live init kubernetes
kpt live apply kubernetes --reconcile-timeout=2m --output=table
```
Details: https://kpt.dev/reference/cli/live/
