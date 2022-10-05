"""
Author: yangguang
Generate Date: Do not edit
LastEditors: lawrence-cell 850140027@qq.com
LastEditTime: 2022-10-04 10:54:14
FilePath: \mmse_test_py\main.py
Description: this file includes all the comonent of 

Copyright (c) 2022 by lawrence-cell 850140027@qq.com, All Rights Reserved. 
"""

import imp
from math import cos, sqrt
from interpolating_resampler.interpolating_resampler import *
from timing_error_detector.timing_error_detector import *
from utils.conv import *
import numpy as np
import scipy.io as scio
import collections


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


if __name__ == "__main__":
    sps = 8

    source_bit_stream = np.random.randint(
        0,
        2,
        [
            100,
        ],
    )

    interp_zero_sig = interp_with_zero(source_bit_stream, sps)

    filter = rcos_filter_root()
    test = np.arange(1, 10, 1)
    print(test[0:5])
    # m_interp = interpolating_resampler()
    # input_sig = np.linspace(0, 99, 100)
    # # mu = 0.5
    # # print(m_interp.interpolate(input_sig, 30, 0.5)).
    # m_interp.sync_reset(30.5)
    # print(m_interp.interpolate(input_sig, 30, m_interp.d_phase_wrap))
    # m_interp.advance_phase(8.3)

    # print(m_interp.interpolate(input_sig, 38, 0.8))
    # m_ted = ted_gardner()
    # m_ted.input(1)
    # m_ted.input(2)
    # m_ted.input(7)
    # print(m_ted.error())
