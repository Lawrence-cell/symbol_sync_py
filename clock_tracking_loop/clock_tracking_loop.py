"""
Author: yanggguang 850140027@qq.com
Generate Date: Do not edit
LastEditors: Lawrence_cell 850140027@qq.com
LastEditTime: 2022-10-05 19:37:26
FilePath: /symbol_sync_py/clock_tracking_loop/clock_tracking_loop.py
Description: 

Copyright (c) 2022 by Lawrence_cell 850140027@qq.com, All Rights Reserved. 
"""
from ast import If
from audioop import lin2adpcm
from mimetypes import init
from re import L
from select import select
from time import sleep
from tkinter import E
# from boto import set_file_logger
from keyring import set_keyring
import numpy as np
# from pandas import period_range


class clock_tracking_loop:
    # output of this whole block
    # in units of input samples
    _d_avg_period = 0
    _d_inst_period = 0

    _d_max_avg_period = 0
    _d_min_avg_period = 0
    _d_nom_avg_period = 0

    _d_phase = 0
    # damping factor of the 2nd order loop transfer function
    # 0.0 ~ 1.0 means under-damped
    # 1.0 ~ inf means over-damped
    # 1 means crtically-damped
    _d_zeta = 0
    # Normalized natural radian frequency of the 2nd order loop transfer function
    # omega_n_norm = omega_n*T  = 2*pi*f_n*T = 2*pi*f_n_norm
    _d_omega_n_norm = 0

    _d_ted_gain = 0
    # loop coeffcients
    _d_alpha = 0
    _d_beta = 0

    _d_prev_avg_period = 0
    _d_prev_inst_period = 0
    _d_prev_phase = 0

    def __init__(
        self,
        loop_bw,
        max_period,
        min_period,
        nominal_period=0.0,
        damping=0.0,
        ted_gain=1.0,
    ):
        self._d_avg_period = nominal_period
        self._d_max_avg_period = max_period
        self._d_min_avg_period = min_period
        self._d_nom_avg_period = nominal_period
        self._d_inst_period = nominal_period
        self._d_zeta = damping
        self._d_omega_n_norm = loop_bw
        self._d_ted_gain = ted_gain
        self._d_prev_avg_period = nominal_period
        self._d_prev_inst_period = nominal_period

    def get_avg_period(self):
        return self._d_avg_period

    def get_inst_period(self):
        return self._d_inst_period

    def get_phase_n(self):
        return np.floor(self._d_phase)

    def get_phase_wrap(self):
        return self._d_phase - self.get_phase_n()

    #####################################################SET FUNCTIONS###########################################################################
    def set_nom_avg_period(self, period):
        if period < self._d_min_avg_period or period > self._d_max_avg_period:
            self._d_nom_avg_period = (
                self._d_max_avg_period + self._d_min_avg_period
            ) / 2
        else:
            self._d_nom_avg_period = period

    def set_damping_factor(self, df):
        if df < 0:
            print("damping factor can not be under 0")
            return
        self._d_zeta = df
        self.update_gains()

    def set_loop_bw(self, loop_bw):
        if loop_bw < 0:
            print("loop_bw can not be below than 0")
            return
        self._d_omega_n_norm = loop_bw
        self.update_gains()

    def set_alpha(self, alpha):
        self._d_alpha = alpha

    def set_beta(self, beta):
        self._d_beta = beta

    def set_avg_period(self, period):
        self._d_avg_period = period
        self._d_prev_avg_period = period

    def set_inst_period(self, period):
        self._d_inst_period = period
        self._d_prev_inst_period = period

    def set_phase(self, phase):
        self._d_phase = phase
        self._d_prev_phase = phase

    #######################################################OPERATIONAL FUNCTION####################################################################
    """
    description:  acrooding to the damping factor and the loop bw to compute the alpha and beta
        _d_omega_n_norm = omega_n*T  = 2*pi*f_n*T = 2*pi*f_n_norm ------------> NORMALIZED
    return {*}
    """

    def update_gains(self):
        omega_n_T = self._d_omega_n_norm
        zeta_omega_n_T = self._d_zeta * omega_n_T
        k0 = 2 / self._d_ted_gain
        k1 = np.exp(-zeta_omega_n_T)
        sinh_zeta_omega_n_T = np.sinh(zeta_omega_n_T)

        self._d_alpha = k0 * k1 * sinh_zeta_omega_n_T
        temp = 0
        if self._d_zeta > 1:  # over damping
            omega_d_T = omega_n_T * np.sqrt(np.power(self._d_zeta, 2) - 1)
            temp = np.sinh(zeta_omega_n_T) + np.cos(omega_d_T)

        elif self._d_zeta == 1:  # critically damped
            temp = np.sinh(zeta_omega_n_T) + 1
        else:  # under damped
            omega_d_T = omega_d_T * np.sqrt(1 - np.power(self._d_zeta, 2))
            temp = np.sinh(zeta_omega_n_T) + np.cosh(omega_d_T)

        self._d_beta = k0 * (1 - k1 * temp)

    """
    description:  receive the output of the ted and pass the clock loop
    advance means about to get ahead one sample output
    param {*} self
    param {*} error the input of the last block TED
    return {*}
    """

    def advance_loop(self, error):
        self._d_prev_avg_period = self._d_avg_period
        self._d_prev_inst_period = self._d_inst_period
        self._d_prev_phase = self._d_phase

        # intergral arm of loop filter
        self._d_avg_period = self._d_avg_period + self._d_beta * error
        self.period_limit()
        # proportional arm of loop filter
        # inst is the final output of the whole loop
        self._d_inst_period = self._d_avg_period + self._d_alpha * error

        if self._d_inst_period <= 0:
            self._d_inst_period = self._d_avg_period

        # self._d_phase = self._d_phase + self._d_inst_period
        # self._d_phase_n = np.floor(self._d_phase)
        # self._d_phase_wrap

    """
    description:  constraint the output in a limited zone
    param {*} self
    return {*}
    """

    def period_limit(self):
        if self._d_avg_period > self._d_max_avg_period:
            self._d_avg_period = self._d_max_avg_period
        elif self._d_avg_period < self._d_min_avg_period:
            self._d_avg_period = self._d_min_avg_period

    def revert_loop(self):
        self._d_avg_period = self._d_prev_avg_period
        self._d_inst_period = self._d_prev_inst_period
        self._d_phase = self._d_prev_phase

    """
    description: constrain the phase is in the period (- avg_period /2 , avg_period/2)  
    param {*} self
    return {*}
    """

    def phase_wrap(self):
        period = self._d_avg_period
        limit = period / 2

        while self._d_phase > limit:
            self._d_phase -= period

        while self._d_phase < -limit:
            self._d_phase += period
