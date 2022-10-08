import imp
from matplotlib.artist import ArtistInspector


import numpy as np

after_interp = np.fromfile(
    open("/home/yangguang/Desktop/symbol_sync_py/data_grc/grc_after_interp"),
    dtype=np.complex64,
)
ted_error = np.fromfile(
    open("/home/yangguang/Desktop/symbol_sync_py/data_grc/grc_after_ted"),
    dtype=np.float32,
)
loop_output = np.fromfile(
    open("/home/yangguang/Desktop/symbol_sync_py/data_grc/grc_after_loop"),
    dtype=np.float32,
)


# np.save("data_grc/py_output", after_interp[0::2])
print(loop_output[0:100])
