




#include<stdio.h>
int main()
{
    int T,M,N;
    scanf("%d",&T);
    while(T--)
    {
        scanf("%d\n",&N);
        scanf("%d",&M);
        int A[N],B[M],i,j,count=0;
        for(i=0;i<N;i++)
        scanf("%d",&A[i]);
        for(j=0;j<M;j++)
        scanf("%d",&B[j]);
        for(i=0;i<N;i++)
        {
            for(j=0;j<M;j++)
            {
                if(A[i]==B[j])
                count++;
            }
        }
        printf("%d\n",count);
    }
    return 0;
}
        



