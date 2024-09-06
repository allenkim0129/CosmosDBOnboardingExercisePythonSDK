# CosmosDBOnboardingExercisePythonSDK
This repo is to learn how to use Cosmos DB Python SDK


# How to get ACCOUNT_URI and ACCOUNT_KEY

```
bash get_account_uri_and_key.sh 
```

# Onboarding Tasks for Python SDK

## 1. Players - gives an understanding of how the SDK works, running users through the most common methods and having them use options to alter behavior.
 
I want you to write a file that does the following:
 
Create two clients = one client with Session consistency and one with Eventual consistency, both with a request timeout of 120
 
Use either of those clients to create two databases with the following settings:
- ID = "Cowboys", throughput = 5000 RUs
- ID = "Pirates"
 
Print out the list of databases
 
In the Cowboys database, create 10 containers with ID = Simon{1-10} and PartitionKey with path = '/id'
 
Print out the list of containers in that database
 
In the Pirates database, create 2 containers:
- ID = "Top Players", PartitionKey = id, default_ttl = 1000
- ID = "All Players", PartitionKey = id, throughput = 3000
 
Print out the list of containers in this database
 
In the "All Players" container, create 10 players. Players are items, and have the following values:
- id: string
- total_wins: int
- total_losses: int
 
Where id can be anything (can use uuid or enable_automatic_id_generation), total_wins is a random int from 10-50, and total_losses is a random int from 10-20
 
Once those are created, read every player you just created from the container
 
Now for each of the players you created, you will run a code that checks if total_wins - total_losses > 5, and if it's true for any player you will create that player in the "Top Players" container as well
 
"Top Players" players only have two values:
- id: string
- game_difference: int -> This is the value you calculate before (total_wins - total_losses)
 
You will then run a cross partition query in the "Top Players" container to find all players whose game_difference > 10, and print those players
 
Once all of this has been done, you will:
- delete all containers in each database
- delete all databases in each client
 
and finish by printing "Completed"
 
For bonus points, do the same thing in the async client - the translation of one to the other should be pretty straightforward
