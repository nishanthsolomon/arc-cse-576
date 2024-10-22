import requests
import json
import configparser
from elasticsearch import Elasticsearch, helpers
from utils.utils import Utilities


class ElasticsearchUtils():
    HEADER = {
        'Content-Type': 'application/json',
    }

    PARAMS = (
        ('pretty', ''),
    )

    DATA_FORMAT = '{{"size": {}, "query": {{ "bool": {{ "must": {{ "match": {{ "data": "{}" }} }}, "should": {{ "match": {{ "data.shingles": "{}" }} }} }} }} }}'

    def __init__(self, config):
        request_url = config['request_url']
        self.index_name = config['index_name']
        self.client = Elasticsearch(request_url)
        self.search_url = '/'.join([request_url, self.index_name, '_search'])
        self.doc_path_index = config['doc_path_index']
        self.num_candidates = config['num_candidates']

    def gendata(self):
        with open(self.doc_path_index) as f:
            for line in f:
                yield {
                    "data":  line,
                }

    def index_data(self):
        response = helpers.bulk(
            self.client, self.gendata(), index=self.index_name, doc_type="_doc")

        print("helpers.bulk() RESPONSE: ", response)

    def shingles_request(self, question):

        question = Utilities.clean_elasticsearch(question)
        data = ElasticsearchUtils.DATA_FORMAT.format(
            self.num_candidates, question, question)

        response = requests.post(
            self.search_url, headers=ElasticsearchUtils.HEADER, params=ElasticsearchUtils.PARAMS, data=data)
        result_json = json.loads(response.text)
        return self.get_candidates(result_json)

    def get_candidates(self, json):
        candidates = []
        for i in range(0, len(json["hits"]["hits"])):
            candidates.append(json["hits"]["hits"][i]["_source"]["data"])

        candidates = list(set(candidates))

        return candidates


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./arc/conf/arc_configuration.conf')
    elasticsearch_config = config['elasticsearch']

    elasticsearch_util = ElasticsearchUtils(elasticsearch_config)
    elasticsearch_util.index_data()
