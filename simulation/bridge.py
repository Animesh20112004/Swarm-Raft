import ctypes
import numpy as np
import os

class Point3D(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double),
                ("z", ctypes.c_double)]

class SwarmRaftBridge:
    def __init__(self, lib_path='core/build/libswarmraft.so'):
        self.lib = ctypes.CDLL(os.path.abspath(lib_path))
        
        self.lib.verify_neighbors.argtypes = [
            ctypes.c_int, 
            ctypes.POINTER(Point3D), 
            ctypes.POINTER(ctypes.c_double), 
            ctypes.c_double, 
            ctypes.POINTER(ctypes.c_bool)
        ]
        
        self.lib.recover_position.argtypes = [
            ctypes.c_int, 
            ctypes.c_int, 
            ctypes.POINTER(Point3D), 
            ctypes.POINTER(ctypes.c_double), 
            ctypes.POINTER(ctypes.c_bool), 
            ctypes.c_int
        ]
        self.lib.recover_position.restype = Point3D

    def run_swarmraft(self, reports, dist_matrix, threshold=5.0):
        n = len(reports)
        
        c_reports = (Point3D * n)(*[Point3D(*r) for r in reports])
        
        c_dist_matrix = dist_matrix.flatten().astype(np.float64).ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        
        fault_flags = (ctypes.c_bool * n)()
        
        self.lib.verify_neighbors(n, c_reports, c_dist_matrix, threshold, fault_flags)
        
        recovered_positions = []
        for i in range(n):
            if fault_flags[i]:
                rec_p = self.lib.recover_position(i, n, c_reports, c_dist_matrix, fault_flags, 100)
                recovered_positions.append([rec_p.x, rec_p.y, rec_p.z])
            else:
                recovered_positions.append(reports[i])
                
        return np.array(recovered_positions), list(fault_flags)