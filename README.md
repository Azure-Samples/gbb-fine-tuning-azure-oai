# <img src="./utils/images/azure_logo.png" alt="Azure Logo" style="width:30px;height:30px;"/>  Fine-Tuning of GPT4o for Function Calling

This repository provides a step-by-step guide on how to implement Fine Tuning of GPT-4o using Azure OpenAI. The fine tuning is done for reducing token consumption 
while maintaining accuracy.

  - [**Fine Tunning**](notebooks/1_finetuning.ipynb): This notebook guides you through the fine tuning process.
  - [**Evaluation**](notebooks/2_evaluation.ipynb): This notebook guides you through evaluating an application that uses either the base model or the fine tuned model. We will use Azure Machine Learning for performing the runs. 
  - [**Application flow**](src/flow/): This is the flow of a simple application, using Prompt Flow.
  - [**Evaluation flow**](src/evaluation/): This is is an evaluation flow of the application above. The flow uses Prompt Flow as well. 

## 🔧 1. Infrastructure Creation
You can use the shell script `set_up.sh` to set up the infrastructure on Azure. To run the script, you need to have the Azure CLI installed and be logged in. You can install the Azure CLI by following the instructions [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

Its necessary to install an extension: az extension add -n ml

```bash
 ./set_up.sh
 ```

The `.env` file will be populated automatically by the script.

- **Install dependencies**
```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## 🔧 2. Running the Evaluation Flow in AI Studio
- Upload the flows to Azure AI Studio Promptflow
- Create the connections to your Azure Open AI Resources
- Execute the evaluation with the provided [datasets](./data/) 

