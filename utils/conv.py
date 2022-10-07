import imp
# from black import out


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

def interp_with_zero(intput_sig, sps):
    sig_len = len(intput_sig)
    interpolated_sig = np.zeros((sps * sig_len,))
    for i in range(sig_len):
        interpolated_sig[i * sps] = intput_sig[i]
    return interpolated_sig


def rcos_filter_root():

    # filter_half_span = (int)(span * sps / 2)
    # n_period = np.arange(-filter_half_span, filter_half_span, 1, dtype=int)
    # analog_sig = np.zeros((sps * span + 1,))
    # for i in n_period:
    #     analog_sig[i + filter_half_span] = np.sinc(i / sps) * (
    #         cos(np.pi * rolloff_factor * (i / sps))
    #         / (1 - 4 * pow(rolloff_factor, 2) * pow(i / sps, 2))
    #     )
    datafile = "filter_taps/rcos_5f_6_8.mat"
    data = scio.loadmat(datafile)
    data = data["filter"]
    return data[0]