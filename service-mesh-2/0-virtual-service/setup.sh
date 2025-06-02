#!/bin/bash

# Script to create a project, label it for Istio, and check mesh membership

# Check if a project name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 --name <project-name>"
  exit 1
fi

PROJECT_NAME=""

# Parse the --name flag
if [ "$1" == "--name" ]; then
  if [ -z "$2" ]; then
    echo "Error: Project name not provided after --name flag."
    echo "Usage: $0 --name <project-name>"
    exit 1
  fi
  PROJECT_NAME=$2
else
  echo "Usage: $0 --name <project-name>"
  exit 1
fi

echo "Creating project '$PROJECT_NAME'..."
oc new-project "$PROJECT_NAME"

if [ $? -ne 0 ]; then
  echo "Error: Failed to create project '$PROJECT_NAME'."
  exit 1
fi

echo "Labeling namespace '$PROJECT_NAME' with istio-injection=enabled..."
oc label namespace "$PROJECT_NAME" istio-injection=enabled --overwrite

if [ $? -ne 0 ]; then
  echo "Error: Failed to label namespace '$PROJECT_NAME'."
  # Optional: attempt to delete the project if labeling fails
  # oc delete project "$PROJECT_NAME"
  exit 1
fi

echo "Waiting for 5 seconds..."
sleep 5

echo "Checking if namespace '$PROJECT_NAME' is part of the Istio service mesh..."
# This command checks if the namespace is listed in the ServiceMeshMemberRoll
# Adjust the 'istio-system' namespace if your Service Mesh control plane is installed elsewhere.
# Adjust the member roll name 'default' if you use a different one.
if oc get smmr default -n istio-system -o yaml | grep -q "$PROJECT_NAME"; then
  echo "Namespace '$PROJECT_NAME' is part of the Istio service mesh."
  oc describe smm -n $PROJECT_NAME
else
  echo "Namespace '$PROJECT_NA// ...existing code...
echo "Waiting for 5 seconds..."

sleep 1

oc policy add-role-to-user system:image-puller system:serviceaccount:0-vs:default --namespace=xpk
