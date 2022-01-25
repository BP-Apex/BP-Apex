




#include <stdio.h>
#include <malloc.h>

void swap(long int Array[],long int one,long int two) {
    long int temp = Array[one];
    Array[one] = Array[two];
    Array[two] = temp;
}

long int partition(long int Array[],long int left,long int right) {
    long int pivot = Array[right];
    long int leftPointer = left - 1;
    long int rightPointer = right;
    for (;;) {
        while (Array[++leftPointer] > pivot) {
        }
        while (rightPointer > 0 && Array[--rightPointer] < pivot) {
        }
        if (leftPointer >= rightPointer) {
            break;
        } else {
            swap(Array, leftPointer, rightPointer);
        }
    }
    /* move pivot to partition point */
    swap(Array, leftPointer, right);
    return leftPointer;
}

void Quicksort(long int Array[],long int left,long int right) {
    if (left < right) {
        long int PartitionPoint = partition(Array, left, right);
        Quicksort(Array, left, PartitionPoint - 1);
        Quicksort(Array, PartitionPoint + 1, right);
    }
}

int main(void) {
	long int n,k,e,m,a[10001],b,t,sum=0,i,j;
	scanf("%ld",&t);
	while(t--){
	    scanf("%ld %ld %ld %ld",&n,&k,&e,&m);
	    for(i=0;i<n-1;i++){
	        a[i]=0;
	        for(j=0;j<e;j++){
	            scanf("%ld",&sum);
	            a[i]+=sum;
	        }
	    }
	    Quicksort(a,0,n-2);
	    //for(i=0;i<n-1;i++)
	      //  printf("%ld ",a[i]);
	    b=0;
	    for(i=0;i<e-1;i++){
	        scanf("%ld",&sum);
	        b+=sum;
	    }
	    //printf("%ld",a[n-k-1]);
	    
	    i = a[k-1] - b + 1;
	    
	    if(i<0)
	        printf("0\n");
	   else if(i >= m)
	        printf("Impossible\n");
	    else
	        printf("%ld\n",(a[k-1]-b)+1);
	}
	return 0;
}


