#include<iostream>
using namespace std;
#include<unistd.h>
int main()  
{   
    int arr[5]={300,350,200,400,250};
    int max_weight=0;
    for(int i=0;i<5;i++)
    {
        if(arr[i]>max_weight){
            max_weight=arr[i];
        }
    }
    cout << "Maximum weight of pig is " << max_weight << endl;
    return 0;
}