"""
Author: lawrence-cell 850140027@qq.com
Generate Date: Do not edit
LastEditors: lawrence-cell 850140027@qq.com
LastEditTime: 2022-09-29 19:03:33
FilePath: \mmse_test\manual_mmse_filter.py
Description: this script is used for learning mmse interpolator filter. the requirement is not allowed to use any module 
except the most base library


Copyright (c) 2022 by lawrence-cell 850140027@qq.com, All Rights Reserved. 
"""

from cgi import print_arguments
import numpy as np
from black import find_project_root
from filter_taps.mmse_filter_taps import taps

# func used to conv two sig, and m_filter is the filter which is not casual, that is it need to know the future input
# the taps num of filter is even
def conv(sig1, m_filter):
    output = []
    filter_taps_num = len(m_filter)
    wait_len = filter_taps_num / 2
    output_len = len(sig1) - wait_len
    for i in range(int(output_len)):
        temp = 0
        if i < wait_len - 1:
            output.append(0)
        else:
            relative_offset_ahead = -3
            relative_offset_back = relative_offset_ahead + filter_taps_num
            sig_value = sig1[i + relative_offset_ahead : i + relative_offset_back]
            # usage  list[start:end] will include elements whose index is from start to end-1

            for k in range(filter_taps_num):
                temp = temp + sig_value[k] * m_filter[k]
            output.append(temp)
            temp = 0
    return output


def choose_filter(mu):
    filter_index = round(mu * len(taps))
    filter = taps[filter_index]
    return filter


if __name__ == "__main__":
    # input_sig = np.zeros((160,), dtype=int)

    # for i in range(16):
    #     input_sig[i * 10] = 1

    input_sig = np.linspace(0, 99, 100)
    mu = 0.5
    mmse_filter = choose_filter(mu)
    # testfilter = np.linspace(1, 8, 8)
    filter_output = conv(input_sig, mmse_filter)
    for i in filter_output:
        print(i)
    # temp = 0
    # for i in np.linspace(1, 8, 8):
    #     temp = temp + i * (9 - i)
    # print(temp)
    # plt.figure()
    # plt.subplot(2, 1, 1)
    # plt.plot(np.linspace(0, 7, 8), mmse_filter)
    # plt.subplot(2, 1, 2)

    # plt.plot(np.linspace(0, len(filter_output), len(filter_output)), filter_output)
    # plt.show()
