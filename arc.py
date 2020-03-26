import configparser
import sys
from textual_entailment import TextualEntailment
from elasticsearch_query import ElasticsearchQuery
from transformers import XLNetTokenizer, XLNetForMultipleChoice
from answerPredictor import AnswerPredictor
from datasetAnalyser import DataAnalyzer

class ARC():
    def __init__(self, config):
        textual_entailment_config = config['textual_entailment']
        elasticsearch_config = config['elasticsearch']
        textual_entailment = TextualEntailment(textual_entailment_config)
        elasticsearch = ElasticsearchQuery(elasticsearch_config)
        tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')
        model = XLNetForMultipleChoice.from_pretrained('xlnet-base-cased')
        predictor = AnswerPredictor(tokenizer, model)
        self.dataset_analyzer = DataAnalyzer(textual_entailment, elasticsearch, predictor)

    def analyse_dataset(self, path, num_rows):
        return self.dataset_analyzer.analyze_arc_dataset(path, num_rows)

if __name__ == "__main__":
    arguments = len(sys.argv) - 1
    config = configparser.ConfigParser()
    config.read('./arc_configuration.conf')
    arc = ARC(config)
    # question = 'Clean and organize around the house.'
    # candidates = arc.get_candidates(question)
    path = sys.argv[1]
    numRows = 5
    if len(sys.argv) > 2:
        numRows = int(sys.argv[2])
    accuracy = arc.analyse_dataset(path, numRows)

    print("Reported accuracy = " + str(accuracy))
