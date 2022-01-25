




#include<stdio.h>

int map[9] = {0, 4, 5, 6, 1, 2, 3, 8, 7};

char berth[9][3] = {"NA\0", "LB\0", "MB\0", "UB\0", "LB\0", "MB\0", "UB\0", "SL\0", "SU\0"};

int main()
{
	int t;
	scanf("%d", &t);
	while(t--)
	{
		int n, x;
		scanf("%d", &n);
		x = n%8;
		if(x==0)
			x+=8;
		int i = map[x];
		printf("%d = %d%s\n", n, map[x]+(n-x), berth[i]);
	}
}

