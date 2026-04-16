import ctypes
import os
import numpy as np

class Position(ctypes.Structure):
    _fields_=[("x",ctypes.c_double),("y",ctypes.c_double),("z",ctypes.c_double)]
class Bridge:
    def __init__(self):
        lib_path=os.path.abspath("core/build/libswarmraft.so")
        self.lib=ctypes.CDLL(lib_path)
        self.lib.verify_and_recover.argtypes=[
            ctypes.c_int,ctypes.POINTER(Position),ctypes.POINTER(ctypes.c_double),
            ctypes.c_double,ctypes.c_double,ctypes.c_int,
            ctypes.POINTER(Position),ctypes.POINTER(ctypes.c_int)
        ]
    def run_consensus(self, drones, dist_mat):
        n=len(drones)
        reported=(Position*n)(*[Position(*d.reported_pos) for d in drones])
        distances=(ctypes.c_double * (n * n))(*dist_mat.flatten())
        verify_arr=(Position *n)()
        flags=(ctypes.c_int* n)()
        self.lib.verify_and_recover(n,reported,distances,2.0,5.0,100,verify_arr,flags)
        return [np.array([v.x, v.y, v.z])for v in verify_arr],list(flags)