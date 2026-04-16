#ifndef SWARMRAFT_H
#define SWARMRAFT_H

typedef struct {
    double x,y,z;
} pos;

void verify_and_recover(
    int n, 
    pos* rep, 
    double* dist_matrix, 
    double threshold, 
    double epsilon, 
    int max_iter, 
    pos* out_verified, 
    int* out_faulty_flags
);

#endif