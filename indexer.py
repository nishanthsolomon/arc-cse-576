import json
from time import sleep
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

client = Elasticsearch("localhost:9200")

def index_data(path, index_name):
    doc_list = []
    idx = 1

    with open(path) as f:
        for line in f:
            doc = json.loads(line)
            doc["timestamp"] = datetime.now()
            doc["_id"] = idx
            doc_list += [doc]
            idx+= 1
    
    response = helpers.bulk(client, doc_list, index=index_name, doc_type="_doc")

    print("helpers.bulk() RESPONSE: ", response)

index_data("./data/train.jsonl", "train_data")
index_data("./data/dev.jsonl", "dev_data")
index_data("./data/test.jsonl", "test_data")