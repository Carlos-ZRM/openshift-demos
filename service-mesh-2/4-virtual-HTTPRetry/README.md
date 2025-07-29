# 0-virtual-service

This directory contains resources related to the configuration of Istio VirtualServices and related elements for the Service Mesh demonstration.

## Elements Created

- **VirtualService**: Defines how requests are routed to services within the mesh. It allows you to control traffic routing, such as splitting traffic between different versions of a service, rewriting URLs, or applying header-based routing.
- **DestinationRule**: Specifies policies that apply to traffic after routing has occurred, such as load balancing, connection pool settings, and outlier detection for a specific service.
- **Gateway** (if present): Configures how traffic enters the mesh from outside, typically exposing HTTP, HTTPS, or other protocols.
- **Service**: Standard Kubernetes Service definitions that expose your application’s pods within the cluster.
- **Deployment**: Standard Kubernetes Deployment resources that manage the lifecycle and scaling of your application pods.

## Usage

1. Apply the manifests in this directory to your OpenShift or Kubernetes cluster:
   ```sh
   oc apply -f .
   ```
2. Ensure that the Service Mesh control plane is installed and configured in your cluster.
3. Verify that the VirtualService and related resources are created:
   ```sh
   oc get virtualservice
   oc get destinationrule
   oc get gw
   ```

## Purpose

These resources demonstrate how to use Istio’s VirtualService and related objects to control and observe traffic flow within a service mesh environment. They are intended for learning, testing, and demonstration purposes.
