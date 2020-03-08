from allennlp.predictors.predictor import Predictor


predictor = Predictor.from_path("./models/decomposable-attention-elmo-2018.02.19.tar.gz")
prediction = predictor.predict(
  hypothesis="The elephant was lost.",
  premise="A large, gray elephant walked beside a herd of zebras."
)

entailment = prediction['label_probs'][0]
contradiction = prediction['label_probs'][1]
neutral = prediction['label_probs'][2]

print('entailment : ' + str(entailment))
print('contradiction : ' + str(contradiction))
print('neutral : ' + str(neutral))