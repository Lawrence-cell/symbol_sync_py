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
from this import d
from interpolating_resampler.interpolating_resampler import *
from timing_error_detector.timing_error_detector import *
from clock_tracking_loop.clock_tracking_loop import *
from utils.conv import *
import numpy as np
import scipy.io as scio
import collections


def sync_reset_internal_clocks(d_interps_per_symbol_n):
    return d_interps_per_symbol_n - 1
    update_internal_clock_outputs()


def update_internal_clock_outputs(
    d_interp_clock,
    d_interps_per_ted_input_n,
    d_interps_per_output_sample_n,
    d_interps_per_symbol_n,
):
    d_ted_input_clock = d_interp_clock % d_interps_per_ted_input_n == 0
    d_output_sample_clock = d_interp_clock % d_interps_per_output_sample_n == 0
    d_symbol_clock = d_interp_clock % d_interps_per_symbol_n == 0


if __name__ == "__main__":
    sps = 8
    output_sps = 1
    d_ted_sps = 2
    f = np.fromfile(open("data_grc/befor_sysmbol_sync"), dtype=np.complex)
    # print(f)
    #        loop_bw,
    # max_period,
    # min_period,
    #  d_clock(loop_bw,
    #           sps + max_deviation,
    #           sps - max_deviation,
    #           sps,
    #           damping_factor,
    #           ted_gain),
    d_interp = interpolating_resampler()
    d_clock_loop = clock_tracking_loop(0.045, 8 + 1.5, 8 - 1.5, 8, 1)
    d_ted = ted_gardner()

    stop_point = len(f) - 8
    i = 0
    interpolants = []
    while i <= stop_point:
        interp_output = d_interp.interpolate(f, i, d_interp.d_phase_wrap)
        interpolants.append(interp_output)
        d_ted.input(interp_output)
        ted_output = d_ted.error()
        d_clock_loop.advance_loop(ted_output)
        d_inst_clock_period = d_clock_loop.get_inst_period() / 2
        d_interp.advance_phase(d_inst_clock_period)
        i += d_interp.d_phase_n

    # tmp = interpolants[::2]
    # b = []
    # for a in tmp:
    #     b.append(a.real)
    #     b.append(a.imag)
    # # tmp = [c.real,c.imag for c in tmp]
    # import struct

    # NN = len(b)
    # tmp_bytes = struct.pack(NN * "f", *b)
    # with open("test.dat", "wb") as f:
    #     f.write(tmp_bytes)

    temp = np.array(interpolants)
    final_output = temp[0::2]
    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(final_output.real, final_output.imag)
    plt.savefig("test.png")
    # plt.show()

    # print(len(final_output[0:]))

    np.save("data_grc/output_py", final_output)

    # final_output.tofile("data_grc/output_py")
    # print(len(final_output))

    # output_gnuradio = np.fromfile(open("data_grc/output_gnuradio"), dtype=np.complex)
    # print(len(output_gnuradio))

    # d_interps_per_symbol_n = 2
    # d_interps_per_ted_input_n = d_interps_per_symbol_n / 2
    # d_interps_per_output_sample_n = d_interps_per_symbol_n / output_sps

    # d_interp_clock = d_interps_per_symbol_n - 1

    # d_interps_per_symbol_n = std::lcm(d_ted->inputs_per_symbol(), d_osps_n);
    # d_interps_per_ted_input_n = d_interps_per_symbol_n / d_ted->inputs_per_symbol();
    # d_interps_per_output_sample_n = d_interps_per_symbol_n / d_osps_n;

    # d_interps_per_symbol = static_cast<float>(d_interps_per_symbol_n);
    # d_interps_per_ted_input = static_cast<float>(d_interps_per_ted_input_n);

    # d_interp_clock = d_interps_per_symbol_n - 1;
    # sync_reset_internal_clocks();
    # d_inst_interp_period = d_inst_clo ck_period / d_interps_per_symbol;

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
