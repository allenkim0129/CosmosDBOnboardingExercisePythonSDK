#! /bin/bash

RES_GROUP=allekim-onboarding-test
ACCT_NAME=allekim-test-account

export ACCOUNT_URI=$(az cosmosdb show --resource-group $RES_GROUP --name $ACCT_NAME --query documentEndpoint --output tsv)
export ACCOUNT_KEY=$(az cosmosdb list-keys --resource-group $RES_GROUP --name $ACCT_NAME --query primaryMasterKey --output tsv)

Echo ''
Echo ACCOUNT_URI: $ACCOUNT_URI
Echo ACCOUNT_KEY: $ACCOUNT_KEY