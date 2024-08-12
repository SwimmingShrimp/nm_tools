#include<iostream>
using namespace std;
#include<unistd.h>

int main()
{
    // 左右相邻2个元素比较，大的往后移，小的往前移
    int arr[9]={4,2,8,0,5,7,1,3,9};
    for (int i=0;i<9;i++)
    {
        cout << arr[i] << " ";
    }
    for(int i=0;i<9;i++)
    {
        for(int j=0;j<9-i-1;j++)
        {
            if(arr[j]>arr[j+1])
            {
                int temp=arr[j];
                arr[j]=arr[j+1];
                arr[j+1]=temp;
            }
        }
    }
    cout << endl << "排序后的数组为：" << endl;
    for (int i=0;i<9;i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
    return 0;
    
}