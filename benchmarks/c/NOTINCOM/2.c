




#include<stdio.h>
int main(){
    long int n,m,i,j,t,c,k;
    scanf("%ld",&t);
    while(t--){
        c=0;
        scanf("%ld %ld",&n,&m);
        long int a[1000001]={0};
        for(i=0;i<n;i++){
            scanf("%ld",&k);
            if(k>0)
            a[k]=1;
        }
        for(j=0;j<m;j++){
            scanf("%d",&k);
            if(a[k]==1)
            c++;
        }
        
        printf("%ld\n",c);
    }
    return 0;
}

