from azure.cosmos import CosmosClient

import os

def create_client():
    URL = os.environ['ACCOUNT_URI']
    KEY = os.environ['ACCOUNT_KEY']
    client = CosmosClient(URL, credential=KEY)
    return client

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_client()
