# Launch a Simple Flask App on DOKs
This codebase contains all of the necessary files required to launch a simple Flask application on Digital Ocean Kubernetes (DOKs). 

### Required Packages
* [Doctl](https://docs.digitalocean.com/reference/doctl/how-to/install/)
* [Docker Desktop](https://www.docker.com/get-started/)

### Prequisites
* DigitalOcean Container Registry (DOCR) is already [created](https://www.digitalocean.com/community/developer-center/how-to-set-up-digitalocean-container-registry).
* DigitalOcean Kubernetes (DOKs) cluster is already [provisioned](https://docs.digitalocean.com/products/kubernetes/getting-started/quickstart/).
* DOCR + DOks are already [integrated](https://docs.digitalocean.com/products/kubernetes/how-to/integrate-with-docr/).

### Assumptions
Any environment variable configurations will be handled via [python-dotenv](https://pypi.org/project/python-dotenv/) or [kubectl secrets](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kubectl/).

## Getting Started
Create a new directory in a location of your choice on your local machine and clone this repository into it. 
```
git clone https://github.com/codyfishman/doks-resources/
```
## Dockerize Application
Build the image locally with Docker. 
```
docker build -t my-python-app .
```
Confirm the image is available in your local Docker registry. 
```
docker images
```
Run the image locally with Docker.
```
docker run -ti -p 80:80 my-python-app
```
## Push Docker Image to DOCR
Run doctl’s login command for registries. 
```
docker registry login
```
Tag your image locally with the DigitalOcean registry name. 
```
docker tag my-python-app registry.digitalocean.com/<your-registry-name>/my-python-app
```
Push your image from the local Docker registry to the DigitalOcean registry.
```
docker push registry.digitalocean.com/<your-registry-name>/my-python-app
```
## Deploy Application to DOKs Cluster
Deploy your application to your DOKs cluster by submitting a deployment object.
```
kubectl create deployment my-python-app --image=registry.digitalocean.com/<your-registry-name>/my-python-app
```
Check the replica set configuration. 
```
kubectl get rs
```
Check the state of your pods (containers running your application).
```
kubectl get pods
```
## Create a Load Balancer Service
Expose your application to the internet via a load balancer.
```
kubectl expose deployment my-python-app --type=LoadBalancer --port=80 --target-port=80
```
Confirm that the load balancer is activated. 
```
doctl compute load-balancer list --format Name,Created,IP,Status
```
## Troubleshooting
Confirm that the image exists on DOCR. 
```
doctl registry repository list-tags <your-registry-name>/my-python-app
```
Check for warnings and error messages in the event log for a particular pod. 
* You can get the pod name by running `kubectl get pods` and copying the name value listed for a degraded pod.
```
kubectl describe pod <pod_name>
```
Restart a deployment after fixes have been implemented. 
```
kubectl rollout restart deployment my-python-app
```
