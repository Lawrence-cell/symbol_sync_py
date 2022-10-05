import imp
from black import out


import numpy as np


def conv(sig, filter):
    sig_len = len(sig)
    filter_len = len(filter)
    filter_reverse = filter[::-1]

    len_of_extend_sig = filter_len * 2 + sig_len
    output = np.zeros[(filter_len + sig_len, 1)]
    sig_extend = np.zeros[(len_of_extend_sig, 1)]
    sig_extend[filter_len : filter_len + sig_len] = sig
    for i in range(len(output)):
        temp = 0
        for k in range(filter_len):
            temp = temp + sig_extend[i + k] * filter_reverse[k]
        output[i] = temp
    return output
