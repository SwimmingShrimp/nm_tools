#include<iostream>
using namespace std;
#include<unistd.h>
void swap(int *p1, int *p2)
{
    int temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}
int main(){
    int a = 10;
    int b=20;
    swap(&a,&b);
    pause();
    return 0;
}