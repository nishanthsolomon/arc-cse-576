from utils import Utilities
import torch
class AnswerPredictor:

    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    def predict_answer(self, question_choices):
        encoded_choices = [self.tokenizer.encode(s) for s in question_choices]
        padded_choices = Utilities.pad_array(encoded_choices)
        # input_ids = torch.from_numpy(padded_array).unsqueeze(0)
        input_ids = torch.tensor(padded_choices).unsqueeze(0)  # Batch size 1, 2 choices
        labels = torch.tensor(3).unsqueeze(0)  # Batch size 1
        #
        outputs = self.model(input_ids, labels=labels)
        # print(outputs)
        loss, classification_scores = outputs[:2]
        return classification_scores