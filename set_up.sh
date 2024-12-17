#!/bin/bash  
prefix="demofinetunning-ncus"
location="northcentralus"
subscription_id=$(az account show --query id --output tsv)
user_id=$(az ad signed-in-user show --query id --output tsv)

ai_resource_name="$prefix"
echo "Resource name: $ai_resource_name"  

# Get aun auth token
auth_token=$(az account get-access-token --resource https://management.azure.com/ --query accessToken --output tsv)

# Create the resource group
ai_resource_name_resource_group_name=$ai_resource_name"-rg"
echo "Creating resource group: $ai_resource_name_resource_group_name"
az group create --name $ai_resource_name_resource_group_name --location $location > null

# Create the Hub
ai_resource_name_hub_name=$ai_resource_name"-hub"
echo "Creating AI Studio Hub: $ai_resource_name_hub_name"
az ml workspace create --kind hub --resource-group $ai_resource_name_resource_group_name --name $ai_resource_name_hub_name > null

# Create project in Hub
hub_id=$(az ml workspace show  -g $ai_resource_name_resource_group_name --name $ai_resource_name_hub_name --query id --output tsv)
# Remove leading slash from hub_id if it exists
hub_id=$(echo $hub_id | sed 's|^/||')
ai_resource_project_name=$ai_resource_name"-project"
echo "Creating AI Studio Project: $ai_resource_project_name"
az ml workspace create --kind project --resource-group $ai_resource_name_resource_group_name --name $ai_resource_project_name --hub-id $hub_id > null

# Create a Azure AI Service Account
ai_resource_ai_service=$ai_resource_name"-aiservice"
echo "Creating AI Service Account: $ai_resource_ai_service"
az cognitiveservices account purge -l $location -n $ai_resource_ai_service -g $ai_resource_name_resource_group_name
az cognitiveservices account create --kind AIServices --location $location --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --sku S0 --yes > null

# Deploying GPT-4o in Azure AI Service
echo "Deploying GPT-4o"
az cognitiveservices account deployment create --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --deployment-name "gpt-4o" --model-name "gpt-4o" --model-version "2024-08-06" --model-format "OpenAI" --sku-capacity "1" --sku-name "Standard" --capacity "100"


# Adding connection to the AI Hub
echo "Adding AI Service Connection to the HUB"
ai_service_resource_id=$(az cognitiveservices account show --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --query id --output tsv)
ai_service_api_key=$(az cognitiveservices account keys list --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --query key1 --output tsv)

rm connection.yml   
echo "name: $ai_resource_ai_service" >> connection.yml  
echo "type: azure_ai_services" >> connection.yml  
echo "endpoint: https://$location.api.cognitive.microsoft.com/" >> connection.yml  
echo "api_key: $ai_service_api_key" >> connection.yml  
echo "ai_services_resource_id:  $ai_service_resource_id" >> connection.yml  

az ml connection create --file connection.yml --resource-group $ai_resource_name_resource_group_name --workspace-name  $ai_resource_name_hub_name > null
rm connection.yml 
az role assignment create --role "Storage Blob Data Contributor" --scope subscriptions/$subscription_id/resourceGroups/$ai_resource_name_resource_group_name --assignee-principal-type User --assignee-object-id $user_id

# Save the database credentials and connection string to the .env file
# create an .env file with hard-coded values for local demos and testing.  
echo "An .env file with hard-coded values for local demos and testing has been created in the src directory"
echo "Please do not share this file, or commit this file to the repository"
echo "This file is used to store the environment variables for the project for demos and testing only"
echo "Delete this file when done with demos, or if you are not using it"

echo "# Please do not share this file, or commit this file to the repository" > .env
echo "# This file is used to store the environment variables for the project for demos and testing only" >> .env
echo "# delete this file when done with demos, or if you are not using it" >> .env
echo "AOAI_ENDPOINT=https://$location.api.cognitive.microsoft.com/" >> .env
echo "AOAI_API_KEY=$ai_service_api_key" >> .env
echo 'AOAI_API_VERSION="2024-05-01-preview"' >> .env
echo 'AOAI_MODEL_NAME="gpt-4o"' >> .env
echo "AZ_RESOURCE_GROUP_NAME=$ai_resource_name_resource_group_name" >> .env
echo "AZ_SUBSCRIPTION_ID=$subscription_id" >> .env
echo "AZ_AI_SERVICE_NAME=$ai_resource_ai_service" >> .env
echo "TEMP_AUTH_TOKEN=$auth_token" >> .env