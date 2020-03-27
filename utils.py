
import numpy as np

class Utilities:
    @staticmethod
    def pad_array(encoded_choides):
        b = np.zeros([len(encoded_choides), len(max(encoded_choides, key=lambda x: len(x)))], dtype=int)
        for i, j in enumerate(encoded_choides):
            b[i][0:len(j)] = j
        # print(b.shape)

        return b.tolist();

    @staticmethod
    def get_values_from_json_array(arr, key):
        values = []
        for key_val in arr:
            values.append(key_val[key])
        return values

