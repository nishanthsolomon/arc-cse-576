from allennlp.predictors.predictor import Predictor


class TextualEntailment():
    def __init__(self, config, cuda_device=-1):
        model_path = config['model_path']
        self.num_candidates = int(config['num_candidates'])
        self.predictor = Predictor.from_path(
            model_path, cuda_device=cuda_device)

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

        candidates = sorted(
            candidates, key=lambda x: float(x[1]), reverse=True)

        candidates = [candidate[0]
                      for candidate in candidates[:self.num_candidates]]

        return candidates
