import requests
import json


class ElasticsearchQuery():
    def __init__(self, config):
        self.request_url = config['request_url']
        self.num_candidates = config['num_candidates']

        self.headers = {
            'Content-Type': 'application/json',
        }
        self.params = (
            ('pretty', ''),
        )
        self.data_format = '{{"size": {}, "query": {{ "bool": {{ "must": {{ "match": {{ "data": "{}" }} }}, "should": {{ "match": {{ "data.shingles": "{}" }} }} }} }} }}'

    def shingles_request(self, question):

        data = self.data_format.format(self.num_candidates, question, question)

        response = requests.post(
            self.request_url, headers=self.headers, params=self.params, data=data)
        result_json = json.loads(response.text)
        return self.get_candidates(result_json)

    def get_candidates(self, json):
        candidates = []
        for i in range(0, len(json["hits"]["hits"])):
            candidates.append(json["hits"]["hits"][i]["_source"]["data"])

        return candidates
