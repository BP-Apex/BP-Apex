#include<stdio.h>

int main()
{
	int s[100],N,Q,x,y,i,query;
    scanf("%d",&N);
    int chef[100];
    for(i = 1; i <= N; i++)
    {
        scanf("%d",&s[i]);
        chef[i] = i;
    }

    scanf("%d",&Q);

    for(i=1; i<=Q; i++)
    {
        scanf("%d",&query);
        if(query==0)
        {
            scanf("%d %d",&x,&y);
            if(chef[x] == chef[y])
                printf("Invalid query!\n");
            else if(s[x]>s[y])
                chef[y]=x;
            else
                chef[x]=y;
        }
        else if(query==1)
        {
            scanf("%d",&x);
            printf("%d\n",chef[x]);
        }
    }
	return 0;
}

