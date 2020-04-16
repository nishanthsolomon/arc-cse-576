import torch
from utils.utils import Utilities
from transformers import XLNetTokenizer, XLNetForMultipleChoice


class XlnetPredictor():
    def __init__(self, config, cuda_device=-1):
        self.cuda_device = False if cuda_device == -1 else True
        model_path = config['model_path']
        self.tokenizer = XLNetTokenizer.from_pretrained(model_path)
        if (self.cuda_device):
            self.model = XLNetForMultipleChoice.from_pretrained(model_path).to('cuda')
        else:
            self.model = XLNetForMultipleChoice.from_pretrained(model_path)

    def predict_answer(self, choices):
        encoded_choices = [self.tokenizer.encode(s) for s in choices]
        padded_choices = Utilities.pad_array(encoded_choices)

        input_ids = torch.tensor(padded_choices).unsqueeze(0)
        labels = torch.tensor(3).unsqueeze(0)

        if (self.cuda_device):
            input_ids = input_ids.to('cuda')
            labels = labels.to('cuda')

        outputs = self.model(input_ids, labels=labels)

        loss, classification_scores = outputs[:2]
        return classification_scores
