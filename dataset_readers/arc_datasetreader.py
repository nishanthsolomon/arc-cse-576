import json
from utils.utils import Utilities


class ArcDatasetReader():
    def __init__(self):
        pass

    def read_arc_dataset(self, path):
        with open(path) as file_dataset:
            corpus = file_dataset.read().splitlines()
            for data in corpus:
                json_data = json.loads(data)
                question = json_data['question']['stem']
                choices_json = json_data['question']['choices']
                choices = Utilities.get_values_from_json_array(
                    choices_json, 'text')
                answer_key = json_data['answerKey']
                if answer_key in Utilities.nums:
                    answer_key = Utilities.prediction_array[int(
                        answer_key) - 1]
                yield question, choices, answer_key
