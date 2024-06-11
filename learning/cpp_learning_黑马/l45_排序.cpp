#include<iostream>
using namespace std;
#include<unistd.h>

int main()
{
    int arr[5] = {1,3,2,5,4};
    cout << "Array before reversal: " << endl;
    for(int i=0;i<5;i++)
    {
        cout << arr[i] << endl;
    }
    //reversal
    int start = 0;
    int end = 4;
    while(start<end)
    {
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
    cout << "Array after reversal: " << endl;
    for(int i=0;i<5;i++)
    {
        cout << arr[i] << endl;
    }
}