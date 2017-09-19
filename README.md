## Synopsis
This is an adapter to the Kubernetes Python client API classes, creating uniform methods for reading and modifying resources in a Kubernetes cluster

## Example
A docker image showing how to use the Adpater API class.
### Build
```bash
docker build -t k8s-adapter .
```

### Run
The example below uses the __.kube/config__ file in your home directory
```bash
docker run --rm -v $HOME/.kube:/.kube -v $PWD:/data k8s-adapter -k /.kube/config -x kargo -f /data/example.yml -n default -c deploy
```