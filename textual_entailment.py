from allennlp.predictors.predictor import Predictor


class TextualEntailment():
    def __init__(self, config):
        model_path = config['model_path']

        self.predictor = Predictor.from_path(model_path)

    def get_entailment_score(self, hypothesis, premise):
        prediction = self.predictor.predict(
            hypothesis=hypothesis,
            premise=premise
        )

        entailment_score = prediction['label_probs'][0]
        contradiction_score = prediction['label_probs'][1]
        neutral_score = prediction['label_probs'][2]

        return entailment_score

    def get_entailment_candidate_list(self, question, elasticsearch_candidates):
        candidates = []
        for elasticsearch_candidate in elasticsearch_candidates:
            entailment_score = self.get_entailment_score(
                question, elasticsearch_candidate)
            candidates.append((elasticsearch_candidate, entailment_score))

        sorted(candidates, key=lambda x: (-x[1]))

        candidates = [candidate[0] for candidate in candidates]

        candidates = candidates[:5]
        return candidates
