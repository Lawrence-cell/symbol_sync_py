"""
Author: yanggguang 850140027@qq.com
Generate Date: Do not edit
LastEditors: lawrence-cell 850140027@qq.com
LastEditTime: 2022-10-08 21:28:51
FilePath: \symbol_sync_py\grc_data_correct.py
Description: 

Copyright (c) 2022 by lawrence-cell 850140027@qq.com, All Rights Reserved. 
"""
import imp

import matplotlib.pyplot as plt


import numpy as np

eplison800m = np.fromfile(
    open("data_grc/eplison800m"),
    dtype=np.complex64,
)
eplison850m = np.fromfile(
    open("data_grc/eplison850m"),
    dtype=np.complex64,
)
eplison900m = np.fromfile(
    open("data_grc/eplison900m"),
    dtype=np.complex64,
)
eplison1000m = np.fromfile(
    open("data_grc/eplison1000m"),
    dtype=np.complex64,
)


# min_len = min(len(eplison1000m), len(eplison800m), len(eplison850m), len(eplison900m))
min_len = 200
x = np.arange(0, min_len, 1)

plt.plot(x, eplison1000m[0:min_len].real, c="red")
plt.plot(x, eplison900m[0:min_len].real, c="blue")
# plt.scatter(x, eplison850m[0:min_len].real, c="y ellow")
plt.show()
