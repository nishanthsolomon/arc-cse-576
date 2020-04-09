import numpy as np


class Utilities:
    prediction_array = ['A', 'B', 'C', 'D']
    @staticmethod
    def pad_array(encoded_choides):
        b = np.zeros([len(encoded_choides), len(
            max(encoded_choides, key=lambda x: len(x)))], dtype=int)
        for i, j in enumerate(encoded_choides):
            b[i][0:len(j)] = j
        # print(b.shape)

        return b.tolist()

    @staticmethod
    def get_values_from_json_array(json_array, key):
        values = []
        for json_object in json_array:
            values.append(json_object[key])
        return values

    @staticmethod
    def get_prediction_mean(scores):
        score = np.array(scores).mean(axis=0)

        index = np.argmax(score)

        return Utilities.prediction_array[index]

    @staticmethod
    def get_prediction_max(scores):
        scores = np.asarray(scores)
        _, index = np.unravel_index(scores.argmax(), scores.shape)

        return Utilities.prediction_array[index]
