#!/bin/bash

# Azure deployment script for FastAPI + FAISS app

# Define variables
RESOURCE_GROUP="faiss-app-rg"
APP_NAME="faiss-document-retrieval"
DOCKER_IMAGE="faiss-app-image"
REGISTRY_NAME="faisscontainerregistry"
LOCATION="eastus"

# Login to Azure
az login

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry (ACR)
az acr create --resource-group $RESOURCE_GROUP --name $REGISTRY_NAME --sku Basic

# Authenticate ACR
az acr login --name $REGISTRY_NAME

# Build and push Docker image to ACR
docker build -t $REGISTRY_NAME.azurecr.io/$DOCKER_IMAGE:latest .
docker push $REGISTRY_NAME.azurecr.io/$DOCKER_IMAGE:latest

# Create Azure App Service Plan
az appservice plan create --name $APP_NAME-plan --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Deploy containerized app to Azure Web App
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_NAME-plan --name $APP_NAME \
    --deployment-container-image-name $REGISTRY_NAME.azurecr.io/$DOCKER_IMAGE:latest

# Configure App Service to pull images from ACR
az webapp config container set --name $APP_NAME --resource-group $RESOURCE_GROUP \
    --docker-custom-image-name $REGISTRY_NAME.azurecr.io/$DOCKER_IMAGE:latest \
    --docker-registry-server-url https://$REGISTRY_NAME.azurecr.io

# Restart the web app to apply changes
az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP

echo "Deployment completed! Access your app at: https://$APP_NAME.azurewebsites.net"
