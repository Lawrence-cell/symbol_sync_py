"""
Author: yanggguang 850140027@qq.com
Generate Date: Do not edit
LastEditors: lawrence-cell 850140027@qq.com
LastEditTime: 2022-10-08 11:21:40
FilePath: \symbol_sync_py\data_test.py
Description: 

Copyright (c) 2022 by lawrence-cell 850140027@qq.com, All Rights Reserved. 
"""
import numpy as np
import matplotlib.pyplot as plt

f = np.fromfile(open("data_grc/grc_output"), dtype=np.complex64)


plt.figure()
plt.scatter(f.real, f.imag)
plt.show()
