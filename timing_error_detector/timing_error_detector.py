"""
Author: lawrence-cell 850140027@qq.com
Generate Date: Do not edit
LastEditors: lawrence-cell 850140027@qq.com
LastEditTime: 2022-10-04 16:03:19
FilePath: \mmse_test_py\timing_error_detector\timing_error_detector.py
Description: 

Copyright (c) 2022 by lawrence-cell 850140027@qq.com, All Rights Reserved. 
"""
from abc import abstractmethod
from enum import Enum
import collections
from operator import mod
from black import err

TED_TYPE = Enum("TED_TYPE", ("GARDNER", "EARLY_LATE"))


class timing_error_detector:
    _d_type = TED_TYPE.GARDNER
    _d_inputs_per_symbol = 2
    _d_error = 0
    _d_prev_error = 0
    _d_error_depth = 3
    _d_input = collections.deque()
    _d_input_clock = 0

    def __init__(self, type, inputs_per_sample, error_depth):
        self._d_inputs_per_symbol = inputs_per_sample
        self._d_error_depth = error_depth
        for i in range(error_depth):
            self._d_input.append(complex(0, 0))

    def error(self):
        return self._d_error

    def inputs_per_symbol(self):
        return self._d_inputs_per_symbol

    def _advance_input_clock(self):
        self._d_input_clock = mod((self._d_input_clock + 1), self._d_inputs_per_symbol)

    @abstractmethod
    def _compute_error_ff(self):
        pass

    # suppose the date type is complex
    def input(self, single_data):
        self._d_input.append(single_data)
        self._advance_input_clock()
        self._d_input.popleft()
        self._d_error = self._compute_error_ff()


class ted_gardner(timing_error_detector):
    def __init__(self):
        super().__init__(TED_TYPE.GARDNER, 2, 3)

    def _compute_error_ff(self):
        #     return ((d_input[0].real() - d_input[2].real()) * d_input[1].real()) +
        #    ((d_input[0].imag() - d_input[2].imag()) * d_input[1].imag());
        return (self._d_input[0].real - self._d_input[2].real) * self._d_input[
            1
        ].real + (self._d_input[0].imag - self._d_input[2].imag) * self._d_input[1].imag
