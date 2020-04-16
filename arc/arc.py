import sys
from dataset_readers.arc_datasetreader import ArcDatasetReader
from predictors.xlnet_predictor import XlnetPredictor
from elasticsearch_utils.elasticsearch_utils import ElasticsearchUtils
from textual_entailment.textual_entailment import TextualEntailment
from utils.utils import Utilities
from sklearn.metrics import accuracy_score


class ARC():
    def __init__(self, config):
        textual_entailment_config = config['textual_entailment']
        elasticsearch_config = config['elasticsearch']
        xlnet_config = config['xlnet']
        self.textual_entailment = TextualEntailment(textual_entailment_config)
        self.elasticsearch = ElasticsearchUtils(elasticsearch_config)
        self.xlnet = XlnetPredictor(xlnet_config)
        self.arc_datasetreader = ArcDatasetReader()

    def get_candidates(self, search_phrase):
        elasticsearch_candidates = self.elasticsearch.shingles_request(
            search_phrase)
        textual_entailment_candidates = self.textual_entailment.get_entailment_candidate_list(
            search_phrase, elasticsearch_candidates)

        return textual_entailment_candidates

    def get_prediction(self, question, choices):
        search_phrase = question + ' ' + ' '.join(choices)
        candidates = self.get_candidates(search_phrase)
        scores = []
        for candidate in candidates:
            input = []
            for choice in choices:
                input.append(
                    ' '.join([candidate.strip(), question.strip(), choice.strip()]))
            score = self.xlnet.predict_answer(input)[0].detach().numpy()
            scores.append(score)
        prediction = Utilities.get_prediction_max(scores)
        return prediction

    def analyse_dataset(self, path, num_questions):

        ground_truth = []
        predictions = []
        for question, choices, answer_key in self.arc_datasetreader.read_arc_dataset(path):
            if (num_questions == len(ground_truth)):
                break
            ground_truth.append(answer_key)
            prediction = self.get_prediction(question, choices)
            predictions.append(prediction)
            print('Question : ' + str(question) + '\nChoices : ' + str(choices) +
                  '\nGround Truth : ' + str(answer_key) + '\nPredicted : ' + str(prediction) + '\n')

        accuracy = accuracy_score(ground_truth, predictions)
        return accuracy
