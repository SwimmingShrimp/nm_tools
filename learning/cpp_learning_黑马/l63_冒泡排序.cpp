/*
 * @Author: lixialin lixialin@nullmax.ai
 * @Date: 2024-04-10 20:22:05
 * @LastEditors: lixialin lixialin@nullmax.ai
 * @LastEditTime: 2024-04-10 20:31:19
 */
#include<iostream>
using namespace std;
#include<unistd.h>

void printarr(int * arr,int len)
{
    for(int i = 0; i < len; i++){
        cout << arr[i] << endl;
    }
    
}
void arrsort(int * arr,int len)
{
    for(int i = 0; i < len-1; i++){
        for(int j = 0; j < len-1-i; j++){
            if (arr[j] > arr[j+1])
            {        
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
            
        }   
    }
}

int main(){
    // 1.创建数组
    int arr[10] = {1,3,5,7,9,2,4,6,8,0};
    // 获取数组的长度
    int len = sizeof(arr)/sizeof(arr[0]);
    // 2. 冒泡排序
    arrsort(arr,len);
    // 3. 打印排序后的数组
    printarr(arr,len);
    
    pause();
    return 0;
}