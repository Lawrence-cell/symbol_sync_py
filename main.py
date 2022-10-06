"""
Author: yanggguang 850140027@qq.com
Generate Date: Do not edit
LastEditors: Lawrence_cell 850140027@qq.com
LastEditTime: 2022-10-05 19:22:08
FilePath: /symbol_sync_py/main.py
Description: 

Copyright (c) 2022 by Lawrence_cell 850140027@qq.com, All Rights Reserved. 
"""
"""
Author: yangguang
Generate Date: Do not edit
LastEditors: lawrence-cell 850140027@qq.com
LastEditTime: 2022-10-04 10:54:14
FilePath: \mmse_test_py\main.py
Description: this file includes all the comonent of the "symbol_sync" block in the gnuradio, 
and the data source is the binary file exported by the gnuradio in linux
by comparing the output of this python project with the output of grc to inspect the correctness of this implementation

Copyright (c) 2022 by lawrence-cell 850140027@qq.com, All Rights Reserved. 
"""

import imp
from lib2to3.pgen2.token import RPAR
from math import cos, sqrt
from interpolating_resampler.interpolating_resampler import *
from timing_error_detector.timing_error_detector import *
from utils.conv import *
import numpy as np
import scipy.io as scio
import collections


if __name__ == "__main__":
    sps = 8
    f = np.fromfile(open("data_grc/befor_sysmbol_sync"), dtype=np.complex)

    test = np.sqrt(np.power(9, 2))
    print(test)

    # input_sig = []

    # for i in range(100):
    #     input_sig.append(complex(i, i))

    # d_interp = interpolating_resampler()

    # for i in range(100):
    #     print(d_interp.interpolate(input_sig, i, 0.5))

    # d_ted = ted_gardner()
    # d_ted.input(complex(1 + 2j))
    # d_ted.input(complex(1 + 3j))
    # d_ted.input(complex(2 + 3j))

    # print(d_ted.error())
