#include<stdio.h>

int FindChef(int c, int chef[])
{
	if(c != chef[c])
		chef[c] = FindChef(chef[c],chef);
	return chef[c];
}

int main()
{
	int s[100005],N,Q,x,y,a,b,i,query;
    scanf("%d",&N);
    int chef[100005];
    for(i = 1; i <= N; i++)
    {
        chef[i] = i;
    }
    for(i = 1; i <= N; i++)
    {
        scanf("%d",&s[i]);
    }

    scanf("%d",&Q);

    for(i=1; i<=Q; i++)
    {
        scanf("%d",&query);
        if(query==0)
        {
            scanf("%d %d",&x,&y);
            a=FindChef(x,chef);
            b=FindChef(y,chef);
            if(a==b){
                printf("Invalid query!\n");
            }
            else if(s[a]>s[b]){
                chef[b]=a;
            }
            else{
                chef[a]=b;
            }
        }
        else if(query==1)
        {
            scanf("%d",&x);
            printf("%d\n",FindChef(x,chef));
        }
    }

	return 0;
}

