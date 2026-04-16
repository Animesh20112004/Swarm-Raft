#include"swarmraft.h"
#include<math.h>
#include<stdlib.h>

void verify_and_recover(int n,pos * rep,double * dist_mat,double thresh,double eps,int max_iter,pos *veri_arr,int *spoof_count) {
    for(int i=0;i<n;i++){
        int v=0;
        for(int j=0;j<n;j++){
            if(i==j)continue;
            double x=rep[i].x-rep[j].x;
            double y=rep[i].y-rep[j].y;
            double z=rep[i].z-rep[j].z;
            double calc_distance=sqrt(x*x+y*y+z*z);
            if(fabs(calc_distance-dist_mat[i*n+j])<thresh)v++;
            else v--;
        }
        spoof_count[i]=(v<0)?1:0; 
        veri_arr[i]=rep[i];
    }
    for(int i=0; i<n;i++){
        if(spoof_count[i]){
            pos p=rep[i]; 
            for (int iter=0; iter<max_iter;iter++){
                double gadr_x=0;
                double gadr_y=0;
                double gadr_z=0;
                int anch_count=0;

                for(int j=0;j<n;j++){
                    if(spoof_count[j])continue;
                    
                    double x=p.x-veri_arr[j].x;
                    double y=p.y-veri_arr[j].y;
                    double z=p.z-veri_arr[j].z;
                    double d=sqrt(x*x+y*y+z*z)+(1e-6);
                    double error = d-dist_mat[i*n+j];
                    
                    gadr_x=gadr_x+(error*(x/d));
                    gadr_y=gadr_y+(error*(y/d));
                    gadr_z=gadr_z+(error*(z/d));
                    anch_count++;
                }
                if(anch_count<3)break;
                p.x=p.x-(0.1*gadr_x);
                p.y=p.y-(0.1*gadr_y);
                p.z=p.z-(0.1*gadr_z);
            }
            double final_dev=sqrt(pow(p.x-rep[i].x,2)+pow(p.y-rep[i].y,2));
            if(final_dev>eps)veri_arr[i]=p;
        }
    }
}