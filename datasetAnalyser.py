import json
from utils import Utilities
import torch
import numpy as np
from sklearn.metrics import accuracy_score


class DataAnalyzer:
    def __init__(self, textual_entailment, elasticsearch, answer_predictor):
        self.textual_entailment = textual_entailment
        self.elasticsearch = elasticsearch
        self.predictor = answer_predictor

    def get_candidates(self, question):
        question = question.encode(
                    "ascii", "ignore").decode("utf-8", "ignore")
        elasticsearch_candidates = self.elasticsearch.shingles_request(
            question)
        candidates = self.textual_entailment.get_entailment_candidate_list(
            question, elasticsearch_candidates)

        return candidates

    def predict_for_all_facts(self, question, candidate_facts, choices):
        max_index = -1
        global_max = float("-inf")
        predictionArray = ['A', 'B', 'C', 'D']

        for fact in candidate_facts:
            input = []
            for choice in choices:
                input.append(question.rstrip() + fact.rstrip() + choice)
            classification_scores = self.predictor.predict_answer(input)
            scores = classification_scores[0].detach().numpy()
            index = np.argmax(scores)
            max_val = scores[index]
            if max_val > global_max:
                global_max = max_val
                max_index = index

        return predictionArray[max_index]

    def analyze_arc_dataset(self, path, num_rows):
        ground_truth = []
        prediction = []
        count = 0
        with open(path) as f:
            data = f.readlines()
            for i, a in enumerate(data):
                if count == num_rows:
                    break
                b = json.loads(a)
                question = b['question']['stem']
                choices_json = b['question']['choices']
                choices = Utilities.get_values_from_json_array(
                    choices_json, 'text')
                answer_key = b['answerKey']
                ground_truth.append(answer_key)
                candidates = self.get_candidates(question)
                predicted_answer = self.predict_for_all_facts(
                    question, candidates, choices)
                prediction.append(predicted_answer)
                print('Question : ' + str(question) + '\nChoices : ' + str(choices) +
                      '\nGround Truth : ' + str(answer_key) + '\nPredicted : ' + str(predicted_answer))
                count += 1

        acc = accuracy_score(ground_truth, prediction)
        return acc
