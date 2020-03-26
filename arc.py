import configparser
from textual_entailment import TextualEntailment
from elasticsearch_query import ElasticsearchQuery
from transformers import XLNetTokenizer, XLNetForMultipleChoice
from answerPredictor import AnswerPredictor


class ARC():
    def __init__(self, config):
        textual_entailment_config = config['textual_entailment']
        elasticsearch_config = config['elasticsearch']

        self.textual_entailment = TextualEntailment(textual_entailment_config)
        self.elasticsearch = ElasticsearchQuery(elasticsearch_config)

    def get_candidates(self, question):
        elasticsearch_candidates = self.elasticsearch.shingles_request(
            question)
        candidates = self.textual_entailment.get_entailment_candidate_list(
            question, elasticsearch_candidates)

        return candidates


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./arc_configuration.conf')

    tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')
    model = XLNetForMultipleChoice.from_pretrained('xlnet-base-cased')

    arc = ARC(config)

    predictor = AnswerPredictor(tokenizer, model)

    question = 'Clean and organize around the house.'
    candidates = arc.get_candidates(question)
