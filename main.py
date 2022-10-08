"""
Author: yanggguang 850140027@qq.com
Generate Date: Do not edit
LastEditors: Lawrence_cell 850140027@qq.com
LastEditTime: 2022-10-05 20:13:26
FilePath: /symbol_sync_py/main.py
Description: 

Copyright (c) 2022 by Lawrence_cell 850140027@qq.com, All Rights Reserved. 
"""

from faulthandler import dump_traceback
from lib2to3.pgen2.token import RPAR
from math import cos, sqrt

import symbol
from this import d
from interpolating_resampler.interpolating_resampler import *
from timing_error_detector.timing_error_detector import *
from clock_tracking_loop.clock_tracking_loop import *
from utils.conv import *
import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sps = 8
    output_sps = 1
    ted_sps = 2
    loop_bw = 0.045
    max_deviation = 1.5
    damping_factor = 1

    interps_per_symbol = ted_sps

    # source data
    f = np.fromfile(open("data_grc/before_symbol_sync"), dtype=np.complex64)

    d_interp = interpolating_resampler()
    d_clock_loop = clock_tracking_loop(
        loop_bw, sps + max_deviation, sps - max_deviation, sps, damping_factor
    )
    d_ted = ted_gardner()

    stop_point = len(f) - 8
    i = 0
    interpolants = []

    interp_clock = 1
    symbol_clock = 0
    d_inst_clock_period = 0

    times = 0
    while i <= stop_point:
        interp_clock = np.mod(interp_clock + 1, interps_per_symbol)
        symbol_clock = interp_clock == 0

        interp_output = d_interp.interpolate(f, i, d_interp.d_phase_wrap)
        interpolants.append(interp_output)

        d_ted.input(interp_output)
        ted_output = d_ted.error()

        if symbol_clock:
            d_clock_loop.advance_loop(ted_output)
            d_inst_clock_period = d_clock_loop.get_inst_period() / 2
            d_clock_loop.phase_wrap()

        d_interp.advance_phase(d_inst_clock_period)
        i += d_interp.d_phase_n

    temp = np.array(interpolants)
    final_output = temp[0::2]

    # test = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j])

    grc_output = np.fromfile(open("data_grc/grc_output"), dtype=np.complex64)

    # plt.figure()
    plt.scatter(final_output.real, final_output.imag, c="red")
    plt.scatter(grc_output.real, grc_output.imag, c="yellow")
    plt.show()

    # np.save("data_grc/py_output", f)
