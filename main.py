from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.cosmos.aio import CosmosClient as CCA

import os
import random
import asyncio

URL = os.environ['ACCOUNT_URI']
KEY = os.environ['ACCOUNT_KEY']
REQUEST_TIMEOUT = 120000 # 120 seconds
THROUGHPUT = 5000 # 5000 RUs

PARTITION_KEY = PartitionKey(path='/id')

def create_client(consistency_level):
    client = CosmosClient(URL, credential=KEY, consistency_level=consistency_level, request_timeout=REQUEST_TIMEOUT)
    return client

def create_client_async(consistency_level):
    client = CCA(URL, credential=KEY, consistency_level=consistency_level, request_timeout=REQUEST_TIMEOUT)
    return client

def create_database(client, database_name):
    database = client.create_database_if_not_exists(database_name, offer_throughput=THROUGHPUT)
    return database


def run_exercise():
    # Create two clients = one client with Session consistency and one with Eventual consistency, both with a request timeout of 120
    client = create_client("Session")
    # client = create_client("Eventual")

    # Use either of those clients to create two databases with the following settings:
    # - ID = "Cowboys", throughput = 5000 RUs
    # - ID = "Pirates"
    cowboys_db = create_database(client, "Cowboys")
    pirates_db = create_database(client, "Pirates")

    # Print out the list of databases
    print("\nList of Databases:")
    for db in client.list_databases():
        print("Databases ID: {}".format(db['id']))

    # In the Cowboys database, create 10 containers with ID = Simon{1-10} and PartitionKey with path = '/id'
    for i in range(1, 11):
        cowboys_db.create_container_if_not_exists(id=f'Simon{i}', partition_key=PartitionKey(path='/id'))

    # Print out the list of containers in that database
    print("\nList of containers in Cowboys DB:")
    for container in cowboys_db.list_containers():
        print("Container ID: {}".format(container['id']))

    # In the Pirates database, create 2 containers:
    # - ID = "Top Players", PartitionKey = id, default_ttl = 1000
    # - ID = "All Players", PartitionKey = id, throughput = 3000
    top_players_container = pirates_db.create_container_if_not_exists(
        id='Top_Players',
        partition_key=PARTITION_KEY,
        default_ttl=1000)
    all_players_container = pirates_db.create_container_if_not_exists(
        id='All_Players',
        partition_key=PARTITION_KEY,
        offer_throughput=3000)

    # Print out the list of containers in this database
    print("\nList of containers in Pirates DB:")
    for container in pirates_db.list_containers():
        print("Container ID: {}".format(container['id']))

    # In the "All Players" container, create 10 players. Players are items, and have the following values:
    # - id: string
    # - total_wins: int
    # - total_losses: int
    # Where id can be anything (can use uuid or enable_automatic_id_generation),
    # total_wins is a random int from 10-50, and total_losses is a random int from 10-20
    for i in range(1, 11):
        all_players_container.upsert_item({
            'id': f'Player{i}',
            'total_wins': random.randint(10, 50),
            'total_losses': random.randint(10, 20),
        })

    # Now for each of the players you created,
    # you will run a code that checks if total_wins - total_losses > 5,
    # and if it's true for any player you will create that player in the "Top Players" container as well

    # "Top Players" players only have two values:
    # - id: string
    # - game_difference: int -> This is the value you calculate before (total_wins - total_losses)

    for item in all_players_container.query_items(
            query="SELECT * FROM All_Players",
            enable_cross_partition_query=True):
        game_diff = item['total_wins'] - item['total_losses']

        if game_diff > 5:
            top_players_container.upsert_item({
                'id': item['id'],
                'game_difference': game_diff,
            })

    # You will then run a cross partition query in the "Top Players" container
    # to find all players whose game_difference > 10, and print those players
    print('\nTop Players with game_difference greater than 10')
    for item in top_players_container.query_items(
            query="SELECT * FROM Top_Players",
            enable_cross_partition_query=True):
        if item['game_difference'] > 10:
            print(f'Top Player ID: {item["id"]}, Game Difference: {item["game_difference"]}')

    # Once all of this has been done, you will:
    # - delete all containers in each database
    # - delete all databases in each client
    print("\nDeleting all Containers")
    print("- Cowboys DB")
    for container in cowboys_db.list_containers():
        print("Container ID: {}".format(container['id']))
        cowboys_db.delete_container(container['id'])

    print("- Pirates DB")
    for container in pirates_db.list_containers():
        print("Container ID: {}".format(container['id']))
        pirates_db.delete_container(container['id'])

    print("\nDeleting all database in each client")
    print("- Client")
    for db in client.list_databases():
        print("Database ID: {}".format(db['id']))
        client.delete_database(db['id'])
    #
    # print("- Client2")
    # for db in client2.list_databases():
    #     print("Database ID: {}".format(db['id']))
    #     client2.delete_database(db['id'])

    print("Completed!")

async def delete_all_containers(db):
    async for container in db.list_containers():
        print("Container ID: {}".format(container['id']))
        await db.delete_container(container['id'])

async def delete_all_databases(client):
    async for db in client.list_databases():
        print("Database ID: {}".format(db['id']))
        await client.delete_database(db['id'])

async def run_exercises_async(consistency_level):
    async with (create_client_async(consistency_level) as client):
        cowboys_db = await client.create_database_if_not_exists("Cowboys_Async", offer_throughput=THROUGHPUT)
        pirates_db = await client.create_database_if_not_exists("Pirates_Async", offer_throughput=THROUGHPUT)

        print("\nList of Databases:")
        async for db in client.list_databases():
            print("Databases ID: {}".format(db['id']))

        print("\nCreate Containers:")
        for i in range(10):
            await cowboys_db.create_container_if_not_exists(id=f'Simon{i + 1}', partition_key=PARTITION_KEY)

        top_players_container = await pirates_db.create_container_if_not_exists(
            id='Top_Players',
            partition_key=PARTITION_KEY,
            default_ttl=1000)
        all_players_container = await pirates_db.create_container_if_not_exists(
            id='All_Players',
            partition_key=PARTITION_KEY,
            offer_throughput=3000)

        # Print out the list of containers in this database
        print("\nList of containers in Pirates DB:")
        async for container in pirates_db.list_containers():
            print("Container ID: {}".format(container['id']))

        print("\nInserting items to All_Player container")
        for i in range(1, 11):
            await all_players_container.upsert_item({
                'id': f'Player{i}',
                'total_wins': random.randint(10, 50),
                'total_losses': random.randint(10, 20),
            })

        async for item in all_players_container.query_items(
                query="SELECT * FROM All_Players"):
            game_diff = item['total_wins'] - item['total_losses']

            if game_diff > 5:
                await top_players_container.upsert_item({
                    'id': item['id'],
                    'game_difference': game_diff,
                })

        print('\nTop Players with game_difference greater than 10')
        async for item in top_players_container.query_items(
                query="SELECT * FROM Top_Players"):
            if item['game_difference'] > 10:
                print(f'Top Player ID: {item["id"]}, Game Difference: {item["game_difference"]}')

        print("\nDeleting all containers in each database")
        await delete_all_containers(cowboys_db)
        await delete_all_containers(pirates_db)

        print("\nDeleting all database in each client")
        await delete_all_databases(client)

    print("Completed!")


if __name__ == '__main__':
    # run_exercise()
    # asyncio.run(run_exercises_async("Session"))
    asyncio.run(run_exercises_async("Eventual"))









