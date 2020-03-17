from elasticsearch import Elasticsearch, helpers


client = Elasticsearch("localhost:9200")


def gendata(path):
    with open(path) as f:
        for line in f:
            yield {
                "doc": {"data": line},
            }


def index_data(path, index_name):

    response = helpers.bulk(client, gendata(
        path), index=index_name, doc_type="_doc")

    print("helpers.bulk() RESPONSE: ", response)


index_data("./dataset/ARC-V1-Feb2018/ARC_Corpus.txt", "arc_corpus")
