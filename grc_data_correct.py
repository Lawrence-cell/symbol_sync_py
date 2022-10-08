import imp
from xml.sax.saxutils import prepare_input_source
from matplotlib.artist import ArtistInspector


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


print(eplison1000m)
