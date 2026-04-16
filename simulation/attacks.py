import numpy as np
def attack_module(drone_arr,count,offset=20.0):
    arr=np.random.choice(len(drone_arr),count,replace=False)
    for i in arr:
        drone_arr[i].is_spoofed=True
        drone_arr[i].reported_pos+=np.random.uniform(offset,(offset*2),size=3)