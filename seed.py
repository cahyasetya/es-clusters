from elasticsearch import Elasticsearch
import csv

client = Elasticsearch("http://localhost:9200")

index_name = "peoples"

if not client.indices.exists(index=index_name):
    client.indices.create(
        index=index_name,
        body={"settings": {"number_of_shards": 3, "number_of_replicas": 2}},
    )
    print(f"Index '{index_name}' created with 1 shard and 3 replicas.")
else:
    print(f"Index '{index_name}' already exists.")

with open("people-2000000.csv", mode="r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Skip the header row

    for row in reader:
        client.index(
            index="peoples",
            id=row[1],
            document={"first_name": row[2], "last_name": row[3], "email": row[5]},
        )
        print(f"{row[1]} inserted")

client.close()
