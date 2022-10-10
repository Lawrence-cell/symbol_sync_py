import imp
from xml.sax.saxutils import prepare_input_source
import matplotlib.pyplot as plt


import numpy as np

eplison800m = np.fromfile(
    open("/home/yangguang/Desktop/symbol_sync_py/data_grc/eplison800m"),
    dtype=np.complex64,
)
eplison850m = np.fromfile(
    open("/home/yangguang/Desktop/symbol_sync_py/data_grc/eplison850m"),
    dtype=np.float32,
)
eplison900m = np.fromfile(
    open("/home/yangguang/Desktop/symbol_sync_py/data_grc/eplison900m"),
    dtype=np.float32,
)
eplison1000m = np.fromfile(
    open("/home/yangguang/Desktop/symbol_sync_py/data_grc/eplison1000m"),
    dtype=np.float32,
)


max_len = max(len(eplison1000m), len(eplison800m), len(eplison850m), len(eplison900m))
x = np.arange(0, max_len, 1)
for i in [eplison1000m, eplison800m, eplison850m, eplison900m]:
    while len(i) < max_len:
        np.append(i, 0)
plt.plot(x, eplison1000m, c="red")
plt.plot(x, eplison850m, c="blue")
plt.show()
