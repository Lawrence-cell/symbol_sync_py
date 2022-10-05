from math import floor
from pyrsistent import m
from filter_taps.mmse_filter_taps import taps

class interpolating_resampler:
    # relative value, normally less than sps
    d_phase = 0
    d_phase_n = 0
    d_phase_wrap = 0
    d_prev_phase = 0
    d_prev_phase_n = 0
    d_prev_phase_wrap = 0
    d_filter_bank = taps

    def __init__(self) -> None:
        pass
    
    # interpolate: use the member varibles filterbank to conv to produce one interpolant
    def interpolate(self, input_sig, basepoint, mu):
        filter_len = len(self.d_filter_bank[1])
        #NSTEPS : number of filterbanks
        NSTEPS = 128
        if basepoint < 0 or basepoint > len(input_sig) - filter_len:
            print("ERROR, the length of the input signal is not enough")
            return
        filter_index = round(mu * NSTEPS)
        m_filter = self.d_filter_bank[filter_index]
        # reverse the filter
        m_filter = m_filter[::-1]
        temp = 0
        #conv: it will introduce filter_len/2 delay
        for i in range(filter_len):
            temp = temp + m_filter[i] * input_sig[basepoint + i]
        return temp

    # update the value of {d_phase, d_phase_n, d_phase_wrap}
    def next_phase(self, increment):
        self.d_phase = self.d_phase_wrap + increment
        self.d_phase_n = floor(self.d_phase)
        self.d_phase_wrap = self.d_phase - self.d_phase_n
    
    # propagae the value of {d_phase, d_phase_n, d_phase_wrap} to {d_prev_phase, d_prev_phase_n, d_prev_phase_wrap}
    # update the value of {d_phase, d_phase_n, d_phase_wrap}
    def advance_phase(self, increment):
        self.d_prev_phase = self.d_phase
        self.d_prev_phase_n = self.d_phase_n
        self.d_prev_phase_wrap = self.d_phase_wrap
        self.next_phase(increment)

    #back to the situation of the last interpolation
    def revert_phase(self):
        self.d_phase = self.d_prev_phase
        self.d_phase_n = self.d_prev_phase_n
        self.d_phase_wrap = self.d_prev_phase_wrap

    def sync_reset(self, phase):
        self.d_phase = phase
        self.d_phase_n = floor(phase)
        self.d_phase_wrap = phase - floor(phase)

        self.d_prev_phase = phase
        self.d_prev_phase_n = floor(phase)
        self.d_prev_phase_wrap = phase - floor(phase)

        
    