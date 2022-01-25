




#include <stdio.h>

int main(){
    int t,i;
    scanf("%d",&t);
    while(t--){
        int n,m;
        scanf("%d %d",&n,&m);
        int a[n],b[m],j,k;
        for(j=0;j<n;j++){
            scanf("%d",&a[j]);
        }
        for(k=0;k<m;k++){
            scanf("%d",&b[k]);
        }
        int count=0;
        for(j=0;j<n;j++){
            for(k=0;k<m;k++){
                if(a[j]==b[k])
                    count++;
            }
        }
        printf("%d\n",count);
    }

    return 0;
}

